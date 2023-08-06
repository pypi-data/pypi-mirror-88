# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import sys
from abc import ABCMeta
from typing import List
from pathlib import Path
from enum import EnumMeta

from azure.ml.component.dsl._module_spec import _BaseParam, Param, InputPort, OutputPort
from ._exceptions import RequiredParamParsingError, DSLComponentDefiningError


class _ComponentBaseParam(_BaseParam):
    """This class defines some common operation for ComponentInputPort/ComponentOutputPort/ComponentParam."""

    @property
    def arg_string(self):
        """Compute the cli option str according to its name, used in argparser."""
        return '--' + self.name

    def to_cli_option_str(self, style=None):
        """Return the cli option str with style, by default return underscore style --a_b."""
        return self.arg_string.replace('_', '-') if style == 'hyphen' else self.arg_string

    def update_name(self, name: str):
        """Update the name of the port/param.

        Initially the names of inputs should be None, then we use variable names of python function to update it.
        """
        if self._name is not None:
            raise AttributeError("Cannot set name to %s since it is not None, the value is %s." % (name, self._name))
        if not name.isidentifier():
            raise DSLComponentDefiningError("The name must be a valid variable name, got '%s'." % name)
        self._name = name

    def add_to_arg_parser(self, parser: argparse.ArgumentParser, default=None):
        """Add this parameter to ArgumentParser, both command line styles are added."""
        cli_str_underscore = self.to_cli_option_str(style='underscore')
        cli_str_hyphen = self.to_cli_option_str(style='hyphen')
        if default is not None:
            return parser.add_argument(cli_str_underscore, cli_str_hyphen, default=default)
        else:
            return parser.add_argument(cli_str_underscore, cli_str_hyphen,)

    def set_optional(self):
        """Set the parameter as an optional parameter."""
        self._optional = True

    @classmethod
    def register_data_type(cls, data_type: type):
        """Register the data type to the corresponding parameter/port."""
        if not isinstance(data_type, type):
            raise TypeError("Only python type is allowed to register, got %s." % data_type)
        cls.DATA_TYPE_MAPPING[data_type] = cls
        cls.DATA_TYPE_NAME_MAPPING[cls.__name__] = cls


class _DataTypeRegistrationMeta(ABCMeta):
    """This meta class is used to register data type mapping for ports/parameters.

    With this metaclass, a simple annotation str could be converted to StringParameter by declaring `DATA_TYPE`.
    """

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        data_type = getattr(cls, 'DATA_TYPE', None)
        if data_type is not None:
            try:
                cls()
            except TypeError:
                raise ValueError("To register a data type, the class must be able to initialized with %s()" % name)
            cls.register_data_type(data_type)
        return cls


class _ComponentParam(Param, _ComponentBaseParam, metaclass=_DataTypeRegistrationMeta):
    """This is the base class of component parameters.

    The properties including name/type/default/options/optional/min/max will be dumped in component spec.
    When invoking a component, param.parse_and_validate(str_val) is called to parse the command line value.
    """

    DATA_TYPE_MAPPING = {}
    DATA_TYPE_NAME_MAPPING = {}

    def __init__(self, name, type,
                 description=None, default=None, options=None, optional=False, min=None, max=None,
                 ):
        super().__init__(name, type, description, default, options, optional, min, max)
        self._allowed_types = ()
        data_type = getattr(self, 'DATA_TYPE', None)
        # TODO: Maybe a parameter could have several allowed types? For example, json -> List/Dict?
        if data_type:
            self._allowed_types = (data_type,)
        self.update_default(default)

    def update_default(self, default_value):
        """Update default is used when the annotation has default values.

        Here we need to make sure the type of default value is allowed.
        """
        if default_value is not None and not isinstance(default_value, self._allowed_types):
            try:
                default_value = self.parse(default_value)
            except Exception as e:
                if self.name is None:
                    msg = "Default value of %s cannot be parsed, got '%s', type = %s." % (
                        type(self).__name__, default_value, type(default_value)
                    )
                else:
                    msg = "Default value of %s '%s' cannot be parsed, got '%s', type = %s." % (
                        type(self).__name__, self.name, default_value, type(default_value)
                    )
                raise DSLComponentDefiningError(cause=msg) from e
        self._default = default_value

    def parse(self, str_val: str):
        """Parse str value passed from command line."""
        return str_val

    def validate_or_throw(self, value):
        """Validate input parameter value, throw exception if not as required.

        It will throw exception if validate failed, otherwise do nothing.
        """
        if not self.optional and value is None:
            raise ValueError("Parameter %s cannot be None since it is not optional." % self.name)
        if self._allowed_types and value is not None:
            if not isinstance(value, self._allowed_types):
                raise TypeError(
                    "Unexpected data type for parameter '%s'. Expected %s but got %s." % (
                        self.name, self._allowed_types, type(value)
                    )
                )

    def parse_and_validate(self, value):
        """Parse the value and validate it."""
        value = self.parse(value) if isinstance(value, str) else value
        self.validate_or_throw(value)
        return value

    def add_to_arg_parser(self, parser: argparse.ArgumentParser, default=None):
        """Add this parameter to ArgumentParser with its default value."""
        default = default or self.default
        super().add_to_arg_parser(parser, default)

    def to_python_code(self):
        """Return the representation of this parameter in annotation code."""
        parameters = []
        if self._default is not None:
            parameters.append('default={!r}'.format(self._default))
        if self._description is not None:
            parameters.append('description={!r}'.format(self._description))
        if self._min is not None:
            parameters.append('min={}'.format(self._min))
        if self._max is not None:
            parameters.append('max={}'.format(self._max))

        return "{type_name}({parameters})".format(
            type_name=self.__class__.__name__, parameters=', '.join(parameters))


class _ComponentInputPort(InputPort, _ComponentBaseParam):
    """This is the base class of component input ports.

    The properties including type/description/optional will be dumped in component spec.
    """

    def __init__(self, type, description=None, name=None, optional=None):
        """Initialize an input port."""
        super().__init__(name=name, type=type, description=description, optional=optional)

    def load(self, str_val: str):
        """Load the data from an input_path with type str."""
        return str_val


class InputPath(_ComponentInputPort):
    """InputPath indicates an input which is a directory."""

    def __init__(self, type='path', description=None, name=None, optional=None):
        """Initialize an output directory port, declare type to use your custmized port type."""
        super().__init__(type=type, description=description, name=name, optional=optional)

    def to_python_code(self):
        """Return the representation of this parameter in annotation code."""
        arguments = ["type=%r" % self.type]
        if self.description:
            arguments.append("description=%r" % self.description)
        if self.name:
            arguments.append("name=%r" % self.name)
        if self.optional:
            arguments.append("optional=%r" % self.optional)
        return "InputPath(%s)" % (', '.join(arguments))


class InputFile(_ComponentInputPort):
    """InputFile indicates an input which is a file."""

    def __init__(self, type='AnyFile', description=None, name=None, optional=None):
        """Initialize an input file port Declare type to use your custmized port type."""
        super().__init__(type=type, description=description, name=name, optional=optional)


class _InputFileList:

    def __init__(self, inputs: List[_ComponentInputPort]):
        self.validate_inputs(inputs)
        self._inputs = inputs
        for i in inputs:
            if i.arg_name is None:
                i.arg_name = i.name

    @classmethod
    def validate_inputs(cls, inputs):
        for i, port in enumerate(inputs):
            if not isinstance(port, (InputFile, InputPath)):
                msg = "You could only use InputPath in an input list, got '%s'." % type(port)
                raise DSLComponentDefiningError(msg)
            if port.name is None:
                raise DSLComponentDefiningError("You must specify the name of the %dth input." % i)
        if all(port.optional for port in inputs):
            raise DSLComponentDefiningError("You must specify at least 1 required port in the input list, got 0.")

    def add_to_arg_parser(self, parser: argparse.ArgumentParser):
        for port in self._inputs:
            port.add_to_arg_parser(parser)

    def load_from_args(self, args):
        """Load the input files from parsed args from ArgumentParser."""
        files = []
        for port in self._inputs:
            str_val = getattr(args, port.name, None)
            if str_val is None:
                if not port.optional:
                    raise RequiredParamParsingError(name=port.name, arg_string=port.arg_string)
                continue
            files += [str(f) for f in Path(str_val).glob('**/*') if f.is_file()]
        return files

    def load_from_argv(self, argv=None):
        if argv is None:
            argv = sys.argv
        parser = argparse.ArgumentParser()
        self.add_to_arg_parser(parser)
        args, _ = parser.parse_known_args(argv)
        return self.load_from_args(args)

    @property
    def inputs(self):
        return self._inputs


class _ComponentOutputPort(OutputPort, _ComponentBaseParam):
    """This is the base class of component output ports.

    The properties including type/description will be dumped in component spec.
    """

    def __init__(self, type, description=None, name=None):
        super().__init__(name=name, type=type, description=description)

    def set_optional(self):
        """Set output port as optional always fail."""
        pass


class OutputPath(_ComponentOutputPort):
    """OutputPath indicates an output which is a directory."""

    def __init__(self, type='path', description=None, name=None):
        """Initialize an output directory port, declare type to use your customized port type."""
        super().__init__(type=type, description=description, name=name)

    def to_python_code(self):
        """Return the representation of this parameter in annotation code."""
        """Str representation of OutputPath."""
        arguments = ["type=%r" % self.type]
        if self.description:
            arguments.append("description=%r" % self.description)
        if self.name:
            arguments.append("name=%r" % self.name)
        return "OutputPath(%s)" % (', '.join(arguments))


class OutputFile(_ComponentOutputPort):
    """OutputFile indicates an output which is a file."""

    def __init__(self, type='AnyFile', description=None):
        """Initialize an output file port Declare type to use your custmized port type."""
        super().__init__(type=type, description=description)


class StringParameter(_ComponentParam):
    """String parameter passed the parameter string with its raw value."""

    DATA_TYPE = str

    def __init__(
            self,
            description=None,
            optional=False,
            default=None,
    ):
        """Initialize a string parameter."""
        _ComponentParam.__init__(
            self,
            name=None,
            description=description,
            optional=optional,
            default=default,
            type='String',
        )


class EnumParameter(_ComponentParam):
    """Enum parameter parse the value according to its enum values."""

    def __init__(
            self,
            enum: EnumMeta = None,
            description=None,
            optional=False,
            default=None,
    ):
        """Initialize an enum parameter, the options of an enum parameter are the enum values."""
        if not isinstance(enum, EnumMeta):
            raise ValueError("enum must be a subclass of Enum.")
        if len(list(enum)) <= 0:
            raise ValueError("enum must have enum values.")
        self._enum_class = enum
        self._option2enum = {str(option.value): option for option in enum}
        self._val2enum = {option.value: option for option in enum}
        super().__init__(
            name=None,
            optional=optional,
            description=description,
            default=default,
            type='Enum',
            options=[str(option.value) for option in enum],
        )

    @property
    def options(self):
        """Return the option values of the enum."""
        return self.enum

    def parse(self, str_val: str):
        """Parse the enum value from a string value."""
        if str_val not in self._option2enum and str_val not in self._val2enum:
            raise ValueError("Not a valid enum value: '%s', valid values: %s" % (str_val, ', '.join(self.options)))
        return self._option2enum.get(str_val) or self._val2enum.get(str_val)

    def update_default(self, default_value):
        """Enum parameter support updating values with a string value."""
        if default_value in self._val2enum:
            default_value = self._val2enum[default_value]
        if isinstance(default_value, self._enum_class):
            default_value = default_value.value
        if default_value is not None and default_value not in self._option2enum:
            raise ValueError(
                "Not a valid enum value: '%s', valid values: %s" % (default_value, ', '.join(self.options))
            )
        self._default = default_value


class _NumericParameter(_ComponentParam):
    """Numeric Parameter is an intermediate type which is used to validate the value according to min/max."""

    def validate_or_throw(self, val):
        super().validate_or_throw(val)
        if self._min is not None and val < self._min:
            raise ValueError("Parameter '%s' should not be less than %s." % (self.name, self._min))
        if self._max is not None and val > self._max:
            raise ValueError("Parameter '%s' should not be greater than %s." % (self.name, self._max))


class IntParameter(_NumericParameter):
    """Int Parameter parse the value to a int value."""

    DATA_TYPE = int

    def __init__(
            self,
            min=None,
            max=None,
            description=None,
            optional=False,
            default=None,
    ):
        """Initialize an integer parameter."""
        _NumericParameter.__init__(
            self,
            name=None,
            optional=optional,
            description=description,
            default=default,
            min=min,
            max=max,
            type='Integer',
        )

    def parse(self, val):
        """Parse the integer value from a string value."""
        return int(val)


class FloatParameter(_NumericParameter):
    """Float Parameter parse the value to a float value."""

    DATA_TYPE = float

    def __init__(
            self,
            min=None,
            max=None,
            description=None,
            optional=False,
            default=None,
    ):
        """Initialize a float parameter."""
        _ComponentParam.__init__(
            self,
            name=None,
            optional=optional,
            description=description,
            default=default,
            min=min,
            max=max,
            type='Float',
        )

    def parse(self, val):
        """Parse the float value from a string value."""
        return float(val)


class BoolParameter(_ComponentParam):
    """Bool Parameter parse the value to a bool value."""

    DATA_TYPE = bool

    def __init__(
            self,
            description=None,
            default=False,
    ):
        """Initialize a bool parameter."""
        _ComponentParam.__init__(
            self,
            name=None,
            optional=True,
            description=description,
            default=default,
            type='Boolean',
        )

    def parse(self, val):
        """Parse the bool value from a string value."""
        if val.lower() not in {'true', 'false'}:
            raise ValueError("Bool parameter '%s' only accept True/False, got %s." % (self.name, val))
        return True if val.lower() == 'true' else False
