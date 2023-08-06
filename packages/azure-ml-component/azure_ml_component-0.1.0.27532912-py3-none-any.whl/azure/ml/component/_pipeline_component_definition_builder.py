# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import sys
import uuid
from collections import OrderedDict
from inspect import Parameter, signature
from datetime import datetime

from azureml.data._dataset import _Dataset
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data.file_dataset import FileDataset
from azureml.exceptions import UserErrorException

from .component import Component, Output, Input, _AttrDict
from ._core._component_definition import PipelineComponentDefinition
from ._dataset import _GlobalDataset
from ._pipeline_validator import PipelineValidator
from ._pipeline_parameters import PipelineParameter
from ._util._exceptions import PipelineValidationError


class PipelineComponentDefinitionBuilder:
    def __init__(self, name=None, description=None, workspace=None,
                 default_compute_target=None, default_datastore=None,
                 parameters=None, from_module_name=None, pipeline_function_name=None,
                 parent_definition_id=None):
        """
        :param name: Definition name.
        :type name: str
        :param description: Description of definition.
        :type description: str
        :param parameters: Parameters of function defined by dsl.pipeline.
        :type parameters: dict
        :param workspace: workspace of definition.
        :type workspace: Workspace
        :param from_module_name: from module name.
        :type from_module_name: str
        :param pipeline_function_name: The pipeline funtion name.
        :type pipeline_function_name: str
        :param default_compute_target: The resolved default compute target.
        :type default_compute_target: tuple(str, str)
        :param default_datastore: The default datastore.
        :type default_datastore: str
        :param parent_definition_id: The parent definition id.
            Used to recover the definition of pipeline so that we can export graph to code.
            Notice that a sub pipeline has parent_definition_id only when sub pipeline defined inside parent pipeline.
            The sub pipeline which defined outside but created inside parent do not has parent_definition_id.
        :type parent_definition_id: str
        """
        self.id = str(uuid.uuid4())
        if name is None:
            now = datetime.now()
            name = 'Pipeline-Created-on-{}-{}-{}'.format(now.month, now.day, now.year)
        self.name = name
        self.description = description
        # Id to components dict inside pipeline definition.
        self.components = OrderedDict({})
        # The variable names of pipeline's components.
        self.components_variable_names = []
        # A dict of inputs name to InputDefinition.
        self.inputs = {}
        # A dict of outputs name to OutputDefinition.
        self.outputs = {}
        self.parameters = {}
        self.original_function_parameters = {}
        if parameters is not None:
            # Inputs will be added as parameter here and will updated in function `_update_inputs_and_parameters_type`
            # Hard code type String here, will be updated from component definition if pass it to component.
            self.original_function_parameters = {name: {'name': name, 'type': 'String', 'default': param.default}
                                                 for name, param in parameters.items()}
            self.not_used_parameter_key = set(self.original_function_parameters.keys())
        # A dict of outputs name to OutputBuilder on Component.
        self.outputs_mapping = {}
        self.default_compute_target = default_compute_target
        self.default_datastore = default_datastore
        self.workspace = workspace
        # A list of dictionaries use to convert kwargs
        # from pipeline input to have component matched key. Dict key is component
        # definition, value is a dict of pipeline parameter keys to component parameter keys list.
        self.components_args_matched_dict_list = []
        self.parent_definition_id = parent_definition_id
        self.from_module_name = from_module_name
        self.pipeline_function_name = pipeline_function_name
        self._component_definition = None

    def _update_inputs_and_parameters_type(self, component):
        """
        Update pipeline parameters type recursively.

        Pipeline parameter type will be determined by the type of inputs
            it finally given on container component, and will be moved to inputs if it was passed
            to input port finally.
        :param component: Current component.
        :type component: Component
        """
        if component._definition is None:
            return
        if isinstance(component._definition, PipelineComponentDefinition):
            # If is sub pipeline, update sub's parameters by container component first.
            nodes, _ = component._expand_pipeline_nodes()
            for comp in nodes:
                self._update_inputs_and_parameters_type(comp)

        # Update current parameters' type by updated component's definition
        # Find pipeline parameters as component input and get type
        all_component_params = {**component.inputs}
        all_component_params.update({**component._parameter_params})
        for key, _input in all_component_params.items():
            val = _input._get_internal_data_source() if isinstance(_input, Input) else _input
            if not isinstance(val, PipelineParameter):
                continue
            parameter_name = val.name
            if parameter_name not in self.not_used_parameter_key:
                continue
            if key in component._definition.inputs.keys():
                # Move parameter to input, update type
                attr_dict = self.original_function_parameters[parameter_name]
                if not isinstance(component._definition, PipelineComponentDefinition):
                    # Only remove component's parameter/inputs.
                    # Do not remove pipeline component parameters because it may be an unused parameter.
                    self.not_used_parameter_key.remove(parameter_name)
                parameter_input = {'name': attr_dict['name']}
                parameter_input.update({'type': component._definition.inputs[key].type})
                self.inputs.update({parameter_name: parameter_input})
            elif key in component._definition.parameters.keys():
                # Update parameter type
                if not isinstance(component._definition, PipelineComponentDefinition):
                    # Only remove component's parameter/inputs.
                    # Do not remove pipeline component parameters because it may be an unused parameter.
                    self.not_used_parameter_key.remove(parameter_name)
                self.parameters[parameter_name] = self.original_function_parameters[parameter_name]
                self.parameters[parameter_name].update({'type': component._definition.parameters[key].type})

    def _update_components_variable_names(self, _locals_data):
        """
        Record component variable names defined by user.

        e.g.
        def pipeline():
            module1 = module_func()
            m2 = module_func()
            no_name = module_func()
            module_func()

        The components_variable_names will be ['module1', 'm2', 'no_name', None]
        Component without name will not in locals data.
        """
        id_name_dict = {}
        for k, v in _locals_data.items():
            if not isinstance(v, Component):
                continue
            if v not in self.components.values():
                continue
            id_name_dict[v._id] = k
        self.components_variable_names.extend([
            id_name_dict[_k] if _k in id_name_dict else None for _k in self.components.keys()])

    def _update_outputs(self, outputs):
        """
        Set method to set pipeline definition outputs.

        It will check if right type of outputs is passed,
            then find the original port definition from it's owner.

        :param outputs: Outputs of component
        :type outputs: Mapping[str, _OutputBuilder]
        """
        error_msg = "The return type of dsl.pipeline decorated function should be a mapping from dataset name to " \
                    "azure.ml.component.component._OutputBuilder"
        is_type_valid = isinstance(outputs, dict)
        if not is_type_valid:
            raise UserErrorException(error_msg)
        for key, value in outputs.items():
            is_key_type_value = isinstance(key, str)
            is_value_type_valid = isinstance(value, Output)
            if not is_key_type_value or not is_value_type_valid:
                raise UserErrorException(error_msg)
            owner = value._owner
            if owner is not None and owner._definition is not None:
                self.outputs.update({
                    key: _v.to_dict() for _k, _v in owner._definition.outputs.items() if _k == value._name})
        self.outputs_mapping = outputs if outputs is not None else {}

    def _correct_default_compute_target(self):
        from ._sub_pipeline_info_builder import _get_compute_setting
        default_compute_target = self._get_default_compute_target()
        self.default_compute_target = _get_compute_setting(default_compute_target)

    def _correct_default_data_store(self):
        from ._sub_pipeline_info_builder import _get_data_store_setting
        default_data_store = self.default_datastore
        self.default_data_store = _get_data_store_setting(default_data_store)

    def _get_default_compute_target(self):
        """Try to resolve the default compute target to tuple(compute_name, compute_type)."""
        default_compute_target = self.default_compute_target

        if default_compute_target is None:
            return None, "AmlCompute"

        # try to resolve compute target
        if isinstance(default_compute_target, str):
            if self.workspace is None:
                # this should only happens in dsl pipeline, when we initialize a Pipeline with no nodes
                return default_compute_target, "AmlCompute"
            from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
            service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
            target = service_caller.get_compute_by_name(default_compute_target)
            if target is None:
                print(default_compute_target + " not found in workspace, assume this is an AmlCompute")
                return default_compute_target, "AmlCompute"
            else:
                return target.name, target.compute_type
        elif isinstance(default_compute_target, tuple):
            if not len(default_compute_target) == 2:
                raise ValueError('Compute target tuple must have 2 elements (compute name, compute type)')
            return default_compute_target
        else:
            raise ValueError('Compute target must be a string')

    def _sort_inputs(self):
        # Sort inputs order as original parameter order.
        self.inputs = {_k: self.inputs[_k] for _k in self.original_function_parameters if _k in self.inputs}
        # Add not used parameter to parameters.
        self.parameters.update({
            _k: _v for _k, _v in self.original_function_parameters.items() if _k in self.not_used_parameter_key})
        # Sort parameters order as original parameter order.
        self.parameters = {
            _k: self.parameters[_k] for _k in self.original_function_parameters if _k in self.parameters}

    def add_component(self, component):
        """
        Add a component into pipeline component definition builder.

        :param component: other component
        :type component: Component
        """
        if component._id in self.components.keys():
            raise UserErrorException('Component already exists.')
        if self.workspace is None:
            self.workspace = component._workspace
        else:
            is_same_workspace = \
                self.workspace._workspace_id == component._workspace._workspace_id
            if not is_same_workspace:
                raise UserErrorException(
                    'Not all pipeline nodes are from the same workspace: {}, {}'.format(
                        self.workspace, component
                    ))
        self._update_inputs_and_parameters_type(component)
        self.components.update({component._id: component})
        self.components_args_matched_dict_list.append(_get_component_args_matched_dict(component))

    def build(self) -> 'PipelineComponentDefinition':
        """
        Build a pipeline component definition using current pipeline definition builder.

        This function will build recursively if there is sub pipeline inside, notice that
            current builder need an attribute named `func` to get the function defined by dsl.pipeline.
        e.g.
        # Now we just create a definition builder but not build.
        @dsl.pipeline
        def sub():
            ...
        @dsl.pipeline
        def parent():
            sub()
        # We build pipeline definition when you want to get a real pipeline instance.
        pipeline = parent()
        #
        """
        if self._component_definition is not None:
            return self._component_definition
        func = self.__getattribute__('func')
        if func is None:
            raise Exception('Pipeline component definition builder call build() without function inside!')
        parameter_list = signature(func).parameters.values()
        _definition_id_now_build.append(self.id)
        default_args = {_p.name: _p.default if _p.default is not Parameter.empty else None
                        for _p in parameter_list}
        original_profiler = sys.getprofile()
        _locals_data = {}

        def tracer(frame, event, arg):
            if event != 'return':
                return
            # Capture the locals of user's dsl function, added to builder.
            nonlocal _locals_data
            _locals_data = frame.f_locals.copy()

        def wrapper_func(*args, **kwargs) -> 'PipelineComponentDefinition':
            is_sub_pipeline = not _definition_builder_stack.is_empty()
            _args, _kwargs = _build_pipeline_parameter(is_sub_pipeline, func, args, kwargs)
            # We use this stack to store the dsl pipeline definition hierarchy
            _definition_builder_stack.push(self)
            try:
                # Set profile to get the variable name inside pipeline given by user.
                sys.setprofile(tracer)
                outputs = func(*_args, **_kwargs)
                sys.setprofile(original_profiler)
            except RecursionError as e:
                cycles = PipelineValidator.validate_pipeline_cycle(_definition_builder_stack)
                raise PipelineValidationError(
                    message="Detected pipeline recursion, pipelines: {}".format(cycles),
                    error_type=PipelineValidationError.PIPELINE_RECURSION) from e
            finally:
                self._update_components_variable_names(_locals_data)
                # pop current pipeline definition builder out of stack
                _definition_builder_stack.pop()
                _definition_id_now_build.pop()
            if outputs is None:
                outputs = {}
            self._update_outputs(outputs)
            self._sort_inputs()
            self._correct_default_compute_target()
            self._correct_default_data_store()
            definition = self.create_definition(_use_dsl=True)
            self._component_definition = definition

            return definition

        definition = wrapper_func(**default_args)
        return definition

    def create_definition(self, _use_dsl=False) -> PipelineComponentDefinition:
        """Create pipeline component definition from pipeline component definition builder fields."""
        return PipelineComponentDefinition(
            id=self.id, name=self.name, components=self.components,
            components_variable_names=self.components_variable_names, workspace=self.workspace,
            inputs=self.inputs, outputs=self.outputs, parameters=self.parameters,
            outputs_mapping=self.outputs_mapping, description=self.description,
            components_args_matched_dict_list=self.components_args_matched_dict_list,
            parent_definition_id=self.parent_definition_id, from_module_name=self.from_module_name,
            pipeline_function_name=self.pipeline_function_name, default_compute_target=self.default_compute_target,
            default_datastore=self.default_datastore)

    @staticmethod
    def from_func(
            name, description, default_compute_target,
            default_datastore, func, parent_def_id=None
    ) -> 'PipelineComponentDefinitionBuilder':
        """Create a pipeline component definition builder from a func defined by dsl.pipeline."""
        builder = PipelineComponentDefinitionBuilder(
            name=name, description=description,
            parameters={p.name: p for p in list(signature(func).parameters.values())},
            default_compute_target=default_compute_target, default_datastore=default_datastore,
            from_module_name=func.__module__, pipeline_function_name=func.__name__, parent_definition_id=parent_def_id)
        # Use set attr to avoid pass self as func parameter incorrectly.
        builder.__setattr__('func', func)
        return builder

    @staticmethod
    def from_nodes(
            nodes=None, name=None, workspace=None, pipeline_outputs=None, description=None,
            default_compute_target=None, default_datastore=None) -> 'PipelineComponentDefinitionBuilder':
        """Create a pipeline component definition builder from several child component nodes."""
        if len(nodes) != len(set(nodes)):
            raise UserErrorException('Could not add duplicate nodes to pipeline.')

        builder = PipelineComponentDefinitionBuilder(
            name, description, workspace, default_compute_target, default_datastore)
        all_node_has_definition = True
        for node in nodes:
            builder.add_component(node)
            if node._definition is None:
                all_node_has_definition = False

        inputs_mapping = _resolve_node_inputs(nodes)
        builder.outputs_mapping = pipeline_outputs if pipeline_outputs is not None else {}
        builder.outputs = {}
        builder.inputs = {}
        if all_node_has_definition:
            builder.outputs = {
                _k: _v._owner._definition.outputs[_v._name].to_dict()
                for _k, _v in builder.outputs_mapping.items()}
            builder.inputs = {
                _k: _v._owner._definition.inputs[_v._name].to_dict()
                for _k, _v in inputs_mapping.items()}

        return builder


class _PipelineComponentDefinitionBuilderStack:
    def __init__(self):
        self.items = []

    def top(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def push(self, item):
        error_msg = "_PipelineComponentDefinitionBuilderStack only " \
                    "allows pushing `PipelineComponentDefinition` element"
        assert isinstance(item, PipelineComponentDefinitionBuilder), error_msg
        return self.items.append(item)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


_definition_builder_stack = _PipelineComponentDefinitionBuilderStack()
# This collection is used to record the id of definition in building,
#   so that we can get the value of parent definition id.
# Notice that a sub pipeline has parent_definition_id only when sub pipeline defined inside parent pipeline.
#   The sub pipeline which defined outside but created inside parent do not has parent_definition_id.
_definition_id_now_build = []


def _add_component_to_current_definition_builder(component):
    if _definition_builder_stack.size() > 0:
        _builder = _definition_builder_stack.top()
        _builder.add_component(component)


def _get_pipeline_parameter(key, value):
    # return value if it's already pipeline parameter
    if isinstance(value, PipelineParameter):
        return value
    return PipelineParameter(key, value, _auto_wrap_for_build=True)


def _build_sub_pipeline_parameter(func, args, kwargs):
    def wrap_arg_value(arg_name, arg):
        from azureml.data.abstract_dataset import AbstractDataset
        from azureml.data.data_reference import DataReference
        if isinstance(arg, Input) or isinstance(arg, Output) \
                or isinstance(arg, AbstractDataset) or isinstance(arg, DataReference) \
                or isinstance(arg, PipelineParameter):
            return Input(arg, arg_name)
        else:
            return _get_pipeline_parameter(arg_name, arg)

    # transform args
    transformed_args = []
    transformed_kwargs = {key: wrap_arg_value(key, value) for key, value in kwargs.items()}

    if func is None:
        assert args is None
        return transformed_args, transformed_kwargs

    def all_p(parameters):
        for value in parameters.values():
            yield value

    parameters = all_p(signature(func).parameters)
    for arg in args:
        transformed_args.append(wrap_arg_value(parameters.__next__().name, arg))
    # transform default values
    for left_args in parameters:
        if left_args.name not in transformed_kwargs.keys() and left_args.default is not Parameter.empty:
            transformed_kwargs[left_args.name] = wrap_arg_value(left_args.name, left_args.default)
    return transformed_args, transformed_kwargs


def _build_pipeline_parameter(is_sub_pipeline, func, args, kwargs):
    # if this is a sub pipeline, we will wrap the arg value with _InputBuilder
    # so that we can keep sub pipeline's ports to inside nodes' ports mapping
    kwargs = {} if kwargs is None else kwargs
    if is_sub_pipeline:
        return _build_sub_pipeline_parameter(func, args, kwargs)
    # transform args
    transformed_args = []

    # transform kwargs
    transformed_kwargs = {
        key: _get_pipeline_parameter(key, value)
        for key, value in kwargs.items()}

    def all_params(parameters):
        for value in parameters.values():
            yield value

    if func is None:
        assert args is None
        return transformed_args, transformed_kwargs

    parameters = all_params(signature(func).parameters)
    for arg in args:
        transformed_args.append(_get_pipeline_parameter(
            parameters.__next__().name, arg))
    # transform default values
    for left_args in parameters:
        if left_args.name not in transformed_kwargs.keys() and left_args.default is not Parameter.empty:
            transformed_kwargs[left_args.name] = _get_pipeline_parameter(left_args.name, left_args.default)
    return transformed_args, transformed_kwargs


def _get_component_args_matched_dict(empty_input_component):
    """
    Convert input param name from a pipeline parameter to component param name.

    e.g.
    def pipeline(param):
      pipeline2(param)
    def pipeline2(parameter): xxx
    then input param from args need to converted to parameter: param instead of param: param

    :return: Component matched args.
    :rtype: dict
    """
    _params = {_k: _v._get_internal_data_source()
               for _k, _v in empty_input_component.inputs.items() if _v._dset is not None}
    _params.update({_k: _v if not isinstance(_v, Input) else _v._get_internal_data_source()
                    for _k, _v in empty_input_component._parameter_params.items() if _k not in _params.keys()})
    match_dict = {}
    for _k, _v in _params.items():
        if not isinstance(_v, PipelineParameter):
            continue
        if _v.name in match_dict.keys():
            match_dict[_v.name] = match_dict[_v.name] + (_k,)
        else:
            match_dict[_v.name] = (_k,)
    return match_dict


def _resolve_node_inputs(nodes):
    """Setter method to set pipeline inputs."""
    all_pipeline_node_outputs = [output for node in nodes for output_name, output in node.outputs.items()]
    # append all nodes, since node with one output could be used as input as well
    all_pipeline_node_outputs.extend([node for node in nodes])
    # append all nodes' outputs, since node's outputs _AttrDict with one output could be used as input as well
    all_pipeline_node_outputs.extend([node.outputs for node in nodes])

    inputs = {}
    for node in nodes:
        for input_name, input in node.inputs.items():
            if input._dset and input._dset not in all_pipeline_node_outputs and \
                    not isinstance(input._dset, _GlobalDataset) and \
                    not isinstance(input._dset, _Dataset) and \
                    not isinstance(input._dset, DatasetConsumptionConfig) and \
                    not isinstance(input._dset, FileDataset):
                instance_id = node._id
                inputs[_unify_input_port_name(node.name, instance_id, input_name, input)] = \
                    _extract_input_port_value(input)
    return _AttrDict(**inputs)


def _unify_input_port_name(node_name, node_id, port_name, port_value):
    """Get input port's unified name.

    if the port is corresponded to a subgraph's pipeline parameter, take it as the parameter name
    otherwise, take it as {node_name}:{port_name}

    :param node_name: name of the node where the port is
    :type node_name: str
    :param node_id: id of the node where the port is
    :type node_id: str
    :param port_name: port's name
    :type port_name: str
    :param port_value: the port's input
    :type: obj
    """
    if isinstance(port_value, Input):
        # if it is _InputBuilder type, that means it comes from a subgraph's pipeline parameter
        if isinstance(port_value._dset, Input):
            return port_value._dset.name
        elif isinstance(port_value._dset, _GlobalDataset):
            return '{}_{}'.format(port_value._dset.data_reference_name, node_id)
        elif isinstance(port_value._dset, _Dataset):
            return '{}_{}'.format(port_value._dset.name, node_id)
        elif isinstance(port_value._dset, PipelineParameter):
            return port_value._dset.name
        else:
            return '{}:{}'.format(node_name, port_name)
    else:
        return '{}:{}'.format(node_name, port_name)


def _extract_input_port_value(port_value):
    """Extract the underlying _InputBuilder.

    This is needed when the input comes from sub graph's pipeline parameter

    :param port_value: the port's input
    :type port_value: obj
    """
    if isinstance(port_value, Input):
        if isinstance(port_value._dset, Input):
            return port_value._dset
        else:
            return port_value
    else:
        return port_value
