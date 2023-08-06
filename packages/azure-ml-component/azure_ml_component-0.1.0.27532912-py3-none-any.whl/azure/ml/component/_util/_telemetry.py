# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import uuid

from azureml.core import Workspace
from azureml.data.abstract_dataset import AbstractDataset


class TelemetryMixin(object):

    def __init__(self):
        pass

    def _get_telemetry_values(self, *args, **kwargs):
        return {}


class RequestTelemetryMixin(TelemetryMixin):

    def __init__(self):
        super().__init__()
        self._request_id = None
        self._from_cli = False

    def _get_telemetry_values(self, *args, **kwargs):
        return {'request_id': self._request_id, 'from_cli': self._from_cli}

    def _set_from_cli_for_telemetry(self):
        self._from_cli = True

    def _refresh_request_id_for_telemetry(self):
        self._request_id = str(uuid.uuid4())


class WorkspaceTelemetryMixin(TelemetryMixin):

    def __init__(self, workspace: Workspace):
        super(WorkspaceTelemetryMixin, self).__init__()
        self._workspace_for_telemetry = workspace

    def _get_telemetry_values(self, *args, **kwargs):
        return self._get_telemetry_value_from_workspace(self._workspace_for_telemetry)

    def _set_workspace_for_telemetry(self, workspace: Workspace):
        self._workspace_for_telemetry = workspace

    @staticmethod
    def _get_telemetry_value_from_workspace(workspace: Workspace):
        """
        Get telemetry value out of a Workspace.

        The telemetry values include the following entries:

        * workspace_id
        * workspace_name
        * subscription_id
        * resource_group
        * location
        * tenant_id

        :param workspace: The workspace.
        :type workspace: azureml.core.Workspace

        :return: telemetry values.
        :rtype: dict
        """
        if workspace is None:
            # log mock workspace for CI tests.
            import os
            # TODO: we may need a place for all these constants
            if '_TEST_ENV' in os.environ:
                return {'subscription_id': 'mock_subscription_id'}
            return {}
        telemetry_values = {
            'workspace_id': workspace._workspace_id,
            'workspace_name': workspace._workspace_name,
            'subscription_id': workspace._subscription_id,
            'resource_group': workspace.resource_group,
            'location': workspace.location
        }

        try:
            from azureml._base_sdk_common.common import fetch_tenantid_from_aad_token
            telemetry_values['tenant_id'] = fetch_tenantid_from_aad_token(workspace._auth_object._get_arm_token())
        except Exception as e:
            telemetry_values['tenant_id'] = "Error retrieving tenant id: {}".format(e)

        return telemetry_values


def _get_telemetry_value_from_pipeline_parameter(pipeline_parameters):
    telemetry_values = {}
    pipeline_parameters_count = 0
    data_pipeline_parameters_count = 0
    literal_pipeline_parameters_count = 0

    if pipeline_parameters is not None:
        pipeline_parameters_count = len(pipeline_parameters)
        data_pipeline_parameters_count = len([x for x in pipeline_parameters.values() if
                                              isinstance(x, AbstractDataset)])
        literal_pipeline_parameters_count = pipeline_parameters_count - data_pipeline_parameters_count

    telemetry_values['pipeline_parameters_count'] = pipeline_parameters_count
    telemetry_values['data_pipeline_parameters_count'] = data_pipeline_parameters_count
    telemetry_values['literal_pipeline_parameters_count'] = literal_pipeline_parameters_count
    return telemetry_values
