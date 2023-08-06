# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from typing import Mapping, Sequence, Optional

from ._io_definition import ParameterDefinition
from .._restclients.designer.models import RunSettingParameter, RunSettingUIWidgetTypeEnum


class RunSettingParam(ParameterDefinition):
    """This class represent the definition of run setting parameters which will be set when run a component."""

    def __init__(
        self, argument_name, name, type, type_in_py,
        description=None, optional=False, default=None, min=None, max=None,
        is_compute_target=False, json_editor=None
    ):
        """Initialize a run setting parameter.

        :param argument_name: The argument name of the parameter which is used to set value in SDK.
        :type argument_name: str
        :param name: The display name of the parameter which is shown in UI.
        :type name: str
        :param type: The type of the parameter.
        :type type: str
                    TODO: Currently the type is not align to the type in InputDefinition, need to be aligned.
        :param type_in_py: The type represented as a python type, used in validation.
        :type type_in_py: type
                          TODO: Refine the validation logic to avoid two types here.
        :param description: The description of the parameter.
        :type description: str
        :param optional: Whether the parameter is optional.
        :type optional: bool
        :param default: The default value of the parameter.
        :type default: Any
        :param min: The min value for a numeric parameter.
        :type min: Union[float, int]
        :param max: The max value for a numeric parameter.
        :type max: Union[float, int]
        :param is_compute_target: Whether the run setting parameter indicate a compute target.
        :type is_compute_target: bool
        :param json_editor: Json Editor of the parameter.
        :type json_editor: UIJsonEditor
        """
        self._argument_name = argument_name
        self._type_in_py = type_in_py
        self._is_compute_target = is_compute_target
        self._json_editor = json_editor
        super().__init__(
            name=name, type=type, description=description, default=default, optional=optional, min=min, max=max,
        )

    @property
    def is_compute_target(self):
        """Return whether the run setting parameter indicate a compute target."""
        return self._is_compute_target

    @property
    def type_in_py(self):
        """Return the type represented as a python type, used in validation."""
        return self._type_in_py

    @property
    def argument_name(self):
        """Return the argument name of the parameter."""
        return self._argument_name

    # The following properties are used for backward compatibility
    # TODO: Update such places to use the new names in the spec then remove there properties.
    @property
    def is_optional(self):
        return self.optional

    @property
    def default_value(self):
        return self.default

    @property
    def parameter_type(self):
        return self.type

    @property
    def parameter_type_in_py(self):
        return self.type_in_py

    @property
    def upper_bound(self):
        return self.max

    @property
    def lower_bound(self):
        return self.min

    @property
    def json_schema(self):
        if self._json_editor is not None:
            json_schema = json.loads(self._json_editor.json_schema)
            return json_schema
        return None

    @classmethod
    def from_dto_run_setting_parameter(cls, p: RunSettingParameter):
        """Convert a run setting parameter the ModuleDto from API result to this class."""
        is_compute_target = p.run_setting_ui_hint.ui_widget_type == RunSettingUIWidgetTypeEnum.compute_selection
        return cls(
            argument_name=p.argument_name, name=p.name, type=p.parameter_type,
            type_in_py=p.parameter_type_in_py,
            description=p.description,
            optional=p.is_optional, default=p.default_value,
            min=p.lower_bound, max=p.upper_bound,
            is_compute_target=is_compute_target,
            json_editor=p.run_setting_ui_hint.json_editor
        )


class RunSettingsDefinition:
    """This class represent a definition of all run settings which need to be set when run a component."""

    def __init__(self, params: Mapping[str, RunSettingParam]):
        """Initialize a run settings definition with a list of run setting parameters."""
        # There should be only one compute target parameter in the initialization run setting parameters.
        self._target = next((param for param in params.values() if param.is_compute_target), None)
        self._params = params

    @property
    def target(self) -> RunSettingParam:
        """Return the compute target definition."""
        return self._target

    @property
    def params(self) -> Mapping[str, RunSettingParam]:
        """Return the mapping from arguments to parameters."""
        return self._params

    @classmethod
    def from_dto_runsettings(cls, dto_runsettings: Sequence[RunSettingParameter]):
        """Convert run settings parameter in ModuleDto from API result to the definition."""
        return cls(params={
            p.argument_name: RunSettingParam.from_dto_run_setting_parameter(p) for p in dto_runsettings
        })


class K8sSectionDefinition:
    """This class represent a section of k8s run settings which need to be set when run a component."""

    def __init__(self, name: str, params: Mapping[str, RunSettingParam], description: str = None):
        self._name = name
        self._description = description
        self._params = params

    @property
    def name(self):
        """Return the name of this section."""
        return self._name

    @property
    def description(self):
        """Return the description of this section."""
        return self._description

    @property
    def params(self) -> Mapping[str, RunSettingParam]:
        """Return the mapping from each run setting argument names to run setting parameters."""
        return self._params

    def __iter__(self):
        """This method is used to enable enumerate the parameters by `for xx in section`"""
        yield from self._params.values()

    @classmethod
    def from_dto_runsettings(cls, dto_runsettings: Sequence[RunSettingParameter]):
        """Convert run settings parameter in ModuleDto from API result to a section of k8s run settings."""
        if len(dto_runsettings) == 0:
            raise ValueError("Cannot initialize k8s section with no runsetting parameter.")
        params = {p.argument_name: RunSettingParam.from_dto_run_setting_parameter(p) for p in dto_runsettings}
        p = dto_runsettings[0]
        # The section related properties are set after `correct_module_dto` is called.
        return cls(name=p.section_argument_name, params=params, description=p.section_description)


class K8sRunSettingsDefinition(dict):
    """This class represent the definition of k8s run settings which need to be set when run a component.

    It is actually a dict from section names to each run setting sections which includes multiple run settings.
    TODO: Refine the whole design of K8sRunSettings.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._available_computes = []

    def get(self, k: str) -> Optional[K8sSectionDefinition]:
        return super().get(k)

    def __getitem__(self, item) -> K8sSectionDefinition:
        return super().__getitem__(item)

    @property
    def available_computes(self):
        """This indicates which computes could enable this definition."""
        return self._available_computes

    @classmethod
    def from_dto_runsettings(cls, dto_runsettings: Sequence[RunSettingParameter]):
        """Convert run settings parameter in ModuleDto from API result to the definition."""
        result = cls()

        # Find out the compute target section.
        target = next((
            p for p in dto_runsettings
            if p.run_setting_ui_hint.ui_widget_type == RunSettingUIWidgetTypeEnum.compute_selection
        ), None)
        if target is None:
            return result

        # Get the parameters from the compute target parameter.
        compute_run_settings_mapping = target.run_setting_ui_hint.compute_selection.compute_run_settings_mapping or {}
        # Get the first compute param list since all computes will share the same settings.
        compute_params = next((params for params in compute_run_settings_mapping.values() if len(params) > 0), [])

        # Set the available computes
        result._available_computes = sorted([
            compute_name for compute_name, params in compute_run_settings_mapping.items() if len(params) > 0
        ])

        # Put different compute params to different sections.
        sections = {p.section_argument_name for p in compute_params}
        result.update({
            section: K8sSectionDefinition.from_dto_runsettings(
                [p for p in compute_params if p.section_argument_name == section]
            ) for section in sections
        })
        return result
