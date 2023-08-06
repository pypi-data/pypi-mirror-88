# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import json
import re
import urllib.request
from pathlib import Path

from azureml.core import Experiment, Run, Dataset
from azureml.core.datastore import Datastore

from azure.ml.component._execution._component_snapshot import _download_snapshot, _extract_zip, \
    _mock_parallel_driver_file, MOCK_PARALLEL_DRIVER
from azure.ml.component._execution._command_execution_builder import translate_parallel_command
from azure.ml.component._restclients.service_caller import DesignerServiceCaller
from azure.ml.component._debug._constants import VSCODE_DIR, INPUT_DIR, LAUNCH_CONFIG, CONTAINER_DIR, \
    CONTAINER_CONFIG, SUBSCRIPTION_KEY, RESOURCE_GROUP_KEY, WORKSPACE_KEY, DEBUG_FOLDER, \
    DATA_REF_PREFIX, EXPERIMENT_KEY, RUN_KEY, ID_KEY
from azure.ml.component._debug._image import ImageBase
from azure.ml.component.dsl._utils import logger, _print_step_info
from azure.ml.component.dsl._constants import DATA_FOLDER


class DebugStepRunHelper:
    @staticmethod
    def installed_requirements():
        exc_map = {
            'docker': "https://www.docker.com/",
            'code': "https://code.visualstudio.com/Download"
        }
        _print_step_info(["Required {} can be installed here: {}".format(exc, url) for exc, url in exc_map.items()])

    @staticmethod
    def create_launch_config(step_name, python_path, commands, arguments):
        default_config = {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "console": "integratedTerminal",
        }
        if '-m' in commands:
            default_config['module'] = commands[-1]
        else:
            default_config['program'] = commands[-1]
        default_config['args'] = arguments
        default_config['pythonPath'] = python_path
        # create python debug config
        with open(INPUT_DIR / LAUNCH_CONFIG) as container_config:
            data = json.load(container_config)
            data['configurations'].append(default_config)
            os.makedirs(VSCODE_DIR, exist_ok=True)
            launch_config_path = os.path.join(VSCODE_DIR, LAUNCH_CONFIG)
            with open(launch_config_path, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        _print_step_info(f'Created launch config {launch_config_path} for step {step_name}')
        return launch_config_path

    @staticmethod
    def create_container_config(**kwargs):
        # create container config
        with open(INPUT_DIR / CONTAINER_CONFIG) as container_config:
            data = json.load(container_config)
            for key, val in kwargs.items():
                data[key] = val
            os.makedirs(CONTAINER_DIR, exist_ok=True)
            container_config_path = os.path.join(CONTAINER_DIR, CONTAINER_CONFIG)
            with open(container_config_path, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        return container_config_path


class DebugOnlineStepRunHelper(DebugStepRunHelper):
    @staticmethod
    def parse_designer_url(url):
        url = re.sub(r'^[^a-zA-Z]+', '', url)
        url = re.sub(r'[^a-zA-Z]+$', '', url)
        args = {}
        entries = re.split(r'[/&?]', url)
        try:
            for i, entry in enumerate(entries):
                if entry == EXPERIMENT_KEY:
                    if entries[i + 1] == ID_KEY:
                        args[EXPERIMENT_KEY] = entries[i + 2]
                    else:
                        args[EXPERIMENT_KEY] = entries[i + 1]
                elif entry in [RUN_KEY, WORKSPACE_KEY, RESOURCE_GROUP_KEY, SUBSCRIPTION_KEY]:
                    args[entry] = entries[i + 1]
            return args[RUN_KEY], args[EXPERIMENT_KEY], args[WORKSPACE_KEY], args[RESOURCE_GROUP_KEY], args[
                SUBSCRIPTION_KEY]
        except BaseException as e:
            raise ValueError(f'Failed to parse portal url: {url}') from e

    @staticmethod
    def get_pipeline_run(run_id, experiment_name, workspace):
        experiments = [experiment for experiment in Experiment.list(workspace) if
                       experiment.id == experiment_name or experiment.name == experiment_name]
        assert len(experiments) > 0, "Experiment %s not found" % experiment_name
        experiment = experiments[0]

        pipeline_run = Run(experiment, run_id)

        _print_step_info(
            f'Workspace: {workspace.name} Experiment: {experiment_name} StepRun: {run_id}')

        return pipeline_run

    @staticmethod
    def get_image_id(step_name, details):
        if 'properties' not in details:
            raise RuntimeError(f'{step_name} does not have properties')
        properties = details['properties']
        if 'AzureML.DerivedImageName' in properties:
            return properties['AzureML.DerivedImageName']
        else:
            for log_file, url in details['logFiles'].items():
                if 'azureml-execution' in log_file:
                    content = urllib.request.urlopen(url).read()
                    m = re.findall(r'latest: Pulling from (azureml/azureml_[^\\n]+)', str(content))
                    if len(m) > 0:
                        return m[0]
                    m = re.findall(r'Start to pulling docker image: [^/]+/(azureml/azureml_[^\\n]+)', str(content))
                    if len(m) > 0:
                        return m[0]
            raise RuntimeError(f'{step_name} does not have valid logs with image pattern azureml/azureml_[^\\n]')

    @staticmethod
    def prepare_dev_container(workspace, step, dry_run=False) -> ImageBase:
        # prepare image
        try:
            environment = step.get_environment()
        except Exception as e:
            original_error_message = f'{e.__class__.__name__}: {e}'
            raise RuntimeError('Failed to get environment details from step run details, '
                               'please make sure this step run has started successfully.\n'
                               f'Original error: {original_error_message}') from e
        image_details = environment.get_image_details(workspace)
        step_run_image = ImageBase(image_details, environment, workspace)

        if dry_run:
            # Won't pull image for dry run,
            # but still need to visit EMS to make sure that image exists and write a config.
            image_name = step_run_image.register_image_name
        else:
            _print_step_info('Preparing image.')
            image_name = step_run_image.get_component_image()
            _print_step_info(f'Prepared image {step_run_image.image_name}')

        # create container config
        data = {'image': image_name}
        DebugOnlineStepRunHelper.create_container_config(**data)
        return step_run_image

    @staticmethod
    def download_snapshot(service_caller: DesignerServiceCaller, step_run: Run, component_type: str, dry_run=False):
        if dry_run:
            return True
        snapshot_path = os.getcwd()
        try:
            # TODO: move service caller to debugger and use run detail as param
            step_run_id = step_run.parent.id
            run_id = step_run.id
            run_details = service_caller.get_pipeline_run_step_details(run_id, step_run_id, include_snaptshot=True)
            snapshot_url = run_details.snapshot_info.root_download_url
            _download_snapshot(snapshot_url, snapshot_path)
            if component_type and component_type.lower() == 'parallel':
                _mock_parallel_driver_file(os.path.join(snapshot_path, DEBUG_FOLDER))
        except BaseException as e:
            logger.warning(
                f'Failed to download snapshot via SMT, fall back to user azureml core API. Error message: {e}')
            try:
                # Failed to download via SMT, try to download via azureml core API
                zip_path = step_run.restore_snapshot(path=snapshot_path)
                _extract_zip(zip_path, snapshot_path)
            except BaseException:
                return False
        _print_step_info(f'Downloaded snapshot {snapshot_path}')
        return True

    @staticmethod
    def prepare_inputs(workspace, details, dry_run=False):
        if 'runDefinition' not in details:
            raise RuntimeError('Failed to get runDefinition from step run details, '
                               'please make sure this step run has started successfully.')
        port_arg_map = {}
        result = True
        # data reference
        data_references = details['runDefinition']['dataReferences']
        for data_reference_name, data_store in data_references.items():
            data_store_name = data_store['dataStoreName']
            path_on_data_store = data_store['pathOnDataStore']
            # TODO: handle special characters in data path(could not run inside container in VS Code)
            port_arg_map[data_reference_name] = path_on_data_store
            if not dry_run:
                download_result = DebugOnlineStepRunHelper.download_data_reference(workspace, data_store_name,
                                                                                   path_on_data_store)
                result = result and download_result

        # dataset
        dataset = details['runDefinition']['data']
        for dataset_name, data in dataset.items():
            dataset_id = data['dataLocation']['dataset']['id']
            if not dry_run:
                download_result = DebugOnlineStepRunHelper.download_dataset(workspace, dataset_id)
                result = result and download_result
            port_arg_map[dataset_name] = dataset_id
        _print_step_info(f'Downloaded data: {port_arg_map}')

        return port_arg_map, result

    @staticmethod
    def download_data_reference(workspace, data_store_name, path_on_data_store) -> bool:
        data_path = Path(DATA_FOLDER)
        try:
            blob_data_store = Datastore.get(workspace, data_store_name)
            blob_data_store.download(target_path=str(data_path), prefix=path_on_data_store, overwrite=False)
            # output directory might be empty
            if not Path(data_path / path_on_data_store).exists():
                os.makedirs(data_path / path_on_data_store)
            return True
        except Exception as e:
            logger.warning('Could not download dataset {} due to error {}'.format(path_on_data_store, e))
            return False

    @staticmethod
    def download_dataset(workspace, dataset_id) -> bool:
        data_path = Path(DATA_FOLDER)
        try:
            dataset = Dataset.get_by_id(workspace, dataset_id)
            target_path = str(data_path / dataset_id)
            dataset.download(target_path=target_path, overwrite=True)
            return True
        except Exception as e:
            logger.warning('Could not download dataset {} due to error {}'.format(dataset_id, e))
            return False

    @staticmethod
    def prepare_arguments(step_name, details, port_arg_map, component_type):
        if 'runDefinition' not in details:
            raise RuntimeError('Failed to get runDefinition from step run details, '
                               'please make sure this step run has started successfully.')
        run_definition = details['runDefinition']
        arguments = run_definition['arguments']
        environment_vars = run_definition['environment']['environmentVariables']
        environment_vars = {f'${key}': environment_vars[key] for key in environment_vars}
        data_path = Path(DATA_FOLDER)
        for data_reference_name, port_dir in port_arg_map.items():
            data_reference_constant = DATA_REF_PREFIX + data_reference_name
            data_reference_path = (data_path / port_dir).as_posix()
            environment_vars[data_reference_constant] = data_reference_path
            port_arg_map[data_reference_name] = data_reference_path

        parsed_arguments = []
        for arg in arguments:
            for env_var, env_var_val in environment_vars.items():
                arg = arg.replace(env_var, env_var_val)
            parsed_arguments.append(arg)

        _print_step_info(f'Prepared arguments: {parsed_arguments} for step {step_name}')
        run_definition = details['runDefinition']
        if component_type.lower() == 'parallel':
            script = f'{DEBUG_FOLDER}/{MOCK_PARALLEL_DRIVER}'
            parsed_arguments = translate_parallel_command(parsed_arguments, port_arg_map)
        else:
            script = run_definition['script']
        return script, parsed_arguments
