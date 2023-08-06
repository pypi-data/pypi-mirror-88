# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import tempfile
import zipfile
import ruamel
import logging

from shutil import copy2, copytree
from pathlib import Path

from azureml.exceptions import UserErrorException
from azureml._project.ignore_file import get_project_ignore_file, IgnoreFile
from azure.ml.component._api._utils import try_to_get_value_from_multiple_key_paths, get_value_by_key_path, \
    _make_zipfile, is_absolute, create_or_cleanup_folder, check_spec_file, _looks_like_a_url

COMPONENT_SNAPSHOT_DIR_NAME = ".build"


def _get_default_property(property_name):
    """
    Copied from azureml._base_sdk_common.cli_wrapper._common.get_default_property to decouple aml cli dependency.
    :return: Returns the default property value for property_name, if set using "az configure" command.
    Return None if no default value found.
    :rtype: str
    """
    try:  # python 3
        from configparser import ConfigParser
    except ImportError:  # python 2
        from ConfigParser import ConfigParser
    config = ConfigParser()
    # we always use az ml, so the config folder is .azure
    config_folder = ".azure"
    config.read(os.path.expanduser(os.path.join('~', config_folder, 'config')))
    if not config.has_section('defaults'):
        return None

    if config.has_option('defaults', property_name):
        return config.get('defaults', property_name)
    else:
        return None


class SnapshotItem:
    def __init__(self, absolute_path, *, relative_path_in_snapshot=None):
        self._absolute_path = absolute_path.resolve()

        # This check can NOT be removed.
        # Since the incoming absolute_path might be a symbol link pointing to the parent folder
        # of itself, which will cause infinite length of file paths.
        # Calling `absolute_path.exists()` to raise "OSError: Too many levels of symbol links"
        # to the user for this case.
        if not absolute_path.exists():
            raise FileNotFoundError("File not found: {}".format(absolute_path))

        if not relative_path_in_snapshot:
            raise ValueError("relative_path_in_snapshot must be specified.")
        self._relative_path = Path(relative_path_in_snapshot)

    @property
    def absolute_path(self):
        return self._absolute_path

    @property
    def relative_path(self):
        result = str(self._relative_path.as_posix())
        if self._absolute_path.is_dir():
            result += '/'
        return result

    def __repr__(self):
        return self.relative_path


class ComponentSnapshot:
    """Manage the snapshot of a component."""

    _DEFAULT_AMLIGNORE_FILE_CONFIG_KEY = 'component_amlignore_file'
    _LEGACY_AMLIGNORE_FILE_CONFIG_KEY = 'module_amlignore_file'

    def __init__(self, spec_file_path, additional_amlignore_file=None, logger=None):
        # Do the path resolve otherwise when the the spec_file_path is like 'module_spec.yaml'
        # which does not contain the parent paths, the `spec_file_path.parent` will be `.`
        # and result in the wrong folder structure of the created snapshot folder structure.
        self._spec_file_path = Path(spec_file_path).resolve()
        self._snapshot_folder = None

        if not additional_amlignore_file:
            additional_amlignore_file = _get_default_property(self._DEFAULT_AMLIGNORE_FILE_CONFIG_KEY)
            # fall back to look legacy aml ignore file.
            if additional_amlignore_file is None:
                additional_amlignore_file = _get_default_property(self._LEGACY_AMLIGNORE_FILE_CONFIG_KEY)
        self._additional_amlignore_file = \
            Path(additional_amlignore_file).resolve() if additional_amlignore_file else None

        if self._additional_amlignore_file:
            if not self._additional_amlignore_file.is_file():
                raise UserErrorException(
                    'The specified amlignore file: {0} does not exist.'.format(self._additional_amlignore_file))

        try:
            with open(spec_file_path, 'r') as f:
                self._spec_dict = ruamel.yaml.safe_load(f)
        except Exception as e:
            raise UserErrorException('Failed to load spec file {0}.\nException: \n{1}'.format(spec_file_path, e))

        if not logger:
            self.logger = logging.getLogger('snapshot')

        self._check_additional_includes()

        # This will be set in component registration and only when yaml is local source
        self.entry_file_relative_path = None

        # By default, the build folder will be COMPONENT_SNAPSHOT_DIR_NAME inside base path
        self._snapshot_build_folder = self.base_path / COMPONENT_SNAPSHOT_DIR_NAME

    @property
    def base_path(self):
        """The base folder path of the snapshot."""
        # First, go to the folder that contains the spec file
        path = self._spec_file_path.parent

        # Then, if sourceDirectory specified in the module spec, apply as relative directory.
        if self.source_directory:
            path = path / self.source_directory
            if path.resolve() not in self._spec_file_path.parents:
                raise UserErrorException(
                    "Invalid sourceDirectory '{}': "
                    "Source directory must be the parent folders of the module yaml spec file. "
                    "Please refer to https://aka.ms/module-source-directory for details.".format(self.source_directory)
                )

        # Finally, resolve the path and return.
        return path.resolve()

    @property
    def source_directory(self):
        return try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/sourceDirectory',
                'implementation/parallel/sourceDirectory',
                'implementation/hdinsight/sourceDirectory',
                'code',
            ]
        )

    @property
    def spec_file_relative_path(self):
        return self._spec_file_path.relative_to(self.base_path.resolve())

    @property
    def conda_file_relative_path(self):
        return try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/amlEnvironment/python/condaDependenciesFile',
                'implementation/parallel/amlEnvironment/python/condaDependenciesFile',
                'environment/conda/conda_dependencies_file',
                'environment/conda/pip_requirements_file',
            ]
        )

    @property
    def pip_file_relative_path(self):
        return try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/amlEnvironment/python/pipRequirementsFile',
                'implementation/parallel/amlEnvironment/python/pipRequirementsFile',
            ]
        )

    @property
    def conda_file(self):
        """The conda file path of the module (if any)."""
        return self.get_file_or_raise(self.conda_file_relative_path, 'conda')

    @property
    def pip_file(self):
        return self.get_file_or_raise(self.pip_file_relative_path, 'pip requirement')

    @property
    def entry_file(self):
        # Need to ensure that entry_file_relative_path is initialized before this
        # Currently all code path can ensure that
        if self.entry_file_relative_path is not None and is_absolute(self.entry_file_relative_path):
            return None
        return self.get_file_or_raise(self.entry_file_relative_path, 'entry file')

    @property
    def additional_includes_file_path(self):
        """Additional includes file, should be base_path/spec_file_name.additional_includes."""
        additional_includes_file_name = self._spec_file_path.with_suffix('.additional_includes')
        return self.base_path / additional_includes_file_name

    def get_file_or_raise(self, relative_path, name):
        if relative_path:
            conda_file_path = self.base_path / relative_path
            if os.path.isfile(conda_file_path):
                return conda_file_path
            elif self.additional_includes:
                # handle case when file in additional includes
                for inc in self._iter_additional_includes():
                    if Path(inc.relative_path).resolve().as_posix() == Path(relative_path).resolve().as_posix():
                        return inc.absolute_path
            else:
                raise UserErrorException('Can not find {0} file: {1}.'.format(name, relative_path))

        return None

    def create_snapshot(self):
        return self._make_zipfile(snapshot_items_iterator=self._iter_files())

    def create_spec_snapshot(self):
        def file_iterator():
            yield SnapshotItem(self._spec_file_path, relative_path_in_snapshot=self.spec_file_relative_path)
            if self.conda_file:
                yield SnapshotItem(self.conda_file, relative_path_in_snapshot=self.conda_file_relative_path)
            if self.pip_file:
                yield SnapshotItem(self.pip_file, relative_path_in_snapshot=self.pip_file_relative_path)
            if self.entry_file:
                yield SnapshotItem(self.entry_file, relative_path_in_snapshot=self.entry_file_relative_path)

        return self._make_zipfile(snapshot_items_iterator=file_iterator())

    def file_exists(self, relative_path):
        """Detect whether a given path exists in the snapshot."""
        if relative_path:
            # First, check snapshot folder
            if (self.base_path / relative_path).is_file():
                return True

            # If not found in snapshot folder, try to find in additional includes
            include_name = Path(relative_path).parts[0]
            for inc in self.additional_includes:
                if Path(inc).name == include_name:
                    full_path = (self.base_path / inc).parent / relative_path
                    if full_path.is_file():
                        return True

            # TODO: handle the case that the file is listed in ignore files.

        # Otherwise, not found
        return False

    @property
    def additional_amlignore_file(self):
        return self._additional_amlignore_file

    def _make_amlignore(self, snapshot_folder):
        if not self.additional_amlignore_file:
            return

        if not self._additional_amlignore_file.is_file():
            raise UserErrorException('The specified amlignore file: {0} is invalid.'
                                     .format(self._additional_amlignore_file))

        # Copy specified .amlignore to snapshot folder if there is not existing one in base folder
        merged_amlignore_file = snapshot_folder / '.amlignore'
        if not merged_amlignore_file.exists():
            self._copy_to(self.additional_amlignore_file, merged_amlignore_file)

        # Append content of specified .amlignore to ignore file in base folder if it exists
        elif merged_amlignore_file.is_file():
            with open(merged_amlignore_file, 'a') as fout, open(self.additional_amlignore_file, 'r') as fin:
                fout.write('\n\n# Additional ignore\n')
                for line in fin:
                    fout.write(line)
                self.logger.debug("Append content of {0} to {1}"
                                  .format(self.additional_amlignore_file, merged_amlignore_file))

        else:
            raise UserErrorException("Unrecognized amlignore file {}".format(merged_amlignore_file))

    @property
    def additional_includes(self):
        additional_includes = self._get_additional_includes_from_file()
        legacy_additional_includes = self._get_additional_includes_from_spec()

        if additional_includes is not None and legacy_additional_includes is not None:
            raise UserErrorException("The 'additionalIncludes' field in module spec is a duplicate configuration. "
                                     "Please remove it when a separate .additional_includes file is provided.")
        elif legacy_additional_includes is not None:
            self.logger.warning(
                "The 'additionalIncludes' in module spec is deprecated. "
                "Please set the additional includes in {} file, and save it to the same folder of {}. "
                "Refer to https://aka.ms/module-additional-includes for details.".format(
                    self._spec_file_path.with_suffix('.additional_includes').name,
                    self._spec_file_path.name
                )
            )
            additional_includes = legacy_additional_includes

        return additional_includes or []

    @property
    def hdinsight_pyfiles(self):
        """This property gets the pyFiles item inside HDInsight section."""
        pyfiles = get_value_by_key_path(dct=self._spec_dict, key_path='implementation/hdinsight/pyFiles')

        if not pyfiles:
            return None

        if isinstance(pyfiles, str):
            pyfiles = [pyfiles]

        if not isinstance(pyfiles, list):
            raise UserErrorException("The 'implementation/hdinsight/pyFiles' field in module spec got an "
                                     "unexpected type, expected to be a list but got {}.'".format(type(pyfiles)))

        return pyfiles

    def _get_additional_includes_from_spec(self):
        additional_includes = try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/additionalIncludes',
                'implementation/parallel/additionalIncludes',
                'implementation/hdinsight/additionalIncludes',
            ]
        )

        if not additional_includes:
            return None

        if isinstance(additional_includes, str):
            additional_includes = [additional_includes]

        if not isinstance(additional_includes, list):
            raise UserErrorException("The 'additionalIncludes' field in module spec got an unexpected type, "
                                     "expected to be a list but got {}.'".format(type(additional_includes)))

        return additional_includes

    def _get_additional_includes_from_file(self):
        additional_includes = None
        try:
            if self.additional_includes_file_path.is_file():
                with open(self.additional_includes_file_path) as f:
                    lines = f.readlines()
                    # Keep the additional_includes is None when the input is empty list
                    if lines:
                        additional_includes = [l.strip() for l in lines if len(l.strip()) > 0]
        except BaseException:
            self.logger.warning(
                "Failed to load additional_includes file: {0}.".format(self.additional_includes_file_path))
            self.logger.debug(
                "Failed to load additional_includes file: {0}.".format(self.additional_includes_file_path),
                exc_info=True)

        return additional_includes

    def _remove_suffix(self, path):
        """Given a path, remove the suffix from it.

        >>> str(Path('/mnt/c/hello.zip'))
        '/mnt/c/hello'
        """
        # Get the stem path name. i.e. For /mnt/c/hello.zip, find /mnt/c/hello
        return path.parent / path.stem

    def _should_be_treated_as_zipped_folder(self, path):
        """Given a path, detect whether it should be treated as a zipped folder.

        For example, given /mnt/c/hello.zip,
          1) If a file or folder named /mnt/c/hello.zip exists, return False
          2) Otherwise,
             a) If a folder named /mnt/c/hello, return True
             b) Otherwise, return False
        """
        if not path.suffix == '.zip':
            return False

        # The file or folder with the .zip suffix exists, not treated as zip folder
        if path.exists():
            return False

        # Get the stem path name. i.e. For /mnt/c/hello.zip, find /mnt/c/hello
        stem_path = self._remove_suffix(path)

        # If the folder /mnt/c/hello exists, return True, otherwise return False
        return stem_path.is_dir()

    def _check_additional_includes(self):
        seen = set()
        for inc in self.additional_includes:
            self._check_additional_includes_item(inc, dst_folder=self.base_path)
            name = (self.base_path / inc).resolve().name
            if name in seen:
                raise UserErrorException("Multiple additional includes item named '{}'.".format(name))
            seen.add(name)

    def _check_additional_includes_item(self, inc, dst_folder):
        inc_path = self.base_path / inc
        src = inc_path.resolve()

        # If the resolved file name is different with the origin input file name,
        # it means that the origin input path wasn't specified to a file name
        # e.g. the path "../../" might be resolved to /foo/bar
        if inc_path.name != src.name:
            self.logger.warning("It's recommended to specify the folder or file name in a additional included path, "
                                "e.g. '../src', '../src/python/library1' and '../assets/LICENSE'. "
                                "The current value is: {0}".format(inc))

        if not src.exists() and not self._should_be_treated_as_zipped_folder(src):
            raise UserErrorException('additionalIncludes path {0} was not found.'.format(src))

        # Check if src is root directory
        if len(src.parents) == 0:
            raise UserErrorException('Root directory is not supported for additionalIncludes.')

        dst_path = dst_folder / src.name
        if dst_path.is_symlink():
            # If the dst_path is a symbolic link, check if it points to the same place of src.
            # If so, treat as a good case; Otherwise, raise error.
            if dst_path.resolve() != src.resolve():
                raise UserErrorException('Path {0} has already existed as a symbolic link to {1}. '
                                         'Please check additionalIncludes.'.format(dst_path, dst_path.resolve()))
        elif dst_path.exists():
            raise UserErrorException('Path {0} has already existed. Please check additionalIncludes.'.format(dst_path))

    def _symbol_link_exist(self):
        for f in self.base_path.glob('**/*'):
            if f.is_symlink():
                return True
        return False

    def _copy_to(self, src, dst, try_to_zip_folders=False, folder_to_lookup_ignore_file=None):
        """Copy src file to dst file or copy src file/directory to location under dst directory.

        :param: src: The file or folder to be copied.
        :param: dst: The target folder to be copied to.
        :param: try_to_zip_folders: When the `src` contains a `.zip` suffix, and the file does not exist,
                                    try to find the folder with same name and copy zipped file.
                                    For example, when src is '/mnt/c/hello.zip', but there is no 'hello.zip' file
                                    in /mnt/c, try to find whether there is a folder named '/mnt/c/hello/'.
                                    If exists, package the folder as 'hello.zip' and then copy to dst folder.
        :param: folder_to_lookup_ignore_file: Specify a folder to lookup ignore file.
                                              This is used only when `try_to_zip_folder` is True.
                                              When creating the zip file, the files listed in the ignore files
                                              are skipped.
        """
        src = src.resolve()
        if src.is_file():
            # Identical to copy() except that copy2() also attempts to preserve file metadata.
            copy2(src, dst)
        elif src.is_dir():
            dst = dst / src.name
            copytree(src, dst)
        elif try_to_zip_folders and self._should_be_treated_as_zipped_folder(src):
            stem_path = self._remove_suffix(src)
            temp_zip_folder = Path(tempfile.mkdtemp()) / src.stem
            self._copy_to(stem_path, temp_zip_folder)
            zip_file = self._make_snapshot(temp_zip_folder, folder_to_lookup_ignore_file=folder_to_lookup_ignore_file)
            self._copy_to(Path(zip_file), dst)
        else:
            raise UserErrorException('Path {0} was not found.'.format(src))

    def _get_snapshot_folder(self):
        if self._snapshot_folder:
            return self._snapshot_folder

        if not self.additional_includes and not self.additional_amlignore_file and not self._symbol_link_exist():
            return self.base_path

        self._snapshot_folder = self._get_temp_snapshot_folder(snapshot_items_iterator=self._iter_files())
        return self._snapshot_folder

    def _make_snapshot(self, src_path, folder_to_lookup_ignore_file=None):
        """Make snapshot file and return its path given source file or directory."""
        src_path = Path(src_path)
        if not src_path.exists():
            raise FileNotFoundError("File or directory {} was not found.".format(src_path))
        if src_path.is_file() and src_path.suffix == '.zip':
            return str(src_path)

        temp_directory = Path(tempfile.mkdtemp())
        zip_file_path = str(temp_directory / (src_path.name + '.zip'))

        if not folder_to_lookup_ignore_file:
            folder_to_lookup_ignore_file = src_path
        if not Path(folder_to_lookup_ignore_file).is_dir():
            raise UserErrorException(
                "No such folder {} to lookup .amlignore from.".format(folder_to_lookup_ignore_file))

        exclude_function = get_project_ignore_file(str(folder_to_lookup_ignore_file)).is_file_excluded
        _make_zipfile(zip_file_path, str(src_path), exclude_function=exclude_function)
        return zip_file_path

    def _iter_additional_includes(self):
        for inc in self.additional_includes:
            path = self.base_path / inc
            if self._should_be_treated_as_zipped_folder(path):
                folder_to_zip = self._remove_suffix(path)
                zip_file = self._make_zipfile(snapshot_items_iterator=self._iter_files_in_folder(folder_to_zip))
                yield SnapshotItem(absolute_path=zip_file, relative_path_in_snapshot=path.name)
            else:
                yield from self._iter_files_in_folder(path)

    def _iter_files(self, skip_additional_includes=False):
        # Firstly, iterate files from main snapshot folder
        yield from self._iter_files_in_folder(
            self.base_path, include_top_level_folder=False, skip_additional_includes=skip_additional_includes)

        # Secondly, iterate files from each additional includes
        yield from self._iter_additional_includes()

        # Then, create zip entry for implementation/hdinsight/pyFiles if needed
        # NOTE: If the pyFiles is specified as zipped, the unzipped version will also included in snapshot.
        # TODO: Exclude unzipped version from snapshot.
        if self.hdinsight_pyfiles:
            for entry in self.hdinsight_pyfiles:
                path = self.base_path / entry
                if self._should_be_treated_as_zipped_folder(path):
                    folder_to_zip = self._remove_suffix(path)
                    zip_file = self._make_zipfile(snapshot_items_iterator=self._iter_files_in_folder(folder_to_zip))
                    yield SnapshotItem(absolute_path=zip_file, relative_path_in_snapshot=path.name)
                else:
                    # TODO: check existance of each entry
                    pass

    def _iter_files_in_folder(self, folder, include_top_level_folder=True, skip_additional_includes=False):
        def create_snapshot_item(path):
            relative_path = path.relative_to(folder)
            if include_top_level_folder:
                # folder must be resolved before getting name since it may be .. or ~ which do not have valid names
                folder_name = folder.resolve().name
                # Append folder_name to the top level of relative path if `include_top_level_folder` specified.
                relative_path = Path(folder_name) / relative_path

            return SnapshotItem(absolute_path=path, relative_path_in_snapshot=relative_path)

        def is_ignored(path):
            folders_to_check = [p for p in path.parents if p not in folder.parents]
            for parent in folders_to_check:
                ignore_file = get_project_ignore_file(str(parent))
                if ignore_file.is_file_excluded(path):
                    return True

            # If not match with the normal ignore files,
            # check the additional amlignore file to see if there's any match.
            if self.additional_amlignore_file:
                # NOTE: Must use the relative path here since the additional amlignore file
                #       may not layout in the same tree of the source path.
                #       Absolute paths will cause the check fail for that case.
                path = path.relative_to(folder)
                ignore_file = IgnoreFile(self.additional_amlignore_file)
                if ignore_file.is_file_excluded(path):
                    return True

            # Implicitly ignore snapshot build folder files
            from azure.ml.component.dsl._utils import _relative_to
            if _relative_to(path, self._snapshot_build_folder) is not None:
                return True

            # If the logic goes here, indicates that the file should not be ignored.
            return False

        def is_additional_includes(path: Path):
            return path == self.additional_includes_file_path

        if Path(folder).is_file():
            # Yield the item directly if it is a file
            yield SnapshotItem(absolute_path=folder, relative_path_in_snapshot=folder.name)

        else:
            # Otherwise treat as a folder
            if include_top_level_folder:
                yield create_snapshot_item(Path(folder))

            for cur_dir, dirnames, filenames in os.walk(folder, followlinks=True):
                for filename in filenames + dirnames:
                    full_path = Path(cur_dir) / filename
                    if skip_additional_includes and is_additional_includes(full_path):
                        continue
                    if not is_ignored(full_path):
                        yield create_snapshot_item(full_path)

    def _make_zipfile(self, snapshot_items_iterator, zip_file_name='temp.zip'):
        temp_directory = Path(tempfile.mkdtemp())
        zip_file = temp_directory / zip_file_name
        with zipfile.ZipFile(zip_file, 'w') as zf:
            for snapshot_item in snapshot_items_iterator:
                zf.write(snapshot_item.absolute_path, snapshot_item.relative_path)
            return zip_file

    def _create_snapshot_in_folder(self, folder, snapshot_items_iterator) -> Path:
        for snapshot_item in snapshot_items_iterator:
            if snapshot_item.absolute_path.is_file():
                copy2(snapshot_item.absolute_path, os.path.join(folder, snapshot_item.relative_path))
            else:
                os.mkdir(os.path.join(folder, snapshot_item.relative_path))
        return Path(folder)

    def _get_temp_snapshot_folder(self, snapshot_items_iterator):
        temp_directory = Path(tempfile.mkdtemp())
        return self._create_snapshot_in_folder(temp_directory, snapshot_items_iterator)


class LocalComponentSnapshot(ComponentSnapshot):
    """A local version of a component snapshot.

    The snapshot only supports vnext yaml(eg: inline additional includes is not supported).
    """

    def __init__(self, spec_file_path, additional_amlignore_file=None, snapshot_folder=None, logger=None):
        if _looks_like_a_url(spec_file_path):
            raise UserErrorException(
                'Only local file is supported when building a local snapshot, got {}'.format(spec_file_path))
        path = check_spec_file(spec_file_path)
        super(LocalComponentSnapshot, self).__init__(path, additional_amlignore_file, logger)
        if snapshot_folder is not None:
            # If user specified snapshot folder, use it
            if os.path.exists(snapshot_folder) and os.path.samefile(snapshot_folder, self.base_path):
                raise UserErrorException(
                    'Output directory {} is the same as project folder, which is not allowed.'.format(snapshot_folder))
            self._snapshot_build_folder = snapshot_folder

        # Clean up snapshot directory if not empty
        try:
            create_or_cleanup_folder(self._snapshot_build_folder)
        except Exception as e:
            raise RuntimeError('Failed to create or clean up snapshot folder: {}. Reason: {}'.format(
                snapshot_folder, e))

    def _get_additional_includes_from_spec(self):
        """Inline additional includes is not supported because it doesn't exist in vnext yaml."""
        additional_includes = try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/additionalIncludes',
                'implementation/parallel/additionalIncludes',
                'implementation/hdinsight/additionalIncludes',
            ]
        )

        if additional_includes:
            raise UserErrorException(
                'Inline additional includes found: {}, which is not supported.'.format(additional_includes))
        else:
            return None

    def _get_snapshot_folder(self):
        """Create snapshot in snapshot folder, returns created snapshot folder."""
        if self._snapshot_folder:
            return self._snapshot_folder

        self._snapshot_folder = self._create_snapshot_in_folder(
            self._snapshot_build_folder, self._iter_files(skip_additional_includes=True))
        return self._snapshot_folder
