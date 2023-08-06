# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines classes for run settings."""

import json
from typing import Sequence

from azureml._base_sdk_common.field_info import _FieldInfo
from azureml.core.runconfig import RunConfiguration
from ._core._run_settings_definition import RunSettingsDefinition, K8sRunSettingsDefinition, \
    RunSettingParam, K8sSectionDefinition
from ._dynamic import KwParameter, create_kw_method_from_parameters
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._exceptions import InvalidTargetSpecifiedError
from ._util._telemetry import WorkspaceTelemetryMixin

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class RunSettings(WorkspaceTelemetryMixin):
    """A RunSettings aggregates the run settings of a component."""

    def __init__(self, definition: RunSettingsDefinition, component_name, workspace, owner):
        """
        Initialize RunSettings.

        :param definition: The definition of RunSettings.
        :type definition: RunSettingsDefinition
        :param component_name: The name of the component.
        :type component_name: str
        :param workspace: The workspace of the component.
        :type workspace: azureml.core.Workspace
        :param owner: The component which the RunSettings belongs to.
        :type owner: azure.ml.component.Component
        """
        self._target = None
        self.target = definition.target.default
        for argument_name, param in definition.params.items():
            if not param.is_compute_target:
                setattr(self, argument_name, param.default)
        self._params_spec = definition.params
        self._workspace = workspace
        self._generate_configure_func(component_name)
        self._owner = owner
        WorkspaceTelemetryMixin.__init__(self, workspace=workspace)

    def _generate_configure_func(self, component_name):
        func_docstring_lines = []
        func_docstring_lines.append("Run setting configuration for component [{}]".format(component_name))
        if len(self._params_spec) > 0:
            func_docstring_lines.append("\n")
        params, _doc_string = _format_params(list(self._params_spec.values()))
        func_docstring_lines.extend(_doc_string)
        func_docstring = '\n'.join(func_docstring_lines)
        self.__doc__ = func_docstring

        self.configure = create_kw_method_from_parameters(
            self.configure,
            parameters=params,
            documentation=func_docstring,
        )

    @track(_get_logger, activity_type=_PUBLIC_API)
    def configure(self, *args, **kwargs):
        """
        Configure the runsettings.

        Note that this method will be replaced by a dynamic generated one at runtime with parameters
        that corresponds to the runsettings of the component.
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        from ._component_validator import ComponentValidator, RunSettingParameterType
        for k, v in kwargs.items():
            if k != "target":  # Bypass target validation since we have done it in property setter
                ComponentValidator.validate_single_runsettings_parameter(k, v, self,
                                                                         RunSettings._process_error)
                if self._params_spec[k].parameter_type == RunSettingParameterType.json_string and \
                        not isinstance(v, str):
                    v = json.dumps(v)
            setattr(self, k, v)

    def __repr__(self):
        """Return the representation of the RunSettings."""
        params_str = ''
        param_names = self._params_spec.keys()
        for name in param_names:
            params_str += '{}: {}\n'.format(name, getattr(self, name))
        return params_str

    def __setattr__(self, key, value):
        """Manage attribute validation."""
        object.__setattr__(self, key, value)
        # Note that this is only for telemetry. Using `__setattr__` is very error-prone and should be limited.
        if hasattr(self, '_params_spec') and key in self._params_spec.keys():
            self._owner._specify_runsettings = True
            self._owner._extra_runsettings[key] = value

    @property
    def _use_default_compute(self):
        return self._target is None

    @property
    def target(self):
        """
        Use name "target" to provide a common access for compute parameter.

        Because the name of compute parameter in HDInsight component is "Compute Name", while other components'
        are "Target".
        """
        return self._target

    @target.setter
    def target(self, compute):
        if compute is not None:
            if isinstance(compute, str):
                # Get compute type
                service_caller = _DesignerServiceCallerFactory.get_instance(self._workspace)
                target_compute = service_caller.get_compute_by_name(compute)
                if target_compute is None:
                    raise InvalidTargetSpecifiedError(target_name="RunSettings.target",
                                                      message="Cannot find compute '{}' in workspace".format(compute))
                else:
                    compute = (compute, target_compute.compute_type)
            elif not (isinstance(compute, tuple) and len(compute) == 2 and
                      isinstance(compute[0], str) and isinstance(compute[1], str)):
                raise InvalidTargetSpecifiedError(target_name="RunSettings.target",
                                                  message="Bad value for target, expect a string value")
        self._target = compute

    @staticmethod
    def _process_error(e: Exception, error_type):
        # Raise exception when hit INVALID_RUNSETTING_PARAMETER
        # Since missing some parameters is allowed when calling runsettings.configure(), for example:
        # runsettings.configure(node_count=2)
        # runsettings.target = 'amlcompute'
        from ._component_validator import ComponentValidationError
        if error_type == ComponentValidationError.INVALID_RUNSETTING_PARAMETER:
            ve = ComponentValidationError(str(e), e, error_type)
            raise ve


class _K8sRunSettings(object):
    def __init__(self, params: K8sRunSettingsDefinition, owner):
        self._params_spec = params
        for section_name, section_params in params.items():
            setattr(self, section_name, _K8sRunSettingsSection(section_params, section_name, owner))
        sections = sorted([section for section in params])
        self.__doc__ = "The compute run settings for Component, only take effect " \
                       "when compute type is in {}.\n" \
                       "Configuration sections: {}.".format(params.available_computes, str(sections))

    def __repr__(self):
        params_str = ''
        for name, section in sorted(self._params_spec.items()):
            params_str += '{}:\n'.format(section.name)
            for p in section.params.values():
                params_str += '\t{}: {}\n'.format(
                    p.argument_name, getattr(getattr(self, name), p.argument_name),
                )
        return params_str


class _K8sRunSettingsSection(object):
    def __init__(self, section: K8sSectionDefinition, section_name, owner):
        self._section_name = section_name
        for p in section.params.values():
            setattr(self, p.argument_name, p.default_value)
        self._params_spec = section.params
        self._generate_configure_func(section)
        self._owner = owner

    def _generate_configure_func(self, section: K8sSectionDefinition):
        func_docstring_lines = [section.description]
        func_params, _doc_string = _format_params(section.params.values(), is_compute_run_settings=True, )
        func_docstring_lines.extend(_doc_string)
        func_docstring = '\n'.join(func_docstring_lines)
        self.__doc__ = func_docstring
        self.configure = create_kw_method_from_parameters(
            self.configure,
            parameters=func_params,
            documentation=func_docstring,
        )

    def configure(self, *args, **kwargs):
        """
        Configure the runsettings.

        Note that this method will be replaced by a dynamic generated one at runtime with parameters
        that corresponds to the runsettings of the component.
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        for k, v in kwargs.items():
            from ._component_validator import ComponentValidator
            ComponentValidator.validate_single_k8srunsettings_parameter(k, v, self,
                                                                        RunSettings._process_error)
            setattr(self, k, v)

    def __repr__(self):
        params_str = ''
        param_names = self._params_spec.keys()
        for name in param_names:
            params_str += '{}: {}\n'.format(name, getattr(self, name))
        return params_str

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        # Note that this is only for telemetry. Using `__setattr__` is very error-prone and should be limited.
        if hasattr(self, '_params_spec') and key in self._params_spec.keys():
            self._owner._specify_k8srunsettings = True


def _set_compute_field(k8srunsettings, compute_type, run_config):
    compute_params_spec = k8srunsettings._params_spec
    if compute_params_spec is None:
        return
    compute_field_map = {'Cmk8s': 'cmk8scompute', 'CmAks': 'cmakscompute'}
    if compute_type in compute_field_map:
        field_name = compute_field_map[compute_type]
        aks_config = {'configuration': dict()}
        for section_name in compute_params_spec:
            for param in compute_params_spec[section_name]:
                value = getattr(getattr(k8srunsettings, section_name), param.argument_name)
                if value is not None:
                    aks_config['configuration'][param.argument_name] = value
        run_config._initialized = False
        setattr(run_config, field_name, aks_config)
        run_config._initialized = True
        RunConfiguration._field_to_info_dict[field_name] = _FieldInfo(dict,
                                                                      "{} specific details.".format(field_name))
        run_config.history.output_collection = True


def _format_params(source_params: Sequence[RunSettingParam], is_compute_run_settings=False):
    target_params = []
    func_docstring_lines = []
    for param in source_params:
        param_name = param.argument_name
        param_name_in_doc = param_name
        # For Hdi component, the name of target parameter is "compute_name"
        # But in sdk, we use "target" to access the target parameter
        # So we add a hint here to indicate "target" is exactly "compute_name"
        if param.is_compute_target and param_name != 'target':
            param_name = 'target'
            param_name_in_doc = 'target ({})'.format(param_name_in_doc)
        # For the k8s compute run settings,
        # the default value in spec is not match the value in description,
        # so we remove "default value" part in doc string for this case.
        if param.is_optional:
            func_docstring_lines.append(":param {}: {} (optional{})"
                                        .format(param_name_in_doc, param.description,
                                                "" if is_compute_run_settings else ", default value is {}."
                                                .format(param.default_value)))
        else:
            func_docstring_lines.append(":param {}: {}".format(param_name_in_doc, param.description))
        parameter_type = param.parameter_type
        func_docstring_lines.append(":type {}: {}".format(param_name_in_doc, parameter_type.value))
        target_params.append(KwParameter(
            param_name,
            annotation=param.description,
            default=param.default_value,
            _type=parameter_type.value))
    return target_params, func_docstring_lines
