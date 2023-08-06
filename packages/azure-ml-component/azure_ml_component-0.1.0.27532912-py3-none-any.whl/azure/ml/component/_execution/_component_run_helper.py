# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import copy
import json
import traceback
import concurrent
import tempfile
import subprocess
from threading import currentThread, main_thread, Thread
from pathlib import Path
from datetime import datetime

from azure.ml.component._util._loggerfactory import _LoggerFactory, track
from azureml.exceptions._azureml_exception import UserErrorException
from azureml.exceptions import ActivityFailedException
from ._component_run_logger import Logger
from ._command_execution_builder import ComponentRunInput, CommandExecutionBuilder, \
    OUTPUT_DIR_NAME, ComponentRunParameter
from ._component_snapshot import _prepare_component_snapshot
from ._constants import IMAGE_DIR_NAME, SCRIPTE_DIR_NAME, EXECUTION_LOGFILE, MODULE_PROPERTY_NAME, RUN_STATUS,\
    STATUS_CODE, PARENT_NODE_ID, NODE_LOG_KEY, PARENT_LOG_KEY, RUN_PREPARE_LOG, RUN_EXEC_LOG, \
    STEP_STATUS, CONDA_DIR_NAME, USER_ERROR_MSG, PREPAREING, RUNNING, COMPLETED, FAILED


_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class ComponentRunHelper:
    input_futures = {}
    env_futures = {}
    _executor = concurrent.futures.ThreadPoolExecutor()

    def __init__(self, component, working_dir, tracker, use_docker=True, show_output=True,
                 visualizer=None, node_id=None, component_to_node_mapping={}, pipeline_parameters=None):
        """
        Init ComponentRunHelper and logger.

        :param component: Executed component
        :type component: azure.ml.component.Component
        :param working_dir: component data and snapshot store path
        :type working_dir: str
        ::param use_docker: If use_docker=True, will pull image from azure and run component in container.
                            If use_docker=False, will directly run component script.
        :type use_docker: bool
        :param tracker: Used for tracking run history.
        :type tracker: RunHistoryTracker
        :param node_id: Node id of component
        :type node_id: str
        :param visualizer: To show pipeline graph in notebook
        :type visualizer: azure.ml.component._widgets._visualize
        :param show_output: Indicates whether to show the pipeline run status on sys.stdout.
        :type show_output: bool
        :param component_to_node_mapping: Mapping of component to node info
        :type component_to_node_mapping: dict{(str, dict)}
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict{(str, object)}
        """
        self.component = component
        Path(working_dir).mkdir(parents=True, exist_ok=True)
        self.working_dir = working_dir
        self.tracker = tracker
        self.logger = Logger(log_path=os.path.join(self.working_dir, EXECUTION_LOGFILE), tracker=tracker)
        self.run_history_log_path = self.logger.get_log_path()
        self.use_docker = use_docker
        self.show_output = show_output
        self.visualizer = visualizer
        self.node_id = node_id
        self.pipeline_parameters = pipeline_parameters
        self.component_to_node_mapping = component_to_node_mapping
        self.tasks = []
        self.component_status = STEP_STATUS.copy()
        self.snapshot_path = os.path.join(self.working_dir, SCRIPTE_DIR_NAME)

    @classmethod
    def download_datasets(cls, datasource, workspace, working_dir, pipeline_parameters=None):
        """
        Add download dataset task in ComponentRunHelper.input_futures.
        And key of input_futures is dataset path in local.

        :param datasource: Input datasets of component
        :type datasource: list
        ::param workspace: The workspace object this dataset will belong to.
        :type workspace: azure.ml.core.Workspace
        :param working_dir: component data store path.
        :type working_dir: str
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict{(str, object)}
        :return: Dict of download input futures
        :rtype: dict{(str, future)}
        """
        dataset_path_futures = {}
        for item in datasource:
            if not isinstance(item, str):
                dataset_path = ComponentRunInput.download_input_data(
                    workspace, item, working_dir, pipeline_parameters, is_download=False)
                if dataset_path not in dataset_path_futures:
                    dataset_path_futures[dataset_path] = \
                        cls._executor.submit(ComponentRunInput.download_input_data, workspace, item,
                                             working_dir, pipeline_parameters)
                cls.input_futures[item] = dataset_path_futures[dataset_path]
        return cls.input_futures

    @classmethod
    def prepare_component_env(cls, component, working_dir, use_docker=True):
        """
        Prepare component execution environment. If use_docker is true, will get component image in local.
        If use_docker=False, will create component conda environment.

        :param component: Component to get environment.
        :type component: azure.ml.component.Component
        :param working_dir: Working dir to store getting environment logs.
        :type working_dir: str
        :return: Dict of get component environment futures
        :rtype: dict{(str, future)}
        """
        if use_docker:
            from azure.ml.component._debug._image import ComponentImage
            component_image = ComponentImage(component, os.path.join(working_dir, IMAGE_DIR_NAME))
            image_name = component_image.image_details['dockerImage']['name']
            if image_name not in cls.env_futures:
                cls.env_futures[image_name] = cls._executor.submit(component_image.get_component_image)
        else:
            component_conda = ComponentCondaEnvironment(component, os.path.join(working_dir, CONDA_DIR_NAME))
            if component_conda.conda_environment_name not in cls.env_futures:
                cls.env_futures[component_conda.conda_environment_name] = \
                    cls._executor.submit(component_conda.build_local)
        return cls.env_futures

    def _add_new_thread_task(self, target, args):
        """
        Create component run child thread which recode parent thread id.
        """
        thread = ThreadWithParent(target=target, args=args)
        self.tasks.append(thread)
        thread.start()
        return thread

    def _update_visualizer(self, current_status):
        """
        Update component status in visualizer

        :param current_status: Component current status.
        :type current_status: str
        """
        self.component_status = update_component_status(
            current_status, self.component_status, run_details_url=self.tracker.get_run_details_url())
        self.pipeline_status.update({self.node_id: self.component_status})
        update_pipeline_in_visualizer(self.visualizer, self.node_id, self.pipeline_status, self.run_history_log_path)

    @track(_get_logger)
    def _prepare_component(self):
        """
        Prepare component run, will download snapshot and regenerate component by replacing params and inputs.
        """
        # Prepare snapshot
        get_component_snapshot_task = ThreadWithParent(
            target=_prepare_component_snapshot, args=(self.component, self.snapshot_path))
        get_component_snapshot_task.start()

        # Prepare component inputs
        component_inputs = ComponentRunInput(self.component, self.working_dir,
                                             self.pipeline_parameters, self.input_futures,
                                             self.component_to_node_mapping).get_component_run_inputs_path()
        # Prepare component parameter
        component_params = ComponentRunParameter(self.component,
                                                 self.pipeline_parameters).get_component_run_parameters()

        # Copy component replace params and inputs
        component = copy.copy(self.component)
        component._replace_inputs(**component_inputs)
        component._replace_parameters(**component_params)

        self._add_new_thread_task(
            target=self.tracker.add_properties,
            args=({MODULE_PROPERTY_NAME: component._identifier},))

        get_component_snapshot_task.join()
        return component

    @track(_get_logger)
    def _get_component_environment(self, python_interpreter_path=None):
        """
        Get component environment

        :param python_interpreter_path: python interpreter path in local
        :type python_interpreter_path: str
        :return: component_environment: Component environment info
                 env_log_path: Component environment log path
        :rtype: azure.ml.component._execution._component_run_helper.ComponentEnvironment, str
        """
        env_log_path = None
        if self.use_docker:
            # build image
            from azure.ml.component._debug._image import ComponentImage
            env_log_path = os.path.join(self.working_dir, IMAGE_DIR_NAME)
            component_environment = ComponentImage(self.component, env_log_path)
        elif python_interpreter_path:
            # use python interpreter path
            component_environment = ComponentEnvironment(self.component)
            component_environment.python_path = python_interpreter_path
        else:
            # build conda environment
            env_log_path = os.path.join(self.working_dir, CONDA_DIR_NAME)
            component_environment = ComponentCondaEnvironment(self.component, env_log_path)
        return component_environment, env_log_path

    @track(_get_logger)
    def _build_component_environment_in_local(self, component_environment):
        """
        Build component environment in local

        :param component_environment: Environment info that need to be built in local.
        :type component_environment: azure.ml.component._execution._component_run_helper.ComponentEnvironment
        """
        if self.use_docker:
            env_name = component_environment.register_image_name
            env_type = 'docker image'
        else:
            env_name = component_environment.conda_environment_name
            env_type = 'conda environment'
        print('%s: get [ %s ] %s %s starting...' % (RUN_PREPARE_LOG, self.component.name, env_type, env_name))
        if self.env_futures and env_name in self.env_futures:
            task_result = self.env_futures[env_name].result()
            if not component_environment.check_environment_exists():
                # Check component env exists, if not start building environment.
                build_future = self._executor.submit(component_environment.build_local)
                task_result = build_future.result()
        else:
            build_future = self._executor.submit(component_environment.build_local)
            task_result = build_future.result()
        if component_environment.register_image_name:
            component_environment.image_name = task_result
        else:
            component_environment.python_path = task_result
        print('%s: get [ %s ] %s %s completed...' % (RUN_PREPARE_LOG, self.component.name, env_type, env_name))

    @track(_get_logger)
    def _handle_component_run_result(self, component_run_success, use_docker,
                                     command_execution, python_path, env_log_path):
        component_run_status = COMPLETED if component_run_success else FAILED
        print('%s: finish running component [ %s ], status is %s...' % (
            RUN_EXEC_LOG, self.component.name, component_run_status))
        if not component_run_success:
            working_dir = Path(self.working_dir).absolute()
            print('Diagnostic your failed run here:\n'
                  '\tworking dir: %s\n'
                  '\texecution log: %s\n'
                  '\toutput dir: %s' % (
                      str(working_dir), self.logger.get_log_path(), str(working_dir / OUTPUT_DIR_NAME)))

        # Upload component outputs and log file to portal
        self._add_new_thread_task(target=self.tracker.upload_snapshot, args=(self.snapshot_path,))
        self._add_new_thread_task(target=self.tracker.upload_run_output, args=(self.component, self.working_dir))
        self._add_new_thread_task(target=self.tracker.update_run_result_status, args=(component_run_success,))
        if env_log_path and Path(env_log_path).exists():
            self._add_new_thread_task(target=self.tracker.upload_folder, args=(env_log_path,))

        self._update_visualizer(component_run_status)

        if use_docker and not component_run_success and command_execution:
            _prepare_debug_config_for_component(self.component, command_execution, self.snapshot_path, python_path)
        return component_run_status

    @track(_get_logger)
    def component_run(self, python_interpreter_path=None, raise_on_error=True, pipeline_status={}):
        """
        component_run will run component in local environment/container. In prepare state, will download component
        snapshots and input dataset, generate component execute command and pull component image. Then will execute
        command in local environment/container.

        :param python_interpreter_path: When use_docker=False and python_interpreter_path not None, will use
                                        python_interpreter_path to run steps.
        :type python_interpreter_path: str
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool
        :return: Component run status
        :rtype: str
        """
        self.pipeline_status = pipeline_status
        is_main_thread = currentThread() is main_thread()
        self.logger.set_show_terminal(self.show_output and is_main_thread)
        env_log_path = None
        with self.logger:
            try:
                self.tracker.print_run_info()
                self._update_visualizer(PREPAREING)
                # Prepare component run
                component = self._prepare_component()
                command_execution = None
                # Get and build component environment in local
                component_environment, env_log_path = self._get_component_environment(python_interpreter_path)
                if self.use_docker or not python_interpreter_path:
                    self._build_component_environment_in_local(component_environment)
                command_execution = CommandExecutionBuilder(component=component,
                                                            snapshot_path=self.snapshot_path,
                                                            working_dir=self.working_dir,
                                                            tracker=self.tracker,
                                                            logger=self.logger,
                                                            component_env=component_environment).build()

                # Start executing component script
                print('%s: prepare to call script [ %s ] with command %s.' % (
                    RUN_EXEC_LOG, self.component._module_dto.entry, command_execution.command))
                print('%s: run component [ %s ] starting....' % (RUN_EXEC_LOG, self.component.name))
                self._update_visualizer(RUNNING)
                print('%s: component execution log starting\n' % (RUN_EXEC_LOG))
                # Execute component script
                if self.use_docker:
                    component_run_success = command_execution.execute_command_in_container()
                else:
                    component_run_success = command_execution.execute_command_in_local()
                # print a blank line to distinguish user code log and component log.
                print()
                print('%s: component execution log completed.' % (RUN_EXEC_LOG))
                if not component_run_success:
                    # Raise error in user scirpt.
                    error_detail = {
                        'error': {'code': 'UserError', 'message': USER_ERROR_MSG % self.logger.get_log_path()},
                        'time': str(datetime.now())
                    }
                    raise ActivityFailedException(error_details=json.dumps(error_detail, indent=4))
            except Exception as ex:
                if not isinstance(ex, ActivityFailedException):
                    # Record component run error message in log file.
                    traceback.print_exc()
                self._update_visualizer(FAILED)
                component_run_success = False
                if raise_on_error:
                    raise ex
            finally:
                component_run_status = self._handle_component_run_result(
                    component_run_success, self.use_docker, command_execution,
                    component_environment.python_path if component_environment else None, env_log_path)
                for task in self.tasks:
                    task.join()
                if self.show_output and not is_main_thread:
                    self.logger.print_logfile()

        return component_run_status


def update_pipeline_in_visualizer(visualizer, node_id, status, log_url=None):
    """
    Update pipeline status and node log_url in visualizer.

    :param node_id: node_id of component in pipeline.
    :type node_id: str
    :param status: Pipeline current status.
    :type status: dict{(str, str)}
    :param log_url: Component run log url.
    :type log_url: str
    """
    if not visualizer or not node_id:
        return
    visualizer.send_message(message='status', content=status)
    if log_url:
        if node_id != PARENT_NODE_ID:
            visualizer.send_message(message='logs', content={node_id: {NODE_LOG_KEY: log_url}})
        else:
            visualizer.send_message(message='logs', content={node_id: {PARENT_LOG_KEY: log_url}})


def update_component_status(component_status, status=None, run_details_url=None):
    """
    Update component run status.

    :param component_status: Component current status.
    :type component_status: str
    :param status: Previous component run status info.
    :type status: dict{(str, str)}
    :param run_details_url: Component run detail url.
    :type run_details_url: str
    :return: Component run status info.
    :rtype: str
    """
    if not status:
        status = copy.deepcopy(STEP_STATUS)
    if not run_details_url:
        status['runDetailsUrl'] = run_details_url

    status['status'] = STATUS_CODE[component_status]
    status['statusCode'] = STATUS_CODE[component_status]
    status['runStatus'] = RUN_STATUS[component_status]

    if component_status == RUNNING and not status['startTime']:
        status['startTime'] = datetime.now().isoformat()
    elif component_status == COMPLETED or component_status == FAILED:
        status['endTime'] = datetime.now().isoformat()
    return status


def _prepare_debug_config_for_component(component, command_execution, snapshot_path, python_path):
    """
    Generate launch and container config files for debugging component in snapshot_path.

    :param component: Component to debug.
    :type component: azure.ml.component.Component
    :param command_execution: Component execution info.
    :type command_execution: azure.ml.component._execution.CommandExecution
    :param snapshot_path: Component snapshot path.
    :type snapshot_path: str
    :param python_path: Python interpreter path in container.
    :type python_path: str
    """
    from azure.ml.component._debug._component_debug_helper import DebugLocalComponentHelper
    mount_val = "source={},target={},type=bind,consistency=cached"
    mounts = [mount_val.format(key, value['bind'])for key, value in command_execution.volumes.items()]
    DebugLocalComponentHelper.prepare_dev_container(command_execution.image_name,
                                                    name=component.name,
                                                    containerEnv=command_execution.environment,
                                                    mounts=mounts,
                                                    target=snapshot_path)
    DebugLocalComponentHelper.create_launch_config(component._module_dto.entry[:-3],
                                                   command_execution.command,
                                                   snapshot_path,
                                                   component.type)
    from azure.ml.component.dsl._utils import _print_step_info
    _print_step_info([
        'Component run failed, you can debug component in vscode by steps:',
        '1. Pressing F1, click "Remote-Containers: Reopen in Container".',
        '2. In Status Bar, selecting python interpreter path "%s"' % python_path,
        "3. Pressing F5 to start debugging."])


class ThreadWithParent(Thread):

    def __init__(self, *args, **kwargs):
        self.parent = currentThread()
        Thread.__init__(self, *args, **kwargs)


class ComponentEnvironment(object):
    def __init__(self, component):
        self.component = component
        self.env = component._get_environment()
        self.conda_environment_name = None
        self.python_path = None
        # register_image_name is the name of image registered in ACR
        self.register_image_name = None
        # image_name is stand for name of image in local.
        self.image_name = None
        self.os_type = None

    def build_local(self):
        pass

    def check_environment_exists(self):
        pass


class ComponentCondaEnvironment(ComponentEnvironment):
    def __init__(self, component, log_dir=None):
        super(ComponentCondaEnvironment, self).__init__(component)
        if self.env.python.user_managed_dependencies:
            raise UserErrorException(
                'Cannot initialize component conda since the conda of the component is not specified.')
        self.conda_environment_name = self.env.python.conda_dependencies._conda_dependencies['name']
        if not log_dir:
            log_dir = tempfile.gettempdir()
        self.log_path = os.path.join(log_dir, self.conda_environment_name + '.txt')
        self.os_type = 'windows' if os.name == 'nt' else 'linux'

    def _get_conda_environment_path(self):
        """Execute command 'conda env list' to get conda environment path."""
        try:
            # Before python3.7, because _winapi.CreateProcess used by subprocess is not thread-safe,
            # it may cause ValueError: embedded null character. This error does not occur when passing args as a list.
            # https://bugs.python.org/issue31446
            conda_version_output = subprocess.check_output(['conda', 'env', 'list'], stderr=subprocess.STDOUT)
            result = conda_version_output.decode("UTF-8")
            for line in result.split(os.linesep):
                if self.conda_environment_name in line:
                    return os.path.join(line.split(' ')[-1], 'python' if os.name == 'nt' else 'bin/python')
        except Exception as e:
            raise UserErrorException('Get conda environment list error, {}.'.format(str(e)))

    @track(_get_logger)
    def build_local(self):
        """Build conda environment in local and return conda environment path."""
        with Logger(log_path=self.log_path) as logger:
            try:
                logger.print_to_terminal(
                    'Start building [ %s ] conda environment: %s\n' % (
                        self.component.name, self.conda_environment_name))
                self.env.build_local(self.component.workspace, useDocker=False)
                self.python_path = self._get_conda_environment_path()
            except:
                raise UserErrorException('Build local conda environment failed, build log: {}.'.format(self.log_path))
            finally:
                logger.print_to_terminal(
                    'Finish building [ %s ] conda environment: %s\n' % (
                        self.component.name, self.conda_environment_name))
            if not self.python_path:
                # In azureml-environment-setup, using environment_path and environment_indicator to check environment
                # existence, and not the validity of environment_path's contents. When user remove environment built
                # by azureml and not completely deleted environment_path, azureml-environment-setup will mistakenly
                # believe environment exists and not build in local.
                raise UserErrorException(
                    'Cannot found {} in conda environment list.'.format(self.conda_environment_name))
        return self.python_path

    def check_environment_exists(self):
        """Check conda exists in local environment."""
        if self._get_conda_environment_path():
            return True
        else:
            return False
