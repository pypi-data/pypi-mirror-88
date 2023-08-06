# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Union
from pathlib import Path
from abc import ABC, abstractmethod
from azure.ml.component.dsl._component import InputPath, OutputPath
from azure.ml.component.dsl._module_spec import BaseModuleSpec, Param, OutputPort, InputPort
from azure.ml.component.dsl._utils import logger, _sanitize_python_class_name, is_notebook_file,\
    NOTEBOOK_EXT, is_py_file, _to_camel_case
from azure.ml.component._util._utils import _sanitize_python_variable_name


DATA_PATH = Path(__file__).resolve().parent / 'data'
NOTEBOOK_ENTRY_TPL_FILE = DATA_PATH / 'from_notebook_sample_code.template'
ARGPARSE_ENTRY_TPL_FILE = DATA_PATH / 'from_argparse_sample_code.template'
ARGPRASE_ENTRY_TPL_FILE_PARALLEL = DATA_PATH / 'from_argparse_parallel_sample_code.template'


def normalize_working_dir(working_dir):
    if working_dir is None:
        working_dir = '.'
    if not Path(working_dir).is_dir():
        raise ValueError("Working directory '%s' is not a valid directory." % working_dir)
    return working_dir


def normalize_entry_path(working_dir, entry, ext=None, job_type=None):
    is_file = False
    if ext:
        is_file = entry.endswith(ext)
    if is_file:
        if Path(entry).is_absolute():
            raise ValueError("Absolute file path '%s' is not allowed." % entry)
        if not (Path(working_dir) / entry).is_file():
            raise FileNotFoundError("Entry file '%s' not found in working directory '%s'." % (entry, working_dir))
        entry = Path(entry).as_posix()
        # For parallel component, we need to import the entry instead of run it.
        if job_type == 'parallel':
            entry = entry[:-3].replace('/', '.')
    return entry


def normalized_target_file(working_dir, target_file, force):
    if target_file:
        if Path(target_file).is_absolute():
            raise ValueError("Absolute target file path '%s' is not allowed." % target_file)
        if not target_file.endswith('.py'):
            raise ValueError("Target file must has extension '.py', got '%s'." % target_file)
        if not force and (Path(working_dir) / target_file).exists():
            raise FileExistsError("Target file '%s' already exists." % target_file)
    return target_file


def normalized_spec_file(working_dir, spec_file, force):
    if spec_file:
        if Path(spec_file).is_absolute():
            raise ValueError("Absolute module spec file path '%s' is not allowed." % spec_file)
        if not spec_file.endswith('.yaml'):
            raise ValueError("Module spec file must has extension '.yaml', got '%s'." % spec_file)
        if not force and (Path(working_dir) / spec_file).exists():
            raise FileExistsError("Module spec file '%s' already exists." % spec_file)
    return spec_file


class BoolParam(Param):
    def __init__(self, name, description=None, default=None, arg_name=None, arg_string=None):
        super().__init__(
            name=name, type='Bool', description=description,
            default=default, arg_name=arg_name, arg_string=arg_string,
        )


class StoreTrueParam(BoolParam):
    @property
    def append_argv_statement(self):
        return "    if %s:\n        sys.argv.append(%r)" % (self.arg_name, self.arg_string)


class StoreFalseParam(BoolParam):
    @property
    def append_argv_statement(self):
        return "    if not %s:\n        sys.argv.append(%r)" % (self.arg_name, self.arg_string)


class BaseParamGenerator:
    def __init__(self, param: Union[Param, InputPort, OutputPort, InputPath, OutputPath]):
        self.param = param

    @property
    def type(self):
        return self.param.type

    @property
    def description(self):
        return self.param.description

    @property
    def default(self):
        value = self.param.default if isinstance(self.param, Param) else None
        if value is None:
            if hasattr(self.param, 'optional') and self.param.optional:
                return 'None'
            return None
        if self.type == 'String':
            return "'%s'" % value
        elif self.type == 'Enum':
            if value not in self.param.enum:
                value = self.param.enum[0]
            return "%s.%s" % (self.enum_class, self.enum_name(value, self.param.enum.index(value)))
        return str(value)

    @property
    def var_name(self):
        return _sanitize_python_variable_name(self.param.name) if self.param.arg_name is None else self.param.arg_name

    @property
    def arg_value(self):
        if self.param.type == 'Enum':
            return self.var_name + '.value'
        return 'str(%s)' % self.var_name

    @property
    def arg_def(self):
        result = "%s: %s" % (self.var_name, self.arg_type)
        result += ',' if self.default is None else ' = %s,' % self.default
        return result

    @property
    def enum_class(self):
        return 'Enum%s' % _sanitize_python_class_name(self.var_name)

    @staticmethod
    def enum_name(value, idx):
        name = _sanitize_python_variable_name(str(value))
        if name == '':
            name = 'enum%d' % idx
        return name

    @staticmethod
    def enum_value(value):
        return "'%s'" % value

    @property
    def enum_name_def(self):
        return '\n'.join("    %s = %s" % (self.enum_name(option, i), self.enum_value(option))
                         for i, option in enumerate(self.param.enum))

    @property
    def enum_def(self):
        return "class {enum_class}(Enum):\n{enum_value_string}\n".format(
            enum_class=self.enum_class, enum_value_string=self.enum_name_def,
        )


class ArgParseParamGenerator(BaseParamGenerator):
    mapping = {str: 'String', int: 'Int', float: 'Float', bool: 'Bool'}
    reverse_mapping = {v: k.__name__ for k, v in mapping.items()}

    @property
    def arg_type(self):
        if isinstance(self.param, (InputPort, OutputPort)):
            desc_str = 'description="%s"' % self.description if self.description else ''
            key = 'Input' if isinstance(self.param, InputPort) else 'Output'
            return "%sPath(%s)" % (key, desc_str)
        if not self.description:
            return self.enum_class if self.type == 'Enum' else self.reverse_mapping[self.type]
        tpl = "EnumParameter(enum={enum_class}, description=\"{description}\")" \
            if self.type == 'Enum' else "{type}Parameter(description=\"{description}\")"
        return tpl.format(type=self.type, enum_class=self.enum_class, description=self.description)

    @property
    def argv(self):
        return ["'%s'" % self.param.arg_string, self.arg_value]

    @property
    def is_optional_argv(self):
        return isinstance(self.param, BoolParam) or \
            not isinstance(self.param, OutputPort) and self.param.optional is True and \
            getattr(self.param, 'default', None) is None

    @property
    def append_argv_statement(self):
        if hasattr(self.param, 'append_argv_statement'):
            return self.param.append_argv_statement
        return """    if %s is not None:\n        sys.argv += [%s]""" % (self.var_name, ', '.join(self.argv))


class NotebookParamGenerator(BaseParamGenerator):

    @property
    def arg_type(self):
        return self.param.to_python_code()


class BaseComponentGenerator(ABC):

    def __init__(self, name=None, entry=None, description=None):
        self._params = []
        self.name = None
        if name is not None:
            self.set_name(name)
        self.entry = None
        self.entry_type = 'path'
        if entry is not None:
            self.set_entry(entry)
        self.description = description
        self._component_meta = {}
        self.parallel_inputs = []

    @property
    @abstractmethod
    def tpl_file(self):
        pass

    @property
    @abstractmethod
    def entry_template_keys(self):
        pass

    def set_name(self, name):
        if name.endswith('.py'):
            name = name[:-3]
        if name.endswith(NOTEBOOK_EXT):
            name = name[:-6]
        # Use the last piece as the component name.
        self.name = _to_camel_case(name.split('/')[-1].split('.')[-1])

    def set_entry(self, entry):
        self.entry = entry
        if is_py_file(entry):
            self.entry_type = 'path'  # python path
        elif is_notebook_file(entry):
            self.entry_type = 'notebook_path'
            suffix = NOTEBOOK_EXT
            self.entry_out = self.entry[:-len(suffix)] + '.out' + suffix
        else:
            self.entry_type = 'module'

    @property
    def component_name(self):
        if self.entry_type == 'module':
            return self.entry
        elif self.entry_type == 'path':
            return Path(self.entry).as_posix()[:-3].replace('/', '.')
        else:
            raise TypeError("Entry type %s doesn't have component name." % self.entry_type)

    def assert_valid(self):
        if self.name is None:
            raise ValueError("The name of a component could not be None.")
        if self.entry is None:
            raise ValueError("The entry of the component '%s' could not be None." % self.name)

    @property
    def params(self):
        return self._params

    def to_component_entry_code(self):
        self.assert_valid()
        with open(self.tpl_file) as f:
            entry_template = f.read()
        return entry_template.format(**{key: getattr(self, key) for key in self.entry_template_keys})

    def to_component_entry_file(self, target='entry.py'):
        with open(target, 'w') as fout:
            fout.write(self.to_component_entry_code())

    @property
    def func_name(self):
        return _sanitize_python_variable_name(self.name)

    @property
    def func_args(self):
        items = [''] + [param.arg_def for param in self.params if param.default is None] + \
                [param.arg_def for param in self.params if param.default is not None]
        return '\n    '.join(items)

    @property
    def dsl_param_dict(self):
        meta = self.component_meta
        if not meta:
            return ''
        items = [''] + ['%s=%r,' % (k, v) for k, v in meta.items()]
        if self.job_type == 'parallel':
            parallel_inputs_str = "InputPath(name='parallel_input_data')" if not self.parallel_inputs else \
                ', '.join("InputPath(name=%r)" % name
                          for name in self.parallel_inputs)
            items.append('parallel_inputs=[%s]' % parallel_inputs_str)
        return '\n    '.join(items) + '\n'

    @property
    def component_meta(self):
        meta = {**self._component_meta}
        if self.description and 'description' not in meta:
            meta['description'] = self.description
        if self.name and 'name' not in meta:
            meta['name'] = self.name
        return meta

    @property
    def job_type(self):
        return self.component_meta.get('job_type', 'basic').lower()

    def update_component_meta(self, component_meta):
        for k, v in component_meta.items():
            if v is not None:
                self._component_meta[k] = v


class ArgParseComponentGenerator(BaseComponentGenerator):

    @property
    def tpl_file(self):
        return ARGPRASE_ENTRY_TPL_FILE_PARALLEL if self.job_type == 'parallel' else ARGPARSE_ENTRY_TPL_FILE

    @property
    def entry_template_keys(self):
        return [
            'enums', 'imports',
            'entry_type', 'entry',
            'component_name',
            'func_name', 'func_args',
            'sys_argv', 'append_stmt',
            'dsl_param_dict',
        ]

    def add_param(self, param: Param):
        self._params.append(ArgParseParamGenerator(param))

    @property
    def params(self):
        result = self._params
        if self.job_type.lower() == 'parallel' and not self.has_output():
            # Add an output if output is not set, since parallel component require one output,
            # which may not be from argparse.
            return [ArgParseParamGenerator(OutputPort(
                name='Output', type='AnyDirectory', arg_name='output', arg_string='--output',
            ))] + result
        return result

    @property
    def component_entry_file(self):
        if is_py_file(self.entry):
            return self.entry
        return self.entry.replace('.', '/') + '.py'

    @property
    def spec(self):
        """This spec is directly generated by argument parser arguments,
        it is used to create a module spec without a new entry file.
        """
        params = [param.param for param in self.params if isinstance(param.param, Param)]
        inputs = [param.param for param in self.params if isinstance(param.param, InputPort)]
        outputs = [param.param for param in self.params if isinstance(param.param, OutputPort)]
        args = []
        for param in self.params:
            if not isinstance(param.param, OutputPort) and param.param.optional:
                args.append(param.param.arg_group())
            else:
                args += param.param.arg_group()

        return BaseModuleSpec(
            name=self.name, description=self.description,
            inputs=inputs, outputs=outputs, params=params,
            args=args,
            command=['python', self.component_entry_file],
        )

    @property
    def spec_dict(self):
        return self.spec.spec_dict

    def to_spec_yaml(self, folder, spec_file='spec.yaml'):
        self.assert_valid()
        self.spec._save_to_code_folder(folder, spec_file=spec_file)

    def has_type(self, type):
        return any(param.type == type for param in self._params)

    def has_import_type(self, type):
        return any(param.type == type and param.description is not None for param in self._params)

    def has_input(self):
        return any(isinstance(param.param, InputPort) for param in self._params)

    def has_output(self):
        return any(isinstance(param.param, OutputPort) for param in self._params)

    @property
    def enums(self):
        return '\n\n' + '\n\n'.join(param.enum_def for param in self.params if param.type == 'Enum') \
            if self.has_type('Enum') else ''

    @property
    def imports(self):
        keys = ['Enum'] + list(ArgParseParamGenerator.reverse_mapping)
        param_imports = [''] + ['%sParameter' % key for key in keys if self.has_import_type(key)]
        # Note that for a parallel component, input/output are required.
        if self.has_input() or self.job_type == 'parallel':
            param_imports.append('InputPath')
        if self.has_output() or self.job_type == 'parallel':
            param_imports.append('OutputPath')
        return ', '.join(param_imports)

    @property
    def sys_argv(self):
        items = ['', "'%s'," % self.entry] + [
            ', '.join(param.argv) + ',' for param in self.params if not param.is_optional_argv
        ]
        return '\n        '.join(items)

    @property
    def append_stmt(self):
        return '\n'.join(param.append_argv_statement for param in self.params if param.is_optional_argv)

    def update_spec_param(self, key, is_output=False):
        target = None
        key = key
        for param in self.params:
            if param.var_name == key:
                target = param
                break
        if not target:
            if not is_output and self.job_type == 'parallel':
                self.parallel_inputs.append(key)
            else:
                logger.warning(f"{key} not found in params.")
            return
        param = target.param
        if is_output:
            target.param = OutputPort(
                name=param.name, type="path", description=param.description,
                arg_string=param.arg_string,
            )
        else:
            target.param = InputPort(
                name=param.name, type="path",
                description=target.description, optional=param.optional,
                arg_string=param.arg_string,
            )

    def update_spec_params(self, keys, is_output=False):
        for key in keys:
            self.update_spec_param(key, is_output)


class NotebookComponentGenerator(BaseComponentGenerator):

    @property
    def tpl_file(self):
        return NOTEBOOK_ENTRY_TPL_FILE

    @property
    def entry_template_keys(self):
        return [
            'func_name',
            'func_args', 'parameters_dict',
            'entry', 'entry_out',
            'dsl_param_dict',
        ]

    def add_param(self, param: Union[Param, InputPath, OutputPath]):
        self._params.append(NotebookParamGenerator(param))

    @property
    def parameters_dict(self):
        items = [''] + ['%s=%s,' % (param.param.name, param.param.name) for param in self.params]
        return '\n            '.join(items)
