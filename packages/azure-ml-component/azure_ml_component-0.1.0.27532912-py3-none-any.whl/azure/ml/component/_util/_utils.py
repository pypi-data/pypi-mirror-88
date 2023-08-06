# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import sys
import json
import docker
import zipfile
import functools
from pathlib import Path, PureWindowsPath
import uuid
from uuid import UUID

from azureml.data.data_reference import DataReference
from azureml.data._dataset import _Dataset
from azure.ml.component._restclients.designer.models import EntityStatus, DataInfo, \
    DataSetDefinition, RegisteredDataSetReference, SavedDataSetReference, \
    DataSetDefinitionValue, DataPath
from azureml.exceptions import WebserviceException


def _is_empty_dir(path):
    path = Path(path)
    return path.is_dir() and next(path.iterdir(), None) is None


def _extract_zip(zip_file, target_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)


def _normalize_identifier_name(name):
    import re
    normalized_name = name.lower()
    normalized_name = re.sub(r'[\W_]', ' ', normalized_name)  # No non-word characters
    normalized_name = re.sub(' +', ' ', normalized_name).strip()  # No double spaces, leading or trailing spaces
    if re.match(r'\d', normalized_name):
        normalized_name = 'n' + normalized_name  # No leading digits
    return normalized_name


def _sanitize_python_variable_name(name: str):
    return _normalize_identifier_name(name).replace(' ', '_')


def _sanitize_python_variable_name_with_value_check(name: str):
    sanitized_name = _sanitize_python_variable_name(name)
    if sanitized_name == '':
        raise ValueError('Given name {} could not be normalized into python variable name.'.format(name))
    return sanitized_name


def _get_or_sanitize_python_name(name: str, name_map: dict):
    return name_map[name] if name in name_map.keys() \
        else _sanitize_python_variable_name(name)


def is_float_convertible(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int_convertible(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_bool_string(string):
    if not isinstance(string, str):
        return False
    return string == 'True' or string == 'False'


def _is_uuid(str):
    try:
        UUID(hex=str)
    except ValueError:
        return False
    return True


def int_str_to_pipeline_status(str):
    if str == '0':
        return EntityStatus.active.value
    elif str == '1':
        return EntityStatus.deprecated.value
    elif str == '2':
        return EntityStatus.disabled.value
    else:
        return 'Unknown'


def _unique(elements, key):
    return list({key(element): element for element in elements}.values())


def _is_prod_workspace(workspace):
    if workspace is None:
        return True

    return workspace.location != "eastus2euap" and workspace.location != "centraluseuap" and \
        workspace.subscription_id != "4faaaf21-663f-4391-96fd-47197c630979"


def _can_visualize():
    """Return true if the platform widget can be visualized in jupyter notebook, otherwise return false."""
    try:
        from IPython import get_ipython
        from traitlets import Unicode
        from ipywidgets import DOMWidget

        if Unicode and DOMWidget:
            pass

        # ContainerClient only exists for azure.storage.blob >= 12.0.0
        # we will fallback to BlockBlobService if ContainerClient not exist
        try:
            from azure.storage.blob import ContainerClient
            if ContainerClient:
                pass
        except:
            from azure.storage.blob import BlockBlobService
            if BlockBlobService:
                pass

        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except (NameError, ModuleNotFoundError, ImportError):
        return False  # Probably standard Python interpreter


def _is_json_string_convertible(string):
    try:
        json.loads(string)
    except ValueError:
        return False
    return True


def _dumps_raw_json(obj):
    try:
        json_string = json.dumps(obj)
    except TypeError:
        return False
    return json_string


def _is_valid_raw_json(string):
    obj = json.loads(string)
    if isinstance(obj, str):
        return False
    return True


def _get_short_path_name(path, create_dir=False):
    '''
        https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file#short-vs-long-names
        Maximum length for a path may defined by 260 characters in Windows.
        So need to trans path to shorten path to avoid filename too long.
        Example short/long path in windows:
            long path: C:\\pipeline-local_run\\67a8bfde-9014-45c0-acc7-1db02d422302\\A dummy pipeline
            short path: C:\\PIPELI~2\\67A8BF~1\\ADUMMY~1
        :param path: need to be shorten path
        :type path: str
        :param create_dir: If create_dir=True, when create dirs before get shorten name
        :type create_dir: bool
        :return: short path form. If path is a short path, will no change.
        :rtype: str
    '''
    if os.name == 'nt':
        try:
            # win32api is an additional module for windows in pywin32
            # https://docs.python.org/3/using/windows.html#additional-modules
            import win32api
            path_list = Path(path).absolute().parts
            short_path = win32api.GetShortPathName(os.path.join(path_list[0]))
            for item in path_list[1:]:
                if create_dir:
                    Path(os.path.join(short_path, item)).mkdir(parents=True, exist_ok=True)
                short_path = win32api.GetShortPathName(os.path.join(short_path, item))
            return short_path
        except Exception:
            # If path is not exist will raise error.
            return str(PureWindowsPath(Path(path).absolute()))
    else:
        Path(path).mkdir(parents=True, exist_ok=True)
        return path


def _get_valid_directory_path(directory_path):
    suffix = 1
    valid_path = directory_path
    while os.path.exists(valid_path):
        valid_path = '{}({})'.format(directory_path, suffix)
        suffix += 1
    return valid_path


def _scrubbed_exception(exception_type, msg: str, args):
    """
    Return the exception with scrubbed error message. Use this to add scrubbed message to exceptions
    that we don't want the record the full message in because it may contains sensitive information.

    :param exception_type: The exception type to create.
    :param msg: The message format.
    :param args: The original args for message formatting.
    :return: The created exception.
    """
    scrubbed_data = '[Scrubbed]'
    e = exception_type(msg.format(args))
    e.scrubbed_message = msg.replace("{}", scrubbed_data)
    return e


def _get_data_info_hash_id(data_info: DataInfo):
    if data_info.saved_dataset_id is not None:
        identifier = data_info.saved_dataset_id
    elif data_info.relative_path is not None:
        identifier = _sanitize_python_variable_name(data_info.relative_path)
    elif data_info.id is not None:
        identifier = data_info.id
    elif data_info.name is not None:
        identifier = data_info.name
    else:
        raise ValueError('Invalid data source {}'.format(data_info.as_dict()))

    return str(uuid.uuid3(uuid.NAMESPACE_DNS, identifier))


def pull_docker_image(docker_client, image_location, username, password, stop_event=None):
    """
    Pulls the docker image from the ACR
    :param docker_client:
    :type docker_client: docker.DockerClient
    :param image_location:
    :type image_location: str
    :param username:
    :type username: str
    :param password:
    :type password: str
    :return:
    :rtype: None
    """
    try:
        print('Pulling image from ACR (this may take a few minutes depending on image size)...\n')
        for message in docker_client.api.pull(image_location, stream=True, decode=True, auth_config={
            'username': username,
            'password': password
        }):
            if stop_event and stop_event.isSet():
                print('Cancel pull image.')
                break
            prefix = '{}: '.format(message['id']) if 'id' in message else ''
            status = message['status']
            progress = message.get('progressDetails', {}).get('progress', '')
            print(prefix + status + progress)
    except docker.errors.APIError as e:
        raise WebserviceException('Error: docker image pull has failed:\n{}'.format(e))
    except Exception as exc:
        raise WebserviceException('Error with docker pull {}'.format(exc))


def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning('This method has been deprecated and will be removed in the future release.')
        return func(*args, **kwargs)
    return wrapper


def trans_to_valid_file_name(file_name):
    import re
    return re.sub('[/?<>\\\\:*|"]', '_', file_name)


def print_to_terminal(msg):
    from azure.ml.component._execution._component_run_logger import Logger
    if isinstance(sys.stdout, Logger):
        sys.stdout.print_to_terminal(msg)
    else:
        print(msg)


def get_dataset_def_from_dataset(workspace, dataset):
    # Resolve dataset def as value assignments if parameter is dataset
    dataset_def = None
    from .._dataset import _GlobalDataset
    if isinstance(dataset, _GlobalDataset) or isinstance(dataset, DataReference):
        dataset_def = _get_dataset_def_from_dataset(dataset)
    elif isinstance(dataset, _Dataset):
        dataset._ensure_saved(workspace)
        dataset_def = _get_dataset_def_from_dataset(dataset)
    return dataset_def


def _get_dataset_def_from_dataset(dataset):

    def _get_dataset_def_from_data_path(data_path, data_type):
        dataset_def_val = DataSetDefinitionValue(literal_value=data_path)
        dataset_def = DataSetDefinition(
            data_type_short_name=data_type,
            value=dataset_def_val
        )
        return dataset_def

    from .._dataset import _GlobalDataset
    if isinstance(dataset, _GlobalDataset):
        data_path = DataPath(data_store_name=dataset.data_store_name, relative_path=dataset.relative_path)
        return _get_dataset_def_from_data_path(data_path, 'DataFrameDirectory')

    if isinstance(dataset, DataReference):
        data_path = DataPath(data_store_name=dataset.datastore.name, relative_path=dataset.path_on_datastore)
        return _get_dataset_def_from_data_path(data_path, 'AnyDirectory')

    # Either data_set_reference or saved_data_set_reference shall be not None in dataset_def.
    saved_dataset_ref = None
    if dataset._registration and dataset._registration.registered_id:
        dataset_ref = RegisteredDataSetReference(
            id=dataset._registration and dataset._registration.registered_id,
            version=dataset._registration and dataset._registration.version
        )
    else:
        dataset_ref = None
        if dataset.id:
            saved_id = dataset.id
            saved_dataset_ref = SavedDataSetReference(id=saved_id)

    dataset_def_val = DataSetDefinitionValue(data_set_reference=dataset_ref,
                                             saved_data_set_reference=saved_dataset_ref)

    dataset_def = DataSetDefinition(
        data_type_short_name='AnyDirectory',
        value=dataset_def_val
    )
    return dataset_def
