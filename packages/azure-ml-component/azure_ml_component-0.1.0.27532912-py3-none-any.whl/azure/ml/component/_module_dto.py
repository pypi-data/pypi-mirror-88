# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import List
from datetime import timezone
from distutils.util import strtobool
from azureml.core import Workspace

from ._dynamic import KwParameter
from azure.ml.component._module._module_constants import IGNORE_PARAMS
from ._restclients.designer.models import ModuleDto as DesignerModuleDto, RunSettingParameterType, \
    RunSettingUIWidgetTypeEnum
from ._util._telemetry import TelemetryMixin, WorkspaceTelemetryMixin
from ._util._utils import _sanitize_python_variable_name, _get_or_sanitize_python_name


def _type_code_to_python_type(type_code):
    type_code = int(type_code)
    if type_code == 0:
        return int
    elif type_code == 1:
        return float
    elif type_code == 2:
        return bool
    elif type_code == 3:
        return str


def _type_code_to_python_type_name(type_code):
    try:
        return _type_code_to_python_type(type_code).__name__
    except BaseException:
        return None


def _python_type_to_type_code(value):
    if value is int:
        return 0
    if value is float:
        return 1
    if value is bool:
        return 2
    if value is str:
        return 3


def _int_str_to_run_setting_parameter_type(int_str_value):
    return list(RunSettingParameterType)[int(int_str_value)]


def _int_str_to_run_setting_ui_widget_type_enum(int_str_value):
    return list(RunSettingUIWidgetTypeEnum)[int(int_str_value)]


def _run_setting_param_type_to_python_type(param_type: RunSettingParameterType):
    if param_type == RunSettingParameterType.json_string or param_type == RunSettingParameterType.string:
        return str
    if param_type == RunSettingParameterType.double:
        return float
    if param_type == RunSettingParameterType.int_enum:
        return int
    if param_type == RunSettingParameterType.bool_enum:
        return bool


class ModuleDto(DesignerModuleDto, TelemetryMixin):
    def __init__(self, module_dto: DesignerModuleDto = None, **kwargs):
        if module_dto:
            _dict = {k: v for k, v in module_dto.__dict__.items()
                     if k in DesignerModuleDto._attribute_map.keys()}
            kwargs.update(_dict)
        super().__init__(**kwargs)
        if self._run_settings_param_type_incorrect():
            self.correct_run_settings()

        self.module_python_interface = ModulePythonInterface(self)

    def _run_settings_param_type_incorrect(self):
        run_setting_parameters = self.run_setting_parameters
        for p in run_setting_parameters:
            # Parameter with right type indicates that the module dto
            #   is cached and has been corrected before.
            if not isinstance(p.parameter_type, RunSettingParameterType):
                return True
        return False

    def _get_telemetry_values(self, workspace: Workspace = None):
        """
        Get telemetry value out of a module dto.

        The telemetry values include the following entries:

        * module_id
        * module_type
        * step_type
        * init_type

        :return: telemetry values.
        :rtype: dict
        """
        telemetry_values = {}
        if workspace is not None:
            telemetry_values.update(WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(workspace))
        telemetry_values['module_id'] = self.module_entity.id
        telemetry_values['step_type'] = self.module_entity.step_type

        # ModuleScope.global
        if self.module_scope == '1':
            telemetry_values['module_type'] = 'Global'
        # ModuleScope.workspace
        elif self.module_scope == '2':
            telemetry_values['module_type'] = 'Custom'
        # ModuleScope.anonymous
        elif self.module_scope == '3':
            telemetry_values['module_type'] = 'Anonymous'
            telemetry_values['module_id'] = self.module_version_id
        else:
            telemetry_values['module_type'] = 'Unknown'

        if self.codegen_by is not None:
            telemetry_values['init_type'] = self.codegen_by
        else:
            telemetry_values['init_type'] = ""

        return telemetry_values

    def get_module_inputs_outputs(self, return_yaml):
        interface = self.module_entity.structured_interface
        transformed_inputs = self.get_transformed_input_params(return_yaml)
        transformed_parameters = self.get_transformed_parameter_params(return_yaml)
        return transformed_inputs, transformed_parameters, interface.outputs

    def correct_module_dto(self):
        if not isinstance(self, ModuleDto):
            return self
        # A module_dto may not have a valid created_date so tzinfo is not set.
        # In such case we manually set the tzinfo to avoid the following warning.
        # WARNING - Datetime with no tzinfo will be considered UTC.
        # This warning is printed when serializing to json in the following code.
        # https://github.com/Azure/msrest-for-python/blob/master/msrest/serialization.py#L1039
        if self.created_date.tzinfo is None:
            self.created_date = self.created_date.replace(tzinfo=timezone.utc)
        if self.last_modified_date.tzinfo is None:
            self.last_modified_date = self.last_modified_date.replace(tzinfo=timezone.utc)

        module_entity = self.module_entity
        if module_entity.created_date.tzinfo is None:
            module_entity.created_date = module_entity.created_date.replace(tzinfo=timezone.utc)
        if module_entity.last_modified_date.tzinfo is None:
            module_entity.last_modified_date = module_entity.last_modified_date.replace(tzinfo=timezone.utc)

    def _correct_run_settings_param(self, param):
        # Convert int string to enum type
        param.parameter_type = _int_str_to_run_setting_parameter_type(param.parameter_type)
        param.parameter_type_in_py = _run_setting_param_type_to_python_type(param.parameter_type)
        param.run_setting_ui_hint.ui_widget_type = _int_str_to_run_setting_ui_widget_type_enum(
            param.run_setting_ui_hint.ui_widget_type)
        # Convert default value to correct type
        if param.default_value is not None and param.parameter_type_in_py is not None:
            if param.parameter_type_in_py is bool:
                param.default_value = bool(strtobool(param.default_value))
            else:
                param.default_value = param.parameter_type_in_py(param.default_value)
        # Handle none argument name
        if not hasattr(param, 'argument_name') or param.argument_name is None:
            param.argument_name = _sanitize_python_variable_name(param.label)

    def correct_run_settings(self):
        run_setting_parameters = self.run_setting_parameters
        for p in run_setting_parameters:
            self._correct_run_settings_param(p)
            # Mark compute target param
            p.is_compute_target = p.run_setting_ui_hint.ui_widget_type == RunSettingUIWidgetTypeEnum.compute_selection
        # Compute run settings
        target_param = next((p for p in run_setting_parameters if p.is_compute_target), None)
        compute_specs = target_param.run_setting_ui_hint.compute_selection.compute_run_settings_mapping
        if compute_specs is None:
            return
        for compute_type in compute_specs:
            compute_params = compute_specs[compute_type]
            if len(compute_params) > 0:
                for p in compute_params:
                    if not hasattr(p, 'section_argument_name'):
                        p.section_argument_name = _sanitize_python_variable_name(p.section_name)
                    self._correct_run_settings_param(p)

    def get_transformed_input_params(self, return_yaml: bool) -> List[KwParameter]:
        inputs = self.module_entity.structured_interface.inputs
        return [
            KwParameter(
                name=_get_or_sanitize_python_name(i.name, self.module_python_interface.inputs_name_mapping),
                # annotation will be parameter type if return yaml
                annotation=i.label if not return_yaml
                else str(i.data_type_ids_list),
                default=None,
                _type=str(i.data_type_ids_list)
            )
            for i in inputs
        ]

    def get_transformed_parameter_params(self, return_yaml: bool) -> List[KwParameter]:
        parameters = self.module_entity.structured_interface.parameters
        transformed_parameter_params = []
        for p in parameters:
            if p.name in IGNORE_PARAMS:
                continue
            default_value = p.default_value
            if default_value is not None:
                ptype = _type_code_to_python_type(p.parameter_type)
                default_value = bool(strtobool(default_value)) if ptype is bool and isinstance(default_value, str) \
                    else ptype(default_value)
            transformed_parameter_params.append(KwParameter(
                name=_get_or_sanitize_python_name(p.name, self.module_python_interface.parameters_name_mapping),
                # annotation will be parameter type if return yaml
                annotation=p.label if not return_yaml
                else _type_code_to_python_type_name(p.parameter_type),
                default=default_value,
                _type=_type_code_to_python_type_name(p.parameter_type)
            ))
        return transformed_parameter_params

    def get_run_setting_parameter_by_argument_name(self, argument_name):
        argument = next(filter(lambda param: param.argument_name == argument_name, self.run_setting_parameters), None)
        return argument


class ModulePythonInterface:
    def __init__(self, module_dto: ModuleDto):
        self.inputs = module_dto.module_python_interface.inputs
        self.inputs_name_mapping = {param.name: param.argument_name for param in self.inputs}

        self.outputs = module_dto.module_python_interface.outputs
        self.outputs_name_mapping = {param.name: param.argument_name for param in self.outputs}

        self.parameters = module_dto.module_python_interface.parameters
        self.parameters_name_mapping = {param.name: param.argument_name for param in self.parameters}

        self.name_mapping = {**self.inputs_name_mapping, **self.outputs_name_mapping, **self.parameters_name_mapping}

    def serialize_to_dict(self):
        param_dict = {"inputs": self.inputs_name_mapping,
                      "outputs": self.outputs_name_mapping,
                      "parameters": self.parameters_name_mapping}
        return param_dict

    def get_input_by_argument_name(self, argument_name):
        interface = next(
            filter(lambda item: item.argument_name == argument_name, self.inputs), None)
        return interface

    def get_parameter_by_argument_name(self, argument_name):
        interface = next(
            filter(lambda item: item.argument_name == argument_name, self.parameters), None)
        return interface

    def get_output_by_argument_name(self, argument_name):
        interface = next(
            filter(lambda item: item.argument_name == argument_name, self.outputs), None)
        return interface

    def get_param_name_to_argument_name_map(self):
        param_name_2_option_dict = {}
        for param_list in [self.inputs, self.parameters, self.outputs]:
            for param in param_list:
                param_name_2_option_dict[param.name] = param.argument_name
        return param_name_2_option_dict
