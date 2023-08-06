# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
import re
import os
import sys

from functools import wraps
from pathlib import Path

from azureml.core import Workspace
from azureml.exceptions import UserErrorException
from azure.ml.component._debug._constants import DIR_PATTERN
from azure.ml.component._debug._step_run_debug_helper import DebugOnlineStepRunHelper, _print_step_info, logger
from azure.ml.component.dsl._pipeline_project import _get_telemetry_logger
from azure.ml.component.dsl._utils import _change_working_dir, _str_to_bool
from azure.ml.component._execution._component_run_helper import MODULE_PROPERTY_NAME
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._util._loggerfactory import track, _PUBLIC_API, _LoggerFactory
from azure.ml.component._util._telemetry import WorkspaceTelemetryMixin


class DebugRunner:
    def __init__(self, target=None):
        if target is None:
            target = os.getcwd()
        self.target = target
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.step_run = None
        self.step_detail = None
        self.python_path = None

    def run(self):
        pass

    def run_step(self, func):
        # run all steps passed in failed_steps
        @wraps(func)
        def wrapper():
            # Hint to install requirements
            DebugOnlineStepRunHelper.installed_requirements()

            func()

        return wrapper

    @staticmethod
    def hint_to_reopen_in_container(target):
        _print_step_info(f'Please open the generated folder {target} in Vs Code, and reopen in Container '
                         'to start debugging. See detail doc here: https://aka.ms/azureml-component-debug')


class OnlineStepRunDebugger(DebugRunner, WorkspaceTelemetryMixin):
    def __init__(self,
                 url=None,
                 run_id=None,
                 experiment_name=None,
                 workspace_name=None,
                 resource_group_name=None,
                 subscription_id=None,
                 target=None,
                 dry_run=False):
        DebugRunner.__init__(self, target=target)
        if url is not None:
            run_id, experiment_name, workspace_name, resource_group_name, subscription_id = \
                DebugOnlineStepRunHelper.parse_designer_url(url)
        if all(var is not None for var in
               [run_id, experiment_name, workspace_name, resource_group_name, subscription_id]):
            self.run_id = run_id
            self.experiment_name = experiment_name
            self.workspace_name = workspace_name
            self.resource_group_name = resource_group_name
            self.subscription_id = subscription_id
            self.dry_run = dry_run
            self.step_run = None
            self.step_detail = None
            self.service_caller = None
            self.step_id = None
        else:
            raise UserErrorException(
                'One of url or step run params(run_id, experiment_name, '
                'workspace_name, resource_group_name, subscription_id) should be passed.')
        try:
            self.workspace = Workspace(subscription_id=self.subscription_id, resource_group=self.resource_group_name,
                                       workspace_name=self.workspace_name)
        except BaseException as e:
            raise UserErrorException(f'Failed to get workspace due to error: {e}')

        # init ws mixin after workspace initialized
        WorkspaceTelemetryMixin.__init__(self, workspace=self.workspace)

        # manually call decorator passing self to decorator
        self.run = self.run_step(self.remote_setup)

    @track(_get_telemetry_logger, activity_name="OnlineStepRunDebugger_debug", activity_type=_PUBLIC_API)
    def remote_setup(self):
        # won't pull image and download data for test
        if '_TEST_ENV' in os.environ:
            logger.warning("Envrionment variable _TEST_ENV is set, won't pull image and download data.")
            self.dry_run = True
        _print_step_info('Fetching pipeline step run metadata')
        self.step_run = DebugOnlineStepRunHelper.get_pipeline_run(self.run_id, self.experiment_name,
                                                                  self.workspace)
        self.step_detail = self.step_run.get_details()
        step_id = '%s:%s' % (self.step_run.name, self.step_run.id)
        step_id = re.sub(DIR_PATTERN, '_', step_id)
        self.step_id = step_id
        # This API are only called from CLI currently.
        self.service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace, from_cli=True)

        if MODULE_PROPERTY_NAME not in self.step_detail['properties']:
            # TODO: rename to component when module is deprecated.
            logger.warning(f'Can not find "{MODULE_PROPERTY_NAME}" in step detail, '
                           f'will debug this step as a basic component.')
            component_type = 'basic'
        else:
            component_dto = self.service_caller.get_component_by_id(
                component_id=self.step_detail['properties'][MODULE_PROPERTY_NAME],
                include_run_setting_params=False)
            component_type = component_dto.job_type

        # log trace
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(self.workspace)
        telemetry_values.update({'job_type': component_type})
        _LoggerFactory.trace(_get_telemetry_logger(), "StepRunDebug", telemetry_values)

        with _change_working_dir(Path(self.target) / self.step_id):
            result = True
            # prepare container and it's config
            step_run_image = DebugOnlineStepRunHelper.prepare_dev_container(self.workspace, self.step_run,
                                                                            dry_run=self.dry_run)
            self.python_path = step_run_image.python_path
            # download snapshot
            snapshot_result = DebugOnlineStepRunHelper.download_snapshot(
                self.service_caller, self.step_run, component_type=component_type, dry_run=self.dry_run)
            result = result and snapshot_result
            # download input/output data
            port_arg_map, input_result = DebugOnlineStepRunHelper.prepare_inputs(
                self.workspace, self.step_detail, dry_run=self.dry_run)
            result = result and input_result
            # get run arguments
            script, arguments = DebugOnlineStepRunHelper.prepare_arguments(self.step_id, self.step_detail,
                                                                           port_arg_map, component_type)
            # create vs code debug env
            DebugOnlineStepRunHelper.create_launch_config(self.step_id, self.python_path,
                                                          ['${workspaceFolder}/' + script], arguments)

            # Hint to install vscode extensions
            OnlineStepRunDebugger.hint_to_reopen_in_container(os.getcwd())

            if not result:
                raise RuntimeError('Snapshot/Dataset preparation failed, please prepare them before debugging.')


def _entry(argv):
    """CLI tool for component creating."""

    parser = argparse.ArgumentParser(
        prog="python -m azure.ml.component._debug._step_run_debugger",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""A CLI tool for component debugging.""",
    )

    subparsers = parser.add_subparsers()

    # create component folder parser
    debug_parser = subparsers.add_parser(
        'debug',
        description='A CLI tool for online component debugging.'
    )

    debug_parser.add_argument(
        '--subscription_id', '-s', type=str,
        help="Subscription id."
    )
    debug_parser.add_argument(
        '--resource_group_name', '-r', type=str,
        help="Resource group."
    )
    debug_parser.add_argument(
        '--workspace_name', '-w', type=str,
        help="Workspace name."
    )
    debug_parser.add_argument(
        '--experiment_name', '-e', type=str,
        help="Experiment name."
    )
    debug_parser.add_argument(
        '--run_id', "-i", type=str,
        help="Run id for specific component run."
    )
    debug_parser.add_argument(
        '--target', type=str,
        help="Target directory to build environment, will use current working directory if not specified."
    )
    debug_parser.add_argument(
        "--url", type=str,
        help="Step run url."
    )
    debug_parser.add_argument(
        "--dry_run", type=_str_to_bool,
        help="Dry run."
    )

    args, _ = parser.parse_known_args(argv)

    params = vars(args)

    def _to_vars(url=None, run_id=None, experiment_name=None, workspace_name=None, resource_group_name=None,
                 subscription_id=None, target=None, dry_run=False):
        return url, run_id, experiment_name, workspace_name, resource_group_name, subscription_id, target, dry_run

    url, run_id, experiment_name, workspace_name, resource_group_name, subscription_id, target, dry_run = _to_vars(
        **params)
    if url is not None:
        debugger = OnlineStepRunDebugger(url=url, target=target, dry_run=dry_run)
    elif all(var is not None for var in
             [run_id, experiment_name, workspace_name, resource_group_name, subscription_id]):
        debugger = OnlineStepRunDebugger(run_id=run_id,
                                         experiment_name=experiment_name,
                                         workspace_name=workspace_name,
                                         resource_group_name=resource_group_name,
                                         subscription_id=subscription_id,
                                         target=target,
                                         dry_run=dry_run)
    else:
        raise RuntimeError(
            'One of url or step run params(run_id, experiment_name, '
            'workspace_name, resource_group_name, subscription_id) should be passed.')
    debugger.run()


def main():
    """Use as a CLI entry function to use OnlineStepRunDebugger."""
    _entry(sys.argv[1:])


if __name__ == '__main__':
    main()
