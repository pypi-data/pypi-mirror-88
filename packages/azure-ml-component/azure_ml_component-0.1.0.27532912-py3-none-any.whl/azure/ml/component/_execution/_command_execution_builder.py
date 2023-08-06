# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from pathlib import Path

from azureml.core import Datastore, Dataset
from azureml.data.datapath import DataPath
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data import FileDataset
from azureml.exceptions._azureml_exception import UserErrorException
from azure.ml.component._util._utils import _get_short_path_name, print_to_terminal
from azure.ml.component._util._loggerfactory import _LoggerFactory, track
from .._core._component_definition import ComponentType
from .._pipeline_parameters import PipelineParameter
from ._command_execution import CommandExecution
from ._constants import OUTPUT_DIR_NAME, CONTAINER_INPUT_PATH, CONTAINER_OUTPUT_PATH, \
    CONTAINER_MOUNT_SCRIPTS_PATH, MOCK_PARALLEL_DRIVER, RUN_PREPARE_LOG, WORKING_DIR


_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class CommandExecutionBuilder:
    """Help to build component execution."""

    def __init__(self, component, working_dir, snapshot_path, tracker, logger, component_env):
        self.component = component
        self.working_dir = working_dir
        self.tracker = tracker
        self.logger = logger
        self.snapshot_path = snapshot_path
        self.component_env = component_env

    @track(_get_logger)
    def build(self):
        """Prepare command, environment and volumes to generate CommandExecution."""
        environment = {}
        cwd = self.snapshot_path

        # Generate command
        python_path = self.component_env.python_path if self.component_env.python_path else 'python'
        run_command = ComponentRunCommand(self.component, self.working_dir, self.component_env.os_type, python_path)
        command, volumes = run_command.generate_command(use_docker=self.component_env.image_name is not None)

        # For metric needed environment variables
        if self.tracker.track_run_history:
            environment.update(self._set_environment_variables_for_run())
        if self.component_env.image_name is not None:
            # Add scripts in volumes
            cwd = CONTAINER_MOUNT_SCRIPTS_PATH
            volumes[self.snapshot_path] = {'bind': CONTAINER_MOUNT_SCRIPTS_PATH, 'mode': 'rw'}

        return CommandExecution(command, environment, cwd, self.logger, volumes, self.component_env.image_name)

    def _set_environment_variables_for_run(self):
        run = self.tracker.get_run()
        env = {
            'AZUREML_RUN_ID': run.id,
            'AZUREML_ARM_SUBSCRIPTION': run.experiment.workspace.subscription_id,
            'AZUREML_ARM_RESOURCEGROUP': run.experiment.workspace.resource_group,
            'AZUREML_ARM_WORKSPACE_NAME': run.experiment.workspace.name,
            'AZUREML_ARM_PROJECT_NAME': run.experiment.name,
            'AZUREML_RUN_TOKEN': run._client.run.get_token().token,
            'AZUREML_WORKSPACE_ID': run.experiment.workspace._workspace_id,
            'AZUREML_SERVICE_ENDPOINT': run._client.run.get_cluster_url(),
            'AZUREML_DISCOVERY_SERVICE_ENDPOINT': run.experiment.workspace.discovery_url,
        }
        return env


class ComponentRunCommand:
    """Generate component run command"""

    def __init__(self, component, working_dir, os_type, python_path='python'):
        self.component = component
        self.working_dir = working_dir
        self.os_type = os_type
        self.python_path = python_path

    def generate_command(self, use_docker, check_data_exist=True, container_input_prefix=CONTAINER_INPUT_PATH,
                         container_output_prefix=CONTAINER_OUTPUT_PATH, remove_none_value=True):
        """
        Generate component run command.

        :param use_docker: Use docker.
        :type use_docker: bool
        :param check_data_exist: If check_data_exist=True, when input not exists raise error.
        :type check_data_exist: bool
        :param container_input_prefix: container input prefix
        :type container_input_prefix: str
        :param container_output_prefix: container output prefix
        :type container_output_prefix: str
        :param remove_none_value: whether remove None in command
        :type remove_none_value: bool
        :return input_path: Dict of input name and input path
                volumes: volumes of outputs
        :rtype Dict{(str, str)}, Dict{(str, Dict)}
        """
        input_path, input_volumes = self.generate_inputs(use_docker, check_data_exist, container_input_prefix)
        output_path, output_volumes = self.generate_outputs(use_docker, check_data_exist, CONTAINER_OUTPUT_PATH)
        input_volumes.update(output_volumes)

        # Get component run command
        command = [self.python_path, self.component._get_script()]
        # Get component arguments
        arguments = self.component._get_arguments(input_path, output_path, remove_none_value)
        command.extend(arguments)

        if self.component.type == ComponentType.MPIComponent.value:
            # Add mpi command in component execution command
            command = translate_mpi_command_by_component(command, self.component, self.os_type)
        elif self.component.type == ComponentType.ParallelComponent.value:
            # For parallel component, replace script and input arguments
            command = translate_parallel_command_by_component(command, self.component, input_path)

        return command, input_volumes

    def generate_inputs(self, use_docker, check_data_exist=True, container_input_prefix=CONTAINER_INPUT_PATH):
        """
        If use_docker=True, generate input path and volumes of container, else generate input path in local.

        :param use_docker: Use docker.
        :type use_docker: bool
        :param check_data_exist: If check_data_exist=True, when input not exists raise error.
        :type check_data_exist: bool
        :param container_input_prefix: container input prefix
        :type container_input_prefix: str
        :return input_path: Dict of input name and input path
                volumes: volumes of outputs
        :rtype Dict{(str, str)}, Dict{(str, Dict)}
        """
        input_path = {}
        volumes = {}
        for input_name, input_item in self.component.inputs.items():
            input_is_optional = self.component._input_is_optional(input_name)
            if isinstance(input_item._dset, str) or isinstance(input_item._dset, Path):
                # Change to absolute path to avoid relative import error when running locally
                input_item_path = Path(input_item._dset).resolve().absolute()
                short_input_item_path = Path(_get_short_path_name(input_item_path))
                port_name = self.component._pythonic_name_to_input_map[input_name]
                input_data_type = next(input.data_type_ids_list for input in self.component._interface_inputs
                                       if input.name == port_name)
                if ['AnyFile'] == input_data_type:
                    if not short_input_item_path.is_file():
                        short_input_item_path = next(
                            filter(lambda item: item.is_file(), short_input_item_path.iterdir()), None)
                if not check_data_exist or short_input_item_path.exists():
                    if use_docker:
                        if str(short_input_item_path) in volumes:
                            input_port_path = volumes[str(short_input_item_path)]['bind']
                        else:
                            input_port_path = container_input_prefix + '/' + \
                                os.path.basename(input_name)
                            volumes[str(short_input_item_path)] = {'bind': input_port_path, 'mode': 'ro'}
                    else:
                        input_port_path = str(short_input_item_path)
                    input_path[input_name] = input_port_path
                else:
                    if check_data_exist and not input_is_optional:
                        raise UserErrorException(
                            'Local input port path for "{}" does not exist, path: {}'.format(input_name,
                                                                                             input_item._dset))
            else:
                if not input_is_optional:
                    raise UserErrorException('Input port "{}" not set'.format(input_name))
        return input_path, volumes

    def generate_outputs(self, use_docker, check_data_exist=True, container_output_prefix=CONTAINER_OUTPUT_PATH):
        """
        If use_docker=True, generate output path and volumes of container, else generate output path in local.

        :param use_docker: Use docker.
        :type use_docker: bool
        :param check_data_exist: If check_data_exist=True, create output folder.
        :type check_data_exist: bool
        :param container_output_prefix: container output prefix
        :type container_output_prefix: str
        :return output_portname_container_path: Dict of output name and output path
                volumes: volumes of outputs
        :rtype Dict{(str, str)}, Dict{(str, Dict)}
        """
        volumes = {}
        output_portname_container_path = {}
        for output_port_name in self.component.outputs:
            if use_docker:
                output_port_path = container_output_prefix + '/' + output_port_name
            else:
                output_port_path = os.path.join(self.working_dir, OUTPUT_DIR_NAME, output_port_name)
            output_portname_container_path[output_port_name] = output_port_path
        output_path = Path(self.working_dir) / OUTPUT_DIR_NAME
        output_path.mkdir(parents=True, exist_ok=True)
        if check_data_exist:
            for output_port_name in self.component.outputs:
                if self.component._output_is_file(output_port_name):
                    (output_path / output_port_name).touch()
                else:
                    (output_path / output_port_name).mkdir(parents=True, exist_ok=True)
        volumes[str(output_path)] = {'bind': CONTAINER_OUTPUT_PATH, 'mode': 'rw'}
        return output_portname_container_path, volumes


def translate_mpi_command_by_component(command, component, os_type):
    """Translate command of mpi component."""
    # Get process_count_per_node param from run settings, will be 1 if did not find
    process_count_per_node = component._get_run_setting('process_count_per_node', int, 1)
    mpi_cmd = ['mpiexec', '-n', str(process_count_per_node)]

    if os_type.lower() == 'linux':
        # If executing in linux, will using root to execute mpi command, need to add --allow-run-as-root in command.
        mpi_cmd.append('--allow-run-as-root')
    command[0:0] = mpi_cmd

    node_count = component._get_run_setting('node_count', int, 1)
    if node_count > 1:
        from ..dsl._utils import logger as dsl_logger
        dsl_logger.warning('Ignore [ %s ] setting node_count = %s, '
                           'component.run only supports executing node on single node' % (component.name, node_count))

    return command


def translate_parallel_command_by_component(command, component, input_paths):
    """Translate key of input_paths from input argument name to input name."""
    command[1] = MOCK_PARALLEL_DRIVER
    port_arg_map = {}
    for input_arg_name, input_path in input_paths.items():
        input_name = component._get_input_name_by_argument_name(input_arg_name)
        port_arg_map[input_name] = input_path
    return translate_parallel_command(command, port_arg_map)


def translate_parallel_command(command, port_arg_map):
    # In parallel component, input value is input_name, and input param name starts with '--input_fds'.
    # This function will translate input name to input path.
    # https://msdata.visualstudio.com/Vienna/_git/AzureMlCli?path=%2Fsrc%2Fazureml-parallel-run%2Fazureml_sys%2Fazureml_sys%2Fparallel_run%2Fjob_args.py&version=GBmaster
    for index, item in enumerate(command):
        if item.startswith('--input_fds_') and index + 1 < len(command) and \
                command[index + 1] in port_arg_map:
            command[index + 1] = port_arg_map[command[index + 1]]
    return command


class ComponentRunInput:
    """Replace input dataset of component to local dataset path."""

    def __init__(self, component, working_dir, pipeline_parameters={},
                 input_futures=None, component_to_node_mapping={}):
        self.component = component
        self.working_dir = working_dir
        self.pipeline_parameters = pipeline_parameters
        self.component_to_node_mapping = component_to_node_mapping
        self.workspace = self.component.workspace
        self.input_futures = input_futures

    @track(_get_logger)
    def get_component_run_inputs_path(self):
        """
        Get input_path of component.

        :return inputs_path: Dict of inputs_path in Component
        :rtype Dict{(str, object)}
        """
        inputs_path = {}
        for input_name, input_value in self.component.inputs.items():
            inputs_path[input_name] = self._prepare_component_input(input_name, input_value._dset)
        return inputs_path

    def _prepare_component_input(self, input_name, dset):
        """
        Get component input path, if not exists in local will download it to working_dir.

        :param input_name: Input port name.
        :type input_name: str
        :param dset: Dataset
        :type dset: object
        :return inputs_path: input dataset path in local
        :rtype str
        """
        if self.input_futures and dset in self.input_futures:
            if not self.input_futures[dset].done():
                print_to_terminal('Download input dataset [ %s ] starting...\n' % input_name)
                print('%s: download input dataset [ %s ] starting...' % (RUN_PREPARE_LOG, input_name))
                self.input_futures[dset].result()
                print('%s: download input dataset [ %s ] completed...' % (RUN_PREPARE_LOG, input_name))
                print_to_terminal('Download input dataset [ %s ] completed...\n' % input_name)
            if Path(self.input_futures[dset].result()).exists():
                return self.input_futures[dset].result()
        # Download dataset and replace node inputs to local data path
        from ..component import Output, Input
        if isinstance(dset, Input):
            return self._prepare_component_input(input_name, dset._dset)
        if isinstance(dset, Output):
            return os.path.join(
                self.component_to_node_mapping[dset._owner._id][WORKING_DIR], OUTPUT_DIR_NAME, dset._name)
        elif isinstance(dset, DataReference) or isinstance(dset, FileDataset) or \
                isinstance(dset, DataPath) or isinstance(dset, DatasetConsumptionConfig) or \
                isinstance(dset, PipelineParameter):
            return ComponentRunInput.download_input_data(
                workspace=self.workspace, dset=dset, working_dir=self.working_dir,
                pipeline_parameters=self.pipeline_parameters)
        elif isinstance(dset, str) or not dset:
            return dset
        else:
            raise UserErrorException("Unknown type %s for node input dataset %s" % (type(dset), input_name))

    @staticmethod
    def download_input_data(workspace, dset, working_dir, pipeline_parameters=None, is_download=True):
        """
        Download input dataset to working_dir.

        :param workspace: The workspace object this input dataset will belong to.
        :type workspace: azureml.core.Workspace
        :param dset: Dataset
        :type dset: object
        :param working_dir: Folder to store dataset
        :type working_dir: dict
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict{(str, object)}
        :param is_download: If is_download is true, will download dataset to working_dir,
                            else only return dataset download path
        :type is_download: bool
        :return dataset_path: Download dataset path
        :rtype str
        """
        # Download component input dataset to local
        if isinstance(dset, PipelineParameter):
            default_value = dset.default_value if not pipeline_parameters or \
                (dset.name not in pipeline_parameters.keys()) else pipeline_parameters[dset.name]
            return ComponentRunInput.download_input_data(workspace, default_value, working_dir, pipeline_parameters)
        elif isinstance(dset, DataReference):
            data_store_name = dset.data_store_name
            path_on_data_store = dset.path_on_datastore
            blob_data_store = Datastore.get(workspace, data_store_name)
            target_path = Path(working_dir) / path_on_data_store
            if not is_download:
                return str(target_path)
            if target_path.exists():
                return str(target_path)
            blob_data_store.download(
                target_path=working_dir, prefix=path_on_data_store, overwrite=False)
            target_path.mkdir(exist_ok=True, parents=True)
            return str(target_path)
        elif isinstance(dset, FileDataset):
            dataset_id = dset.id
            dataset_name = dset.name
            target_path = Path(working_dir, dataset_name if dataset_name else dataset_id)
            if not is_download:
                return str(target_path)
            if target_path.exists():
                return str(target_path)
            dataset = Dataset.get_by_id(workspace, dataset_id)
            dataset.download(target_path=str(target_path), overwrite=False)
            return str(target_path)
        elif isinstance(dset, DataPath):
            path_on_data_store = dset._path_on_datastore
            target_path = Path(working_dir) / path_on_data_store
            if not is_download:
                return str(target_path)
            if target_path.exists():
                return str(target_path)
            dset._datastore.download(
                target_path=working_dir, prefix=path_on_data_store, overwrite=False)
            target_path.mkdir(exist_ok=True, parents=True)
            return str(target_path)
        elif isinstance(dset, DatasetConsumptionConfig):
            return ComponentRunInput.download_input_data(workspace, dset.dataset, working_dir, pipeline_parameters)
        elif isinstance(dset, str) or isinstance(dset, Path):
            # When generate command will check dset existence
            return dset
        else:
            raise UserErrorException('Input dataset is of unsupported type: {0}'.format(type(dset).__name__))


class ComponentRunParameter:

    def __init__(self, component, pipeline_parameters=None):
        self.component = component
        self.pipeline_parameters = pipeline_parameters

    @track(_get_logger)
    def get_component_run_parameters(self):
        """
        Get parameters of component.

        :return params_value: Dict of params in Component
        :rtype Dict{(str, object)}
        """
        params_value = {}
        for param_name, param_value in self.component._parameter_params.items():
            params_value[param_name] = self._get_component_parameter(param_name, param_value)
        return params_value

    def _get_component_parameter(self, param_name, param_value):
        """Get param value by param_name from component."""
        from ..component import Input
        if isinstance(param_value, PipelineParameter):
            return self._get_pipeline_param(param_name, param_value)
        elif isinstance(param_value, Input):
            return self._get_component_parameter(param_name, param_value._dset)
        else:
            return param_value

    def _get_pipeline_param(self, param_name, param_value):
        """Get param value from pipeline_params."""
        default_value = self.pipeline_parameters[param_value.name] if self.pipeline_parameters and \
            param_value.name in self.pipeline_parameters.keys() else param_value.default_value
        if isinstance(default_value, int) or isinstance(default_value, str) or \
                isinstance(default_value, bool) or isinstance(default_value, float):
            return default_value
        else:
            raise UserErrorException('Node parameter is of unsupported type: {0}'.format(type(default_value).__name__))
