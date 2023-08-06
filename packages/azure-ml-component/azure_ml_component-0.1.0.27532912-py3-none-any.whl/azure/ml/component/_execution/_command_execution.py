# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import subprocess
import tarfile
import traceback
import docker

from azureml._model_management._util import write_dir_in_container
from azureml._model_management._util import write_file_in_container
from azureml._model_management._util import get_docker_client
from .._util._loggerfactory import _LoggerFactory, track
from ._constants import CONTAINER_OUTPUT_PATH

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class CommandExecution:
    """Execute command in local or container."""
    def __init__(self, command, environment, cwd, logger, volumes=None, image_name=None):
        """
        :param command: execute command in container
        :type command: list
        :param environment: the environment variables for execute command
        :type environment: dict
        :param cwd: current directory when execute command
        :type cwd: str
        :param logger: log container output
        :type logger: azure.ml.component._execution._component_run_logger.Logger
        :param image_name: image name
        :type image_name: str
        :param volumes: volumes need to mount in container
        :type volumes: dict
        """
        self.command = command
        self.environment = environment
        self.cwd = cwd
        self.logger = logger
        self.volumes = volumes
        self.image_name = image_name

    @track(_get_logger)
    def execute_command_in_local(self):
        """
        Execute command in subprocess and streaming log output in logger.

        :return command_result: is command execute success
        :rtype bool
        """
        environment = dict(list(self.environment.items()) + list(os.environ.items()))
        process = subprocess.Popen(
            self.command, env=environment, cwd=self.cwd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, encoding='utf-8')
        # Because stdout.readline will hang up to wait for output, needn't to sleep in loop.
        for line in iter(process.stdout.readline, ''):
            self.logger.write_message(line)
        # Wait for process to terminate
        returncode = process.wait()
        return returncode == 0

    @track(_get_logger)
    def execute_command_in_container(self):
        """
        Execute command in container and streaming log container output to logger.

        :return command_result: is command execute success
        :rtype bool
        """
        # Set PYTHONUNBUFFERED=1 to force the stdout and stderr streams to be unbuffered.
        environment = dict(list(self.environment.items()) + list({'PYTHONUNBUFFERED': 1}.items()))
        docker_client = get_docker_client()
        is_wsl_or_container = _is_in_container() or _is_in_wsl1()
        if is_wsl_or_container:
            container = docker_client.containers.create(
                self.image_name, working_dir=self.cwd, environment=environment,
                stdin_open=True, privileged=True, tty=True)
        else:
            container = docker_client.containers.create(
                self.image_name, working_dir=self.cwd, environment=environment,
                volumes=self.volumes, stdin_open=True, privileged=True, tty=True)
        try:
            container.start()
            if is_wsl_or_container:
                command_result = _exec_command_in_wsl1_container(container, self.command, self.volumes, self.logger)
            else:
                command_result = _container_exec_run(container, self.command, self.logger)
            container.stop()
            if command_result == 0:
                container.remove()
        except Exception:
            traceback.print_exc()
            return False
        return command_result == 0


def _copy_from_docker(container, source, target):
    """
    Copy folder from container to local.

    :param container: execute command in container
    :type container: docker.container
    :param source: folder path in container.
    :type source: str
    :param target: target path
    :type target: str
    """
    try:
        data_stream, _ = container.get_archive(source)
        tar_file = target + '.tar'
        with open(tar_file, 'wb') as f:
            for chunk in data_stream:
                f.write(chunk)
        with tarfile.open(tar_file, mode='r') as tar:
            for file_name in tar.getnames():
                tar.extract(file_name, os.path.dirname(target))
    except Exception as e:
        raise RuntimeError(e)
    finally:
        os.remove(tar_file)


def _is_in_container():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )


def _is_in_wsl1():
    process = subprocess.run(["systemd-detect-virt", "-c"], shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
    return 'wsl' in process.stdout


def _exec_command_in_wsl1_container(container, command, volumes, logger):
    """
    In WSL1 and container, will execute docker command in host machine, so folder in WSL1/container
    cannot mount in docker container. Using docker cp to replace mounting.

    :param container: container
    :type container: docker.container
    :param command: execute command in container
    :type command: list
    :param volumes: volumes need to mount in container
    :type volumes: dict
    :param logger: log container output
    :type logger: azure.ml.component._execution._component_run_logger.Logger
    :return command_result: command run result, if not 0, may some error when execute
            stdout: log of executing command
    :rtype int, bytes
    """
    print('Warning: Running in WSL1 or container')
    # copy code and data to container
    for key, item in volumes.items():
        if not os.path.exists(key):
            continue
        if os.path.isdir(key):
            write_dir_in_container(container, item['bind'], key)
        else:
            with open(key, 'rb') as f:
                write_file_in_container(container, item['bind'], f.read())

    # execute command
    command_result = _container_exec_run(container, command, logger=logger)

    # copy reuslt to local
    for key, item in volumes.items():
        if item['bind'].startswith(CONTAINER_OUTPUT_PATH):
            _copy_from_docker(container, item['bind'], key)
    return command_result


def _container_exec_run(container, command, logger):
    """
    Create and start a container execution

    :param container: container
    :type container: docker.container
    :param command: execute command in container
    :type command: list
    :param logger: log container output
    :type logger: azure.ml.component._execution._component_run_logger.Logger
    :return command_result: command run result, if not 0, may some error when execute
    :rtype int
    """
    container_exec = docker.APIClient().exec_create(container.id, command)
    exec_output = docker.APIClient().exec_start(container_exec['Id'], stream=True)

    for line in exec_output:
        line = line.decode('utf-8')
        logger.write_message(line)
    # Get command exit code in container
    container_inspect = docker.APIClient().exec_inspect(container_exec['Id'])
    command_result = container_inspect['ExitCode']
    return command_result
