# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import shutil
import inspect
from enum import Enum
from urllib import request
from pathlib import Path
from io import BytesIO
from typing import Sequence, Union, Mapping
from collections import OrderedDict
from tempfile import mkdtemp

from azure.ml.component._api._api import ModuleAPI, ComponentAPI
from azure.ml.component._core._component_contexts import CreationContext, RegistrationContext
from ruamel import yaml

from azureml.core import Workspace

from ._core import Component
from ._io_definition import _remove_empty_values, ParameterDefinition, InputDefinition, OutputDefinition
from ._environment import Environment
from ._run_settings_definition import RunSettingsDefinition, K8sRunSettingsDefinition
from azure.ml.component._util._utils import _extract_zip, _is_empty_dir, _sanitize_python_variable_name


# TODO: We should have a shared logger for component package
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)


def _to_camel(s, first_lower=False):
    result = s.title().replace('_', '')
    if first_lower and len(result) > 1:
        result = result[0].lower() + result[1:]
    return result


def _to_ordered_dict(data: dict) -> OrderedDict:
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = _to_ordered_dict(value)
    return OrderedDict(data)


class ComponentType(Enum):
    """Represents all types of components."""

    Component = 'Component'
    CommandComponent = 'CommandComponent'
    PipelineComponent = 'PipelineComponent'
    MPIComponent = 'MPIComponent'
    ParallelComponent = 'ParallelComponent'
    HDInsightComponent = 'HDInsightComponent'

    @classmethod
    def get_component_type_by_str(cls, type_str):
        if type_str is None:
            return cls.CommandComponent
        for t in cls:
            if t.value.lower() == type_str.lower():
                return t

        # The legacy mapping is to get the correct type from the job type in old style yaml.
        legacy_mapping = {
            'basic': cls.CommandComponent,
            'mpi': cls.MPIComponent,
            'parallel': cls.ParallelComponent,
            'hdinsight': cls.HDInsightComponent,
        }
        return legacy_mapping.get(type_str.lower(), cls.CommandComponent)

    def get_definition_class(self):
        mapping = {
            self.CommandComponent: CommandComponentDefinition,
            self.MPIComponent: MPIComponentDefinition,
            self.ParallelComponent: ParallelComponentDefinition,
            self.HDInsightComponent: HDInsightComponentDefinition,
        }
        # For unknown types, we simply use ComponentDefinition in default which includes interface to be used.
        return mapping.get(self, ComponentDefinition)


class ComponentDefinition(Component):
    r"""Represents a Component asset version.

    ComponentDefinition is immutable class.
    """
    SCHEMA_KEY = '$schema'
    SCHEMA = 'http://azureml/sdk-2-0/CommandComponent.json'
    HELP_DOC_KEY = 'helpDocument'
    CONTACT_KEY = 'contact'
    CODE_GEN_BY_KEY = 'codegenBy'
    TYPE = ComponentType.Component

    def __init__(
        self, name, version=None, display_name=None,
        description=None, tags=None, is_deterministic=False,
        inputs=None, parameters=None, outputs=None,
        runsettings: RunSettingsDefinition = None,
        workspace=None,
        creation_context=None,
        registration_context=None,
        namespace=None  # add namespace to be compatible with legacy usage
    ):
        """Initialize the component."""
        self._name = name
        self._namespace = namespace
        self._type = self.TYPE
        self._version = version
        self._display_name = display_name
        self._description = description
        self._tags = tags
        self._is_deterministic = is_deterministic
        inputs = inputs or {}
        parameters = parameters or {}
        outputs = outputs or {}
        self._inputs = {
            name: data if isinstance(data, InputDefinition) else InputDefinition.load({'name': name, **data})
            for name, data in inputs.items()
        }
        self._parameters = {
            name: data if isinstance(data, ParameterDefinition) else ParameterDefinition.load({'name': name, **data})
            for name, data in parameters.items()
        }
        self._outputs = {
            name: data if isinstance(data, OutputDefinition) else OutputDefinition.load({'name': name, **data})
            for name, data in outputs.items()
        }
        self._runsettings = runsettings
        self._k8srunsettings = None
        self._workspace = workspace
        self._creation_context = creation_context
        self._registration_context = registration_context

    @property
    def name(self) -> str:
        """Return the name of the component."""
        if self._namespace is not None:
            # If self._namespace is not None, it's a legacy module, we combine namespace and name as it's name
            return '{}://{}'.format(self._namespace, self._name)
        return self._name

    @property
    def display_name(self) -> str:
        """
        Return the display_name of the component.
        If display_name is None, return name without namespace instead.
        """
        if self._display_name is not None:
            return self._display_name
        elif "://" in self.name:
            # if the name contains '://', componet.run will fail with environment.register return 404
            return self.name.split("://")[-1]
        else:
            return self.name

    @property
    def version(self) -> str:
        """Return the version of the component."""
        return self._version

    @property
    def type(self) -> ComponentType:
        """Return the type of the component."""
        return self._type

    @property
    def inputs(self) -> Mapping[str, InputDefinition]:
        """Return the inputs of the component."""
        return self._inputs

    @property
    def parameters(self) -> Mapping[str, ParameterDefinition]:
        """Return the parameters of the component."""
        return self._parameters

    @property
    def outputs(self) -> Mapping[str, OutputDefinition]:
        """Return the outputs of the component."""
        return self._outputs

    @property
    def description(self):
        """Return the description of the component."""
        return self._description

    @property
    def tags(self):
        """Return the tags of the component."""
        return self._tags or {}

    @property
    def contact(self):
        """Return the contact of the component."""
        return self.tags.get(self.CONTACT_KEY)

    @property
    def help_document(self):
        """Return the help document of the component."""
        return self.tags.get(self.HELP_DOC_KEY)

    @property
    def is_deterministic(self) -> bool:
        """Return whether the component is deterministic."""
        return self._is_deterministic

    @property
    def workspace(self) -> Workspace:
        """Return the workspace of the component."""
        return self._workspace

    @property
    def creation_context(self):
        # If component is not initialized from module dto, create an empty CreationContext.
        if self._creation_context is None:
            self._creation_context = CreationContext({})
        return self._creation_context

    @creation_context.setter
    def creation_context(self, val):
        """Set creation context for ComponentDefinition."""
        self._creation_context = val

    @property
    def registration_context(self):
        # If component is not initialized from module dto, create an empty RegistrationContext.
        if self._registration_context is None:
            self._registration_context = RegistrationContext({})
        return self._registration_context

    @registration_context.setter
    def registration_context(self, val):
        """Set registration context for ComponentDefinition."""
        self._registration_context = val

    @property
    def identifier(self):
        """Return the identifier of the component(unique in one workspace)."""
        return self.registration_context.id

    @property
    def runsettings(self) -> RunSettingsDefinition:
        """Return the run settings definition of the component."""
        return self._runsettings

    @property
    def k8srunsettings(self) -> K8sRunSettingsDefinition:
        """Return the k8s run settings definition of the component."""
        return self._k8srunsettings

    @staticmethod
    def list(workspace, include_disabled=False) -> Sequence['ComponentDefinition']:
        """Return a list of components in the workspace.

        :param workspace: The workspace from which to list component definitions.
        :type workspace: azureml.core.workspace.Workspace
        :param include_disabled: Include disabled modules in list result
        :type include_disabled: bool
        :return: A list of module objects.
        :rtype: builtin.list['ComponentDefinition']
        """
        raise NotImplementedError

    @staticmethod
    def get(workspace, name, namespace=None, version=None):
        """Get the component definition object from the workspace.

        :param workspace: The workspace that contains the component.
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the component to return.
        :type name: str
        :param namespace: The namespace of the component to return.
        :type namespace: str
        :param version: The version of the component to return.
        :type version: str
        :return: The component definition object.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    @staticmethod
    def register(workspace, spec_file, package_zip, anonymous_registration: bool,
                 set_as_default, amlignore_file, version):
        """Register the component to workspace.

        :param workspace: The workspace that contains the component.
        :type workspace: azureml.core.workspace.Workspace
        :param spec_file: The component spec file. Accepts either a local file path, a GitHub url,
                           or a relative path inside the package specified by --package-zip.
        :type spec_file: Union[str, None]
        :param package_zip: The zip package contains the component spec and implementation code.
                           Currently only accepts url to a DevOps build drop.
        :type package_zip: Union[str, None]
        :param anonymous_registration: Whether to register the component as anonymous.
        :type anonymous_registration: bool
        :param set_as_default: Whether to update the default version.
        :type set_as_default: Union[str, None]
        :param amlignore_file: The .amlignore or .gitignore file used to exclude files/directories in the snapshot.
        :type amlignore_file: Union[str, None]
        :param version: If specified, registered component will use specified value as version
                                           instead of the version in the yaml.
        :return: The component definition.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    def validate(self):
        """Validate whether the component is valid."""
        raise NotImplementedError

    def enable(self):
        """Enable a component in the workspace.

        :return: The updated component object.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    def disable(self):
        """Disable a component in the workspace.

        :return: The updated component object.
        :rtype: azure.ml.component.core.ComponentDefinition
        """
        raise NotImplementedError

    @classmethod
    def load(cls, yaml_file) -> 'ComponentDefinition':
        """Load a component definition from a component yaml file."""
        with open(yaml_file) as fin:
            return cls._from_dict(yaml.safe_load(fin))

    def _dump_to_stream(self, stream):
        """Dump the component definition to stream with specific style."""
        _setup_yaml(yaml)
        data = _to_ordered_dict(self._to_dict())
        yaml.dump(data, stream, default_flow_style=False)

    def save(self, yaml_file):
        """Dump the component definition to a component yaml file.

        :param yaml_file: The target yaml file path
        :type yaml_file: str
        """
        with open(yaml_file, 'w') as fout:
            self._dump_to_stream(fout)

    @classmethod
    def _from_dict(cls, dct, ignore_unexpected_keywords=True):
        """Load a component definition from a component yaml dict."""
        # TODO: Load the dict according to the schema version.
        if cls.SCHEMA_KEY in dct:
            dct.pop(cls.SCHEMA_KEY)

        component_type = None if 'type' not in dct else dct.pop('type')
        if cls.TYPE not in {None, ComponentType.Component} and component_type not in {None, cls.TYPE.value}:
            raise TypeError("The type must be %r." % cls.TYPE.value)

        # Distinguish inputs and parameters from original yaml dict if parameters is not specified.
        if not dct.get('parameters'):
            inputs = dct.pop('inputs') if 'inputs' in dct else {}
            types = {k: data['type'] if isinstance(data, dict) else data.type for k, data in inputs.items()}
            dct['inputs'] = {
                k: data for k, data in inputs.items() if not ParameterDefinition.is_valid_type(types[k])
            }
            dct['parameters'] = {
                k: data for k, data in inputs.items() if ParameterDefinition.is_valid_type(types[k])
            }

        valid_parameters = inspect.signature(cls).parameters
        for key in [k for k in dct]:
            if key not in valid_parameters:
                if ignore_unexpected_keywords:
                    dct.pop(key)
                else:
                    raise KeyError("The dict contain an unexpected keyword '%s'." % key)
        return cls(**dct)

    def _to_dict(self):
        """Convert the component definition to a python dict."""
        # Currently we combine inputs/parameters
        inputs = {
            **{key: val.to_dict(remove_name=True) for key, val in self.inputs.items()},
            **{key: val.to_dict(remove_name=True) for key, val in self.parameters.items()}
        }
        outputs = {key: val.to_dict(remove_name=True) for key, val in self.outputs.items()}
        result = {
            self.SCHEMA_KEY: self.SCHEMA,
            'name': self.name,
            'version': self.version,
            'display_name': self.display_name,
            'type': self.type.value,
            'description': self.description,
            'is_deterministic': self.is_deterministic,
            'tags': self.tags,
            'inputs': inputs,
            'outputs': outputs,
        }
        # We don't remove empty values of tags since it may contains the values like {tag: None}
        result = _remove_empty_values(result, ignore_keys={'tags'})
        return result

    VALID_NAME_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-')

    @classmethod
    def is_valid_name(cls, name: str):
        """Indicate whether the name is a valid component name."""
        return all(c in cls.VALID_NAME_CHARS for c in name)


class CommandComponentDefinition(ComponentDefinition):
    r"""represents a Component asset version.

    ComponentDefinition is immutable class.
    """
    SCHEMA = 'http://azureml/sdk-2-0/CommandComponent.json'
    TYPE = ComponentType.CommandComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=False,
                 inputs=None, parameters=None, outputs=None,
                 runsettings: RunSettingsDefinition = None,
                 command=None, environment=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None,
                 namespace=None  # add namespace to be compatible with legacy usage
                 ):
        """Initialize a CommandComponentDefinition from the args."""
        super().__init__(
            name=name, namespace=namespace, version=version, display_name=display_name,
            description=description,
            tags=tags,
            is_deterministic=is_deterministic,
            inputs=inputs, parameters=parameters, outputs=outputs,
            runsettings=runsettings,
            workspace=workspace,
            creation_context=creation_context,
            registration_context=registration_context
        )
        self._command = command
        if isinstance(environment, dict):
            environment = Environment._from_dict(environment)
        self._environment = environment
        self._code = code
        self._snapshot_local_cache = None
        self._api_caller = None

        # This field is used for telemetry when loading the component from a workspace,
        # a new name may be required since the interface has been changed to `get` instead of `load`
        self._load_source = None

        # This property is a workaround to unblock the implementation of Component,
        # will be removed after all the implementations are ready.
        self._module_dto = None

    @property
    def command(self):
        """Return the command of the CommandComponentDefinition."""
        return self._command

    @property
    def environment(self) -> Environment:
        """Return the environment of the CommandComponentDefinition."""
        if self._environment is None:
            self._environment = Environment()
        return self._environment

    @property
    def code(self):
        """Return the source code directory of the CommandComponentDefinition."""
        return self._code or '.'

    @property
    def _registered(self) -> bool:
        """Return whether the CommandComponentDefinition is registered in the workspace."""
        return self.workspace is not None and self.identifier is not None

    @property
    def api_caller(self):
        """CRUD layer to call rest APIs."""
        if self._api_caller is None:
            self._api_caller = ComponentAPI(self.workspace, logger=logger)
        return self._api_caller

    @api_caller.setter
    def api_caller(self, api_caller):
        """Setter for api caller."""
        self._api_caller = api_caller

    def _to_dict(self) -> dict:
        """Convert the component definition to a python dict."""
        result = super()._to_dict()
        values_to_update = {
            'command': self._reformat_command(self.command),
            'environment': self.environment._to_dict(),
            'code': self.code if self.code != '.' else None,
        }
        result.update(_remove_empty_values(values_to_update))
        return result

    @property
    def snapshot_url(self) -> str:
        """Return the snapshot url for a registered CommandComponentDefinition."""
        if not self._registered:
            raise ValueError("Only registered CommandComponent has a snapshot url.")
        return self.api_caller.get_snapshot_url_by_id(component_id=self.identifier)

    def get_snapshot(self, target=None, overwrite=False) -> Path:
        """Get the snapshot in target folder, if target is None, the snapshot folder is returned."""
        if target is not None:
            target = Path(target)
            if target.exists() and not _is_empty_dir(target) and not overwrite:
                raise FileExistsError("Target '%s' can only be an empty folder when overwrite=False." % target)
            if target.exists():
                # Remove the empty folder to store snapshot.
                shutil.rmtree(target)
            # Make sure the parent folder exists.
            target.parent.mkdir(exist_ok=True, parents=True)
        if self._snapshot_local_cache and Path(self._snapshot_local_cache).exists():
            if target is None:
                return self._snapshot_local_cache
            shutil.copytree(str(self._snapshot_local_cache), str(target))
        else:
            if target is None:
                target = mkdtemp()
            self._download_snapshot(target)
            self._snapshot_local_cache = target
            return target

    def _download_snapshot(self, target: Union[str, Path]):
        """Download the snapshot in the target folder."""
        snapshot_url = self.snapshot_url
        response = request.urlopen(snapshot_url)
        _extract_zip(BytesIO(response.read()), target)

    @staticmethod
    def get(
            workspace: Workspace, name: str, version: str = None,
    ) -> 'CommandComponentDefinition':
        """Get the component definition object from the workspace."""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        component = api_caller.get(
            name=name,
            version=version,  # If version is None, this will get the default version
        )
        component.api_caller = api_caller
        return component

    @staticmethod
    def get_by_id(workspace: Workspace, _id: str):
        """Get the component definition object by its id from the workspace."""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        component = api_caller.get_by_id(_id)
        component.api_caller = api_caller
        return component

    @staticmethod
    def batch_get(workspace: Workspace, module_version_ids, selectors):
        """Batch get component definition objects by their id or identifiers."""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        result = api_caller.batch_get(module_version_ids, selectors)
        for d in result:
            d.api_caller = api_caller

        return result

    @staticmethod
    def list(workspace, include_disabled=False) -> Sequence['CommandComponentDefinition']:
        """Return a list of components in the workspace."""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        return api_caller.list(include_disabled=include_disabled)

    @staticmethod
    def register(workspace, spec_file, package_zip, anonymous_registration: bool,
                 set_as_default, amlignore_file, version):
        """Register from yaml file or URL"""
        api_caller = ComponentAPI(workspace=workspace, logger=logger)
        return api_caller.register(spec_file=spec_file, package_zip=package_zip,
                                   anonymous_registration=anonymous_registration,
                                   set_as_default=set_as_default,
                                   amlignore_file=amlignore_file, version=version)

    @staticmethod
    def _register_module(workspace, spec_file, package_zip, anonymous_registration: bool,
                         set_as_default, amlignore_file, version):
        """Only used for backward compatibility. Register from yaml file or URL"""
        api_caller = ModuleAPI(workspace=workspace, logger=logger)
        return api_caller.register(spec_file=spec_file, package_zip=package_zip,
                                   anonymous_registration=anonymous_registration,
                                   set_as_default=set_as_default,
                                   amlignore_file=amlignore_file, version=version)

    @classmethod
    def load(cls, yaml_file) -> 'CommandComponentDefinition':
        with open(yaml_file) as fin:
            result = cls._from_dict(yaml.load(fin))
        result._snapshot_local_cache = Path(Path(yaml_file).parent / result.code)
        return result

    @classmethod
    def _from_dict(cls, dct, ignore_unexpected_keywords=False) -> 'CommandComponentDefinition':
        """Load a component definition from a component yaml dict."""
        return super()._from_dict(dct, ignore_unexpected_keywords=ignore_unexpected_keywords)

    @staticmethod
    def _reformat_command(command):
        """Reformat the command to make the output yaml clear."""
        if isinstance(command, str):
            return _CommandStr(command)
        if not command:
            return []
        # Here we call _YamlFlowList and _YamlFlowDict to have better representation when dumping args to yaml.
        result = []
        for arg in command:
            if isinstance(arg, list):
                arg = [_YamlFlowDict(item) if isinstance(item, dict) else item for item in arg]
                arg = _YamlFlowList(arg)
            result.append(arg)
        return result

    @classmethod
    def _module_yaml_convert_arg_item(cls, arg, inputs, parameters, outputs):
        """Convert one arg item in old style yaml to new style."""
        if isinstance(arg, (str, int, float)):
            return arg
        if isinstance(arg, list):
            return cls._module_yaml_convert_args(arg, inputs, parameters, outputs)
        if not isinstance(arg, dict) or len(arg) != 1:
            raise ValueError("Arg item is not valid: %r" % arg)
        key, value = list(arg.items())[0]
        for value_key in ['inputs', 'outputs', 'parameters']:
            items = locals()[value_key]
            # Parameters are also $inputs.xxx
            if value_key == 'parameters':
                value_key = 'inputs'
            for item in items:
                if item['name'] == value:
                    return '{%s.%s}' % (value_key, item['argumentName'])
        raise ValueError("%r is not in inputs and outputs." % value)

    @classmethod
    def _module_yaml_convert_args(cls, args, inputs, parameters, outputs):
        """Convert the args in old style yaml to new style."""
        return [cls._module_yaml_convert_arg_item(arg, inputs, parameters, outputs) for arg in args] if args else []

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        """Construct the component dict from an old style ModuleDefinition."""
        inputs, parameters, outputs = module.input_ports, module.params, module.output_ports
        for item in inputs + parameters + outputs:
            if 'argumentName' not in item:
                item['argumentName'] = _sanitize_python_variable_name(item['name'])
            if 'options' in item:
                # This field is different in old module definition and vNext definition.
                item['enum'] = item.pop('options')

        command = module.command or []
        command += cls._module_yaml_convert_args(module.args, inputs, parameters, outputs)
        # Convert the command from list to string
        command = ' '.join(arg if isinstance(arg, str) else '[%s %s]' % (arg[0], arg[1]) for arg in command)

        input_pairs = [(item.pop('argumentName'), item) for item in inputs]
        parameter_pairs = [(item.pop('argumentName'), item) for item in parameters]
        output_pairs = [(item.pop('argumentName'), item) for item in outputs]

        env = module.aml_environment or {}
        if env and 'python' in env:
            env['conda'] = env.pop('python')
        if module.image:
            env.update({'docker': {'image': module.image}})

        # Get tags according to the old yaml.
        tags = {key: None for key in module.tags} if module.tags else {}
        if module.help_document:
            tags[cls.HELP_DOC_KEY] = module.help_document
        if module.contact:
            tags[cls.CONTACT_KEY] = module.contact
        if cls.CODE_GEN_BY_KEY in module.annotations:
            tags[cls.CODE_GEN_BY_KEY] = module.annotations[cls.CODE_GEN_BY_KEY]

        # Convert the name to make sure only valid characters
        name = '%s://%s' % (module.namespace, module.name) if module.namespace else module.name
        name = name.lower().replace('://', '.').replace('/', '.').replace(' ', '_')
        new_dct = {
            'name': name,
            # This is a hard code rule.
            'version': module.version,
            'display_name': module.name,
            'is_deterministic': module.is_deterministic,
            'description': module.description,
            'tags': tags,
            'type': cls.TYPE.value,
            'inputs': {key: value for key, value in input_pairs},
            'parameters': {key: value for key, value in parameter_pairs},
            'outputs': {key: value for key, value in output_pairs},
            'command': command,
            'environment': env,
            'code': module.source_directory,
        }
        return new_dct

    @staticmethod
    def _from_module_yaml_dict(dct) -> 'CommandComponentDefinition':
        """Load the component from the old style module yaml dict."""
        from ..dsl._module_spec import _YamlModuleDefinition, _YamlParallelModuleDefinition, \
            _YamlHDInsightModuleDefinition
        definition_cls, cls = _YamlModuleDefinition, CommandComponentDefinition
        job_type = dct.get('jobType')
        if job_type is not None:
            if job_type.lower() == 'parallel':
                definition_cls, cls = _YamlParallelModuleDefinition, ParallelComponentDefinition
            elif job_type.lower() == 'hdinsight':
                definition_cls, cls = _YamlHDInsightModuleDefinition, HDInsightComponentDefinition
            elif job_type.lower() == 'mpi':
                definition_cls, cls = _YamlModuleDefinition, MPIComponentDefinition
        return cls._from_dict(cls._construct_dict_from_module_definition(definition_cls(dct)))

    @classmethod
    def _from_module_yaml_file(cls, f):
        """Load the component from the old style module yaml file."""
        with open(f) as fin:
            return cls._from_module_yaml_dict(yaml.safe_load(fin))

    DEFAULT_SPEC_FILE = 'spec.yaml'
    DEFAULT_CONDA_FILE = 'conda.yaml'

    def _save_to_code_folder(self, folder, spec_file=None):
        """Save the module spec to specific folder under the source directory."""
        from ..dsl._module_spec import _dump_yaml_file, _relative_to, _Dependencies

        _setup_yaml(yaml)
        if spec_file is None:
            spec_file = self.DEFAULT_SPEC_FILE
        source_directory = self.code if self.code else \
            Path(folder).resolve().absolute().as_posix()
        spec_file = (Path(folder) / spec_file).resolve()
        spec_dict = _to_ordered_dict(self._to_dict())
        if 'code' in spec_dict:
            spec_dict.pop('code')
        # Check whether the spec path is valid and set sourceDirectory to spec_dict.
        try:
            source_dir_2_spec_folder = _relative_to(spec_file.parent, source_directory, raises_if_impossible=True)
        except ValueError as e:
            raise ValueError("Target spec file '%s' is not under the source directory '%s'." % (
                spec_file.absolute().as_posix(), source_directory
            )) from e
        relative_path = source_dir_2_spec_folder.as_posix()
        if relative_path != '.':
            relative_path = ''.join(['../'] * len(relative_path.split('/')))  # aa/bb => ../../
            spec_dict['code'] = relative_path

        env = self.environment
        conda_file = env.conda_file
        # Check whether we need to specify a default conda file in the folder containing the spec file.
        # The scenario is that conda_dict/conda_file is not specified, while the conda is specified in dsl.component.
        if env.conda is not None and env.conda_dict is None and env.conda_file is None:
            conda_file = (source_dir_2_spec_folder / self.DEFAULT_CONDA_FILE).as_posix()
            spec_dict['environment']['conda'][env.CONDA_FILE_KEY] = conda_file

        # Dump a default conda dependencies to the folder if the conda file doesn't exist.
        # The scenario that the initialized conda is a file need to be refined
        # because we don't know where is the conda.
        if conda_file and not (Path(source_directory) / conda_file).exists():
            msg = "Conda file %s doesn't exist in the folder %s, a default one is dumped." % (conda_file, folder)
            logging.info(msg)
            _dump_yaml_file(
                _Dependencies.create_default().conda_dependency_dict,
                Path(source_directory) / conda_file
            )

        # Here we set unsafe=True because we used _YamlFlowDict, _YamlFlowList _str_ for better readability
        _dump_yaml_file(spec_dict, spec_file, unsafe=True, header=YAML_HELP_COMMENTS)


class MPIComponentDefinition(CommandComponentDefinition):
    """The component definition of a MPI component,
    currently there is no difference with CommandComponentDefinition.
    """

    TYPE = ComponentType.MPIComponent


class ParallelComponentDefinition(CommandComponentDefinition):
    """The component definition of a parallel component."""

    TYPE = ComponentType.ParallelComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=False,
                 inputs=None, parameters=None, outputs=None,
                 input_data=None, output_data=None,
                 entry=None,
                 command=None, environment=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None):
        super().__init__(
            name=name, version=version, display_name=display_name,
            description=description, tags=tags,
            is_deterministic=is_deterministic, inputs=inputs, parameters=parameters, outputs=outputs,
            command=command, environment=environment,
            code=code,
            workspace=workspace, creation_context=creation_context, registration_context=registration_context,
        )
        # Here we support multiple input_data as an input list.
        self._input_data = input_data if isinstance(input_data, list) else [input_data]
        self._output_data = output_data
        self._entry = entry
        self._job_type = 'parallel'

    @property
    def input_data(self) -> Sequence[str]:
        return self._input_data

    @property
    def output_data(self) -> str:
        return self._output_data

    @property
    def entry(self) -> str:
        return self._entry

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        dct = super()._construct_dict_from_module_definition(module)
        # Use name mapping to make sure input_data/output_data are correct
        # since the component definition uses argument name as the key
        name_mapping = {}
        for item in module.input_ports + module.output_ports:
            name_mapping[item['name']] = item.get('argumentName', _sanitize_python_variable_name(item['name']))
        input_data = module.input_data if isinstance(module.input_data, list) else [module.input_data]
        dct['parallel'] = {
            'inputData': [name_mapping[i] for i in input_data],
            'outputData': name_mapping[module.output_data],
            'entry': module.entry,
        }
        return dct

    @classmethod
    def _from_dict(cls, dct) -> 'ParallelComponentDefinition':
        component_type = dct.pop('type') if 'type' in dct else None
        if component_type != cls.TYPE.value:
            raise ValueError("The type must be %r, got %r." % (cls.TYPE.value, component_type))
        if 'parallel' in dct:
            parallel = dct.pop('parallel')
            dct['input_data'] = parallel['inputData']
            dct['output_data'] = parallel['outputData']
            dct['entry'] = parallel['entry']
        return super()._from_dict(dct)

    def _to_dict(self) -> dict:
        result = super()._to_dict()
        parallel_section = {
            'parallel': {
                'inputData': self.input_data,
                'outputData': self.output_data,
                'entry': self.entry
            }}
        result.update(_remove_empty_values(parallel_section))
        return result


class HDInsightComponentDefinition(CommandComponentDefinition):
    """The component definition of a HDInsight component."""

    TYPE = ComponentType.HDInsightComponent

    def __init__(self, name, version=None, display_name=None,
                 description=None, tags=None, is_deterministic=False,
                 inputs=None, parameters=None, outputs=None,
                 file=None, jars=None,
                 py_files=None,
                 command=None, environment=None,
                 code=None,
                 workspace=None,
                 creation_context=None,
                 registration_context=None):
        super().__init__(
            name=name, version=version, display_name=display_name, description=description, tags=tags,
            is_deterministic=is_deterministic, inputs=inputs, parameters=parameters, outputs=outputs,
            command=command, environment=environment,
            code=code,
            workspace=workspace, creation_context=creation_context, registration_context=registration_context,
        )
        self._file = file
        self._jars = jars
        self._py_files = py_files

    @property
    def file(self) -> str:
        return self._file

    @property
    def jars(self) -> Sequence[str]:
        return self._jars

    @property
    def py_files(self) -> Sequence[str]:
        return self._py_files

    @classmethod
    def _construct_dict_from_module_definition(cls, module):
        dct = super()._construct_dict_from_module_definition(module)
        dct['hdinsight'] = {
            'file': module.file,
            'jars': module.jars,
            'pyFiles': module.py_files,
        }
        return dct

    @classmethod
    def _from_dict(cls, dct) -> 'HDInsightComponentDefinition':
        job_type = None if 'jobType' not in dct else dct.pop('jobType')
        component_type = None if 'type' not in dct else dct.pop('type')
        if component_type is None:
            if job_type is None or job_type.lower() != 'hdinsight':
                raise ValueError("The job type must be hdinsight, got '%s'." % job_type)
        else:
            if component_type != ComponentType.HDInsightComponent.value:
                raise ValueError("The type must be '%s', got '%s'." %
                                 (ComponentType.HDInsightComponent, component_type))
        if 'hdinsight' in dct:
            hdinsight = dct.pop('hdinsight')
            dct['file'] = hdinsight['file']
            dct['jars'] = hdinsight['jars']
            dct['py_files'] = hdinsight['pyFiles']
        return super()._from_dict(dct)

    def _to_dict(self) -> dict:
        result = super()._to_dict()
        hdinsight_section = {
            'hdinsight': {
                'file': self._file,
                'jars': self._jars,
                'pyFiles': self._py_files,
            }}
        result.update(_remove_empty_values(hdinsight_section))
        return result


class PipelineComponentDefinition(ComponentDefinition):
    r"""represents a Component asset version.

    ComponentDefinition is immutable class.
    """
    SCHEMA = 'http://azureml/sdk-2-0/PipelineComponent.json'
    TYPE = ComponentType.PipelineComponent

    def __init__(self, id, name, components: dict, components_variable_names=None, description=None,
                 inputs=None, outputs=None, parameters=None, workspace=None,
                 parent_definition_id=None, from_module_name=None, pipeline_function_name=None,
                 outputs_mapping=None, default_compute_target=None,
                 default_datastore=None, components_args_matched_dict_list=None):
        """
        :param id: Definition id.
        :type id: str
        :param name: Definition name.
        :type name: str
        :param components: Id to components dict inside pipeline definition.
        :type components: OrderedDict[str, Component]
        :param components_variable_names: The variable names of pipeline's components.
        :type components_variable_names: list[str]
        :param description: Description of definition.
        :type description: str
        :param inputs: A dict of inputs name to definition.
        :type inputs: dict[str, InputDefinition]
        :param outputs: A dict of outputs name to definition.
        :type outputs: dict[str, OutputDefinition]
        :param parameters: Parameters of function defined by dsl.pipeline.
        :type parameters: dict
        :param workspace: workspace of definition.
        :type workspace: Workspace
        :param parent_definition_id: parent definition id.
        :type parent_definition_id: str
        :param from_module_name: from module name.
        :type from_module_name: str
        :param pipeline_function_name: The pipeline funtion name.
        :type pipeline_function_name: str
        :param outputs_mapping: A dict of outputs name to OutputBuilder on Component.
            Different from outputs, the outputs mapping is the real outputs of a pipeline,
             the _owner of dict value(OutputBuilder) is the component of definition.
            This mapping is used to record dsl.pipeline function's output
             and create a pipeline component instance from definition.
        :type outputs_mapping: dict[str, _OutputBuilder]
        :param default_compute_target: The resolved default compute target.
        :type default_compute_target: tuple(str, str)
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :param components_args_matched_dict_list: A list of dictionaries use to convert kwargs
            from pipeline input to have component matched key. Dict key is component
            definition, value is a dict of pipeline parameter keys to component parameter keys list.
        :type components_args_matched_dict_list: list[dict[str, tuple(str, str .. )]]
        """
        super().__init__(
            name=name, description=description, is_deterministic=False,
            inputs=inputs, outputs=outputs, parameters=parameters, workspace=workspace)
        self._components = components
        self._components_variable_names = components_variable_names
        self._id = id
        self._outputs_mapping = outputs_mapping
        self._default_compute_target = default_compute_target
        self._default_datastore = default_datastore
        self._components_args_matched_dict_list = components_args_matched_dict_list
        self._parent_definition_id = parent_definition_id
        # There are tests of the two field so we shall keep them in definition
        self._from_module_name = from_module_name
        self._pipeline_function_name = pipeline_function_name

    @property
    def components(self):
        """
        Get the components of a pipeline component definition.

        The components are shared by all the pipeline component created by same definition.

        :return: Id to component dict inside pipeline component definition.
        :rtype: dict[str, Component]
        """
        return self._components


class _YamlFlowDict(dict):
    """This class is used to dump dict data with flow_style."""

    @classmethod
    def representer(cls, dumper: yaml.dumper.Dumper, data):
        return dumper.represent_mapping('tag:yaml.org,2002:map', data, flow_style=True)


class _YamlFlowList(list):
    """This class is used to dump list data with flow_style."""

    @classmethod
    def representer(cls, dumper: yaml.dumper.Dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


class _CommandStr(str):
    """This class is used to dump command str with >- style."""
    @classmethod
    def representer(cls, dumper: yaml.dumper.Dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')


def _str_representer(dumper: yaml.dumper.Dumper, data):
    """Dump a string with normal style or '|' style according to whether it has multiple lines."""
    style = ''
    if '\n' in data:
        style = '|'
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=style)


def _setup_yaml(yaml):
    yaml.add_representer(_YamlFlowDict, _YamlFlowDict.representer)
    yaml.add_representer(_YamlFlowList, _YamlFlowList.representer)
    yaml.add_representer(_CommandStr, _CommandStr.representer)
    yaml.add_representer(str, _str_representer)
    yaml.add_representer(type(None), lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', ''))

    # Setup to preserve order in yaml.dump, see https://stackoverflow.com/a/8661021
    def _represent_dict_order(self, data):
        return self.represent_mapping("tag:yaml.org,2002:map", data.items())

    yaml.add_representer(OrderedDict, _represent_dict_order)


YAML_HELP_COMMENTS = """#  This is an auto generated component spec yaml file.
#  For more details, please refer to https://aka.ms/azure-ml-component-specs
"""
