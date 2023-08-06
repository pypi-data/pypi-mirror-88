# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Sequence, Optional, Union


def _remove_empty_values(data, ignore_keys=None):
    if not isinstance(data, dict):
        return data
    ignore_keys = ignore_keys or {}
    return {k: v if k in ignore_keys else _remove_empty_values(v)
            for k, v in data.items() if v is not None or k in ignore_keys}


class ParameterDefinition:

    _PARAM_VALIDATORS = {
        'String': None,
        'Float': None,
        'Integer': None,
        'Boolean': None,
        'Enum': None,

        # The following types are internal usage for built-in modules.
        'Script': None,
        'ColumnPicker': None,
        'Credential': None,
        'ParameterRange': None
    }  # These validators are used to validate parameter values.

    _PARAM_PARSERS = {
        'Float': float,
        'Integer': int,
        'Boolean': lambda v: v.lower() == 'true',
    }

    def __init__(self, name, type, description=None, default=None, optional=False, enum=None, min=None, max=None):
        """Define an input for the component."""
        self._name = name
        self._type = type
        self._description = description
        self._optional = optional
        self._default = default
        self._enum = enum
        self._min = min
        self._max = max

    @property
    def name(self) -> str:
        """"Return the name of the parameter."""
        return self._name

    @property
    def type(self) -> str:
        """"Return the type of the parameter."""
        return self._type

    @property
    def optional(self) -> bool:
        """"Return whether the parameter is optional."""
        return self._optional

    @property
    def default(self) -> Optional[Union[str, int, float]]:
        """"Return the default value of the parameter."""
        return self._default

    @property
    def description(self) -> Optional[str]:
        """"Return the description of the parameter."""
        return self._description

    @property
    def enum(self) -> Optional[Sequence[str]]:
        """"Return the enum values of the parameter for an enum parameter."""
        return self._enum

    @property
    def max(self) -> Optional[Union[int, float]]:
        """"Return the maximum value of the parameter for a numeric parameter."""
        return self._max

    @property
    def min(self) -> Optional[Union[int, float]]:
        """"Return the minimum value of the parameter for a numeric parameter."""
        return self._min

    def to_dict(self, remove_name=False) -> dict:
        """Convert the ParameterDefinition object to a dict."""
        keys = ['name', 'type', 'description', 'min', 'max', 'enum', 'default', 'optional']
        if remove_name:
            keys.remove('name')
        result = {key: getattr(self, key) for key in keys}
        return _remove_empty_values(result)

    @classmethod
    def from_dict(cls, dct: dict):
        """Convert a dict to an ParameterDefinition object."""
        # Some legacy case have options instead of enum, this will be removed in the future.
        if 'options' in dct:
            dct['enum'] = dct.pop('options')
        return cls(**dct)

    @classmethod
    def load(cls, data):
        """Load an ParameterDefinition according to the input data type."""
        if isinstance(data, ParameterDefinition):
            return data
        elif isinstance(data, dict):
            return cls.from_dict(data)
        raise NotImplementedError("The conversion from %s to %s is not implemented." % (type(data), cls))

    def validate(self, value):
        """Validate whether the value is OK as the parameter."""
        validator = self._PARAM_VALIDATORS.get(str(self.type))
        if validator is None:
            return
        # TODO: Validate logic goes here

    @classmethod
    def is_valid_type(cls, type):
        """Return whether the type is a valid parameter type."""
        return isinstance(type, str) and type in cls._PARAM_VALIDATORS

    @classmethod
    def parse_param(cls, type, str_value):
        """Parse the str value to param value according to the param type."""
        parser = cls._PARAM_PARSERS.get(type)
        return parser(str_value) if isinstance(str_value, str) and parser else str_value


class InputDefinition:

    def __init__(self, name, type, description=None, optional=False):
        """Define an output definition for the component."""
        self._name = name
        self._type = type
        self._description = description
        self._optional = optional

    @property
    def name(self) -> str:
        """"Return the name of the input."""
        return self._name

    @property
    def type(self) -> str:
        """"Return the type of the input."""
        return self._type

    @property
    def description(self) -> str:
        """"Return the description of the input."""
        return self._description

    @property
    def optional(self) -> bool:
        """"Return whether the input is optional."""
        return self._optional

    @classmethod
    def from_dict(cls, dct):
        """Convert a dict to an InputDefinition object."""
        return cls(**dct)

    def to_dict(self, remove_name=False):
        """Convert the InputDefinition object to a dict."""
        keys = ['name', 'type', 'description', 'optional']
        if remove_name:
            keys.remove('name')
        result = {key: getattr(self, key) for key in keys}
        return _remove_empty_values(result)

    @classmethod
    def load(cls, data):
        """Load an InputDefinition according to the input data type."""
        if isinstance(data, InputDefinition):
            return data
        elif isinstance(data, dict):
            return cls.from_dict(data)
        raise NotImplementedError("The conversion from %s to %s is not implemented." % (type(data), cls))


class OutputDefinition:

    def __init__(self, name, type, description=None):
        """Define an output definition for the component."""
        self._name = name
        self._type = type
        self._description = description

    @property
    def name(self) -> str:
        """"Return the name of the output."""
        return self._name

    @property
    def type(self) -> str:
        """"Return the type of the output."""
        return self._type

    @property
    def description(self) -> str:
        """"Return the description of the output."""
        return self._description

    @classmethod
    def from_dict(cls, dct: dict):
        """Convert a dict to an OutputDefinition object."""
        return cls(**dct)

    def to_dict(self, remove_name=False):
        """Convert the OutputDefinition object to a dict."""
        keys = ['name', 'type', 'description']
        if remove_name:
            keys.remove('name')
        result = {key: getattr(self, key) for key in keys}
        return _remove_empty_values(result)

    @classmethod
    def load(cls, data):
        """Load an OutputDefinition according to the output data type."""
        if isinstance(data, OutputDefinition):
            return data
        elif isinstance(data, dict):
            return cls.from_dict(data)
        raise NotImplementedError("The conversion from %s to %s is not implemented." % (type(data), cls))
