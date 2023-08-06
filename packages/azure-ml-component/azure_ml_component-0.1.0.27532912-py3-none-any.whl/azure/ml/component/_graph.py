# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import uuid
from typing import List

from azureml.core.compute import AmlCompute, ComputeInstance, RemoteCompute, HDInsightCompute
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig

from azure.ml.component._util._attr_dict import _AttrDict
from azure.ml.component._util._utils import _get_dataset_def_from_dataset
from azureml.data._dataset import _Dataset
from azureml.exceptions import UserErrorException

from .component import Component, Input, Output
from ._module_dto import _python_type_to_type_code
from ._pipeline_data import PipelineData
from ._pipeline_parameters import PipelineParameter
from ._dataset import _GlobalDataset
from ._restclients.designer.models import GraphDraftEntity, GraphModuleNode, GraphDatasetNode, \
    GraphEdge, ParameterAssignment, PortInfo, DataSetDefinition, EntityInterface, Parameter, DataPathParameter, \
    OutputSetting, GraphModuleNodeRunSetting, RunSettingParameterAssignment, ComputeSetting, \
    RunSettingUIWidgetTypeEnum, ComputeType, MlcComputeInfo


def _topology_sort_nodes(nodes: List[Component]):
    """
    Sort the modules in the topological order
    If there has circlular dependencies among the modules, the returned list order is not assured

    :param: nodes: list of modules
    :type nodes: List[Module]
    :return list of modules in topological order
    : rtype: List[Module]
    """
    from .pipeline import Pipeline

    node_len = len(nodes)
    if node_len == 0:
        return []

    output_to_module = {}
    visted = {}
    stack = []
    for node in nodes:
        visted[node] = False
        for output in node.outputs.values():
            output_to_module[output] = node

    def get_dependencies(node, visted):
        dependencies = []
        for input in node.inputs.values():
            if isinstance(input, Input):
                dset = input._get_internal_data_source()
                if isinstance(dset, Output):
                    if dset in output_to_module.keys():
                        dependencies.append(output_to_module[dset])
                elif isinstance(dset, Component) or isinstance(dset, Pipeline):
                    for output in dset.outputs.values():
                        if isinstance(output, Output) and output in output_to_module.keys():
                            dependencies.append(output_to_module[output])
                elif isinstance(dset, _AttrDict):
                    for output in dset.values():
                        if isinstance(output, Output) and output in output_to_module.keys():
                            dependencies.append(output_to_module[output])
        return [d for d in dependencies if not visted[d]]

    result = []
    for node in nodes:
        if not visted[node]:
            visted[node] = True
            stack.append(node)
            while len(stack) != 0:
                cur = stack[-1]
                dependencies = get_dependencies(cur, visted)
                if (len(dependencies) == 0):
                    result.append(cur)
                    stack.pop()
                else:
                    for d in dependencies:
                        if not visted[d]:
                            stack.append(d)
                            visted[d] = True

    return result


class _GraphEntityBuilderContext(object):
    def __init__(self, compute_target=None, pipeline_parameters=None, pipeline_regenerate_outputs=None,
                 module_nodes=None, workspace=None, default_datastore=None):
        """
        Init the context needed for graph builder.

        :param compute_target: The compute target.
        :type compute_target: tuple(name, type)
        :param pipeline_parameters: The pipeline parameters.
        :type pipeline_parameters: dict
        :param pipeline_regenerate_outputs: the `regenerate_output` value of all module node
        :type pipeline_regenerate_outputs: bool
        """
        self.compute_target = compute_target
        # Copy pipeline parameters here because after build graph, dataset parameters will be removed.
        self.pipeline_parameters = {} if pipeline_parameters is None else {**pipeline_parameters}
        self.pipeline_regenerate_outputs = pipeline_regenerate_outputs

        self.module_nodes = module_nodes
        self.workspace = workspace
        self.default_datastore = default_datastore


class _GraphEntityBuilder(object):
    """The builder that constructs SMT graph-related entities from `azure.ml.component.Component`."""
    DATASOURCE_PORT_NAME = 'data'

    def __init__(self, context: _GraphEntityBuilderContext):
        self._context = context
        self._modules = _topology_sort_nodes(context.module_nodes)
        self._nodes = {}
        self._input_nodes = {}
        self._data_path_parameter_input = {}
        self._dataset_parameter_keys = set()

    def build_graph_entity(self, is_local_run=False):
        """
        Build graph entity that can be used to create pipeline draft and pipeline run.

        Notice that context.pipeline_parameters will be modified after build,
            dataset parameters will be removed.
        :param is_local_run: whether module execute in local
        :type is_local_run: bool
        :return Tuple of (graph entity, module node run settings, dataset definition value assignments)
        :rtype tuple
        """

        graph_entity = GraphDraftEntity()
        module_node_to_graph_node_mapping = {}

        # Prepare the entity
        graph_entity.dataset_nodes = []
        graph_entity.module_nodes = []
        graph_entity.edges = []
        graph_entity.entity_interface = EntityInterface(parameters=[], data_path_parameters=[],
                                                        data_path_parameter_list=[])

        if self._context.compute_target is not None:
            default_compute_name, default_compute_type = self._context.compute_target
            graph_entity.default_compute = ComputeSetting(name=default_compute_name,
                                                          compute_type=ComputeType.mlc,
                                                          mlc_compute_info=MlcComputeInfo(
                                                              mlc_compute_type=default_compute_type))

        module_node_run_settings = []

        # Note that the modules must be sorted in topological order
        # So that the dependent outputs are built before we build the inputs_map
        for module in self._modules:
            module_node = self._build_graph_module_node(module,
                                                        self._context.pipeline_regenerate_outputs,
                                                        module_node_to_graph_node_mapping)
            graph_entity.module_nodes.append(module_node)
            self._nodes[module_node.id] = module_node

            # Note that outputs_map must be build for edges to have the correct producer information.
            outputs_map = module._build_outputs_map(
                producer=module_node, default_datastore=self._context.default_datastore)
            inputs_map = module._build_inputs_map()
            for input_name, i in inputs_map.items():
                edge = None
                if isinstance(i, DatasetConsumptionConfig) or isinstance(i, _GlobalDataset) \
                        or isinstance(i, PipelineParameter) or isinstance(i, DataReference):
                    dataset_node = self._get_or_create_dataset_node(graph_entity, module, i)
                    edge = self._produce_edge_dataset_node_to_module_node(input_name, dataset_node, module_node)
                elif isinstance(i, PipelineData):
                    edge = self._produce_edge_module_node_to_module_node(input_name, i, module_node)
                else:
                    raise ValueError("Invalid input type: {0}".format(type(i)))
                if edge is not None:
                    graph_entity.edges.append(edge)

            module_node_run_settings.append(
                self._produce_module_runsettings(module, module_node))

            self._update_module_node_params(graph_entity, module_node, module,
                                            inputs_map, outputs_map)

        self._update_data_path_parameter_list(graph_entity)
        setattr(graph_entity, 'module_node_to_graph_node_mapping', module_node_to_graph_node_mapping)

        remove_node_ids = self.resolve_empty_nodes(graph_entity)
        graph_entity.dataset_nodes = [node for node in graph_entity.dataset_nodes
                                      if node.id not in remove_node_ids]
        graph_entity.edges = [edge for edge in graph_entity.edges
                              if edge.source_output_port.node_id not in remove_node_ids]
        # Keep graph data path parameter order as original pipeline parameter order.
        graph_entity.entity_interface.data_path_parameter_list = \
            self.sort_parameter_order(graph_entity.entity_interface.data_path_parameter_list)
        graph_entity.entity_interface.parameters = \
            self.sort_parameter_order(graph_entity.entity_interface.parameters)

        return graph_entity, module_node_run_settings

    def sort_parameter_order(self, parameters_list):
        parameters = {_p.name: _p for _p in parameters_list}
        results = {_k: parameters[_k] for _k in self._context.pipeline_parameters.keys() if _k in parameters}
        results.update({_p.name: _p for _p in parameters_list if _p.name not in results})
        return list(results.values())

    def resolve_empty_nodes(self, graph_entity):
        remove_node_ids = []
        data_path_param_names = set(i.name for i in graph_entity.entity_interface.data_path_parameter_list
                                    if i.default_value is not None)
        for node in graph_entity.dataset_nodes:
            dataset_def = node.data_set_definition
            if dataset_def is None or (
                    dataset_def.value is None and dataset_def.parameter_name not in data_path_param_names):
                remove_node_ids.append(str(node.id))
        return set(remove_node_ids)

    def _produce_module_runsettings(self, module: Component, module_node: GraphModuleNode):

        use_default_compute = module.runsettings._use_default_compute

        # do not remove this, or else module_node_run_setting does not make a difference
        module_node.use_graph_default_compute = use_default_compute
        module_node_run_setting = GraphModuleNodeRunSetting()
        module_node_run_setting.module_id = module._identifier
        module_node_run_setting.node_id = module_node.id
        module_node_run_setting.step_type = module._definition._module_dto.module_entity.step_type
        module_node_run_setting.run_settings = []

        runsettings = module._runsettings
        k8srunsettings = module._k8srunsettings
        params_spec = runsettings._params_spec
        for param_name in params_spec:
            param = params_spec[param_name]
            if param.is_compute_target:
                compute_run_settings = []
                # Always add compute settings
                # Since module may use default compute, we don't have to detect this, MT will handle
                if k8srunsettings is not None:
                    for section_name in k8srunsettings._params_spec:
                        for compute_param in k8srunsettings._params_spec[section_name]:
                            compute_param_value = getattr(getattr(k8srunsettings, section_name),
                                                          compute_param.argument_name)
                            compute_run_settings.append(RunSettingParameterAssignment(name=compute_param.name,
                                                                                      value=compute_param_value,
                                                                                      value_type=0))
                compute_name = runsettings.target
                compute_type = None
                if isinstance(compute_name, tuple):
                    compute_name, compute_type = runsettings.target
                module_node_run_setting.run_settings.append(
                    RunSettingParameterAssignment(name=param.name, value=compute_name, value_type=0,
                                                  use_graph_default_compute=runsettings._use_default_compute,
                                                  mlc_compute_type=compute_type,
                                                  compute_run_settings=compute_run_settings))
            else:
                param_value = getattr(runsettings, param_name)
                module_node_run_setting.run_settings.append(
                    RunSettingParameterAssignment(name=param.name, value=param_value, value_type=0))
        return module_node_run_setting

    def _produce_edge_dataset_node_to_module_node(self, input_name, dataset_node, module_node):
        source = PortInfo(node_id=dataset_node.id, port_name=self.DATASOURCE_PORT_NAME)
        dest = PortInfo(node_id=module_node.id, port_name=input_name)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _produce_edge_module_node_to_module_node(self, input_name, pipeline_data: PipelineData, dest_module_node):
        source_module_node = pipeline_data._producer
        source = PortInfo(node_id=source_module_node.id, port_name=pipeline_data._port_name)
        dest = PortInfo(node_id=dest_module_node.id, port_name=input_name)
        return GraphEdge(source_output_port=source, destination_input_port=dest)

    def _get_or_create_dataset_node(self, graph_entity: GraphDraftEntity, module: Component, input):
        if input in self._input_nodes:
            return self._input_nodes[input]
        else:
            dataset_node = self._build_graph_datasource_node(input, module)
            self._input_nodes[input] = dataset_node
            self._nodes[dataset_node.id] = dataset_node
            graph_entity.dataset_nodes.append(dataset_node)
            return dataset_node

    def _build_graph_module_node(self, module: Component,
                                 pipeline_regenerate_outputs: bool,
                                 module_node_to_graph_node_mapping) -> GraphModuleNode:
        node_id = self._generate_node_id()
        regenerate_output = pipeline_regenerate_outputs \
            if pipeline_regenerate_outputs is not None else module.regenerate_output
        module_node = GraphModuleNode(id=node_id, module_id=module._identifier,
                                      regenerate_output=regenerate_output)
        module_node.module_parameters = []
        module_node.module_metadata_parameters = []
        module_node_to_graph_node_mapping[module._get_instance_id()] = node_id
        return module_node

    def _update_module_node_params(self, graph_entity: GraphDraftEntity, module_node: GraphModuleNode,
                                   module: Component, inputs_map, outputs_map):
        """Add module node parameters and update it with context.pipeline_parameters."""
        pipeline_parameters = self._context.pipeline_parameters
        node_parameters = module._get_default_parameters()
        node_pipeline_parameters = {}

        user_provided_params = module._build_params()

        for param_name, param_value in user_provided_params.items():
            # TODO: Use an enum for value_type
            if isinstance(param_value, Input):
                param_value = param_value._get_internal_data_source()
            if isinstance(param_value, PipelineParameter):
                # Notice that param_value.name != param_name here
                if pipeline_parameters is not None and len(pipeline_parameters) > 0 and \
                        param_value.name in pipeline_parameters:
                    # If parameter is from pipeline parameters, add as node pipeline parameters
                    #   to display the relationship.
                    value = pipeline_parameters[param_value.name]
                    node_pipeline_parameters[param_name] = param_value.name
                    exist = next((x for x in graph_entity.entity_interface.parameters
                                  if x.name == param_value.name), None) is not None
                    if not exist:
                        graph_entity.entity_interface.parameters.append(Parameter(
                            name=param_value.name,
                            default_value=value,
                            is_optional=False,
                            type=_python_type_to_type_code(type(value))))
                    if param_name in node_parameters:
                        del node_parameters[param_name]
                else:
                    node_parameters[param_name] = param_value.default_value
            else:
                node_parameters[param_name] = param_value

        for _, input in inputs_map.items():
            if input in self._data_path_parameter_input.values():
                continue
            if isinstance(input, PipelineParameter):
                self._data_path_parameter_input[input.name] = input

        self._batch_append_module_node_parameter(module_node, node_parameters)
        self._batch_append_module_node_pipeline_parameters(module_node, node_pipeline_parameters)

        module_node.module_output_settings = []
        for output in outputs_map.values():
            output_setting = OutputSetting(name=output.name, data_store_name=output.datastore.name,
                                           data_store_mode=output._output_mode,
                                           path_on_compute=output._output_path_on_compute,
                                           overwrite=output._output_overwrite,
                                           data_reference_name=output.name,
                                           dataset_registration=output._dataset_registration)
            module_node.module_output_settings.append(output_setting)

    def _update_data_path_parameter_list(self, graph_entity: GraphDraftEntity):
        """Update data path parameters with dataset parameters in context.pipeline_parameters."""
        def get_override_parameters_def(name, origin_val, pipeline_parameters):
            # Check if user choose to override with pipeline parameters
            if pipeline_parameters is not None and len(pipeline_parameters) > 0:
                for k, v in pipeline_parameters.items():
                    if k == name:
                        self._dataset_parameter_keys.add(k)
                        if isinstance(v, _GlobalDataset):
                            return _get_dataset_def_from_dataset(v)
                        elif isinstance(v, AbstractDataset):
                            v._ensure_saved(self._context.workspace)
                            return _get_dataset_def_from_dataset(v)
                        else:
                            raise UserErrorException('Invalid parameter value for dataset parameter: {0}'.format(k))

            return origin_val

        pipeline_parameters = self._context.pipeline_parameters
        for name, pipeline_parameter in self._data_path_parameter_input.items():
            dset = pipeline_parameter.default_value
            dataset_def = None

            if isinstance(dset, AbstractDataset):
                dset._ensure_saved(self._context.workspace)
                dset = dset.as_named_input(name)

            if isinstance(dset, DatasetConsumptionConfig):
                dataset_consumption_config = dset
                dataset = dataset_consumption_config.dataset
                dataset._ensure_saved(self._context.workspace)
                dataset_def = _get_dataset_def_from_dataset(dataset)

            if isinstance(dset, _GlobalDataset):
                dataset_def = _get_dataset_def_from_dataset(dset)
            dataset_def = get_override_parameters_def(name, dataset_def, pipeline_parameters)
            if dataset_def is not None:
                exist = next((x for x in graph_entity.entity_interface.data_path_parameter_list
                              if x.name == name), None) is not None
                if not exist:
                    graph_entity.entity_interface.data_path_parameter_list.append(DataPathParameter(
                        name=name,
                        default_value=dataset_def.value,
                        is_optional=False,
                        data_type_id='DataFrameDirectory'
                    ))

    def _batch_append_module_node_pipeline_parameters(self, module_node: GraphModuleNode, params):
        for k, v in params.items():
            param_assignment = ParameterAssignment(name=k, value=v, value_type=1)
            module_node.module_parameters.append(param_assignment)

    def _batch_append_module_node_parameter(self, module_node: GraphModuleNode, params):
        for k, v in params.items():
            param_assignment = ParameterAssignment(name=k, value=v, value_type=0)
            module_node.module_parameters.append(param_assignment)

    def _append_module_meta_parameter(self, module_node: GraphModuleNode, param_name, param_value):
        param_assignment = ParameterAssignment(name=param_name, value=param_value, value_type=0)
        module_node.module_metadata_parameters.append(param_assignment)

    def _build_graph_datasource_node(self, input, module: Component) -> GraphDatasetNode:
        node_id = self._generate_node_id()
        if isinstance(input, DatasetConsumptionConfig) and isinstance(input.dataset, _Dataset):
            input.dataset._ensure_saved(self._context.workspace)
            dataset_def = _get_dataset_def_from_dataset(input.dataset)
            data_node = GraphDatasetNode(id=node_id, data_set_definition=dataset_def)
            return data_node

        if isinstance(input, PipelineParameter):
            dataset_def = DataSetDefinition(data_type_short_name="DataFrameDirectory",
                                            parameter_name=input.name)
            return GraphDatasetNode(id=node_id, data_set_definition=dataset_def)

        if isinstance(input, _GlobalDataset) or isinstance(input, DataReference):
            dataset_def = _get_dataset_def_from_dataset(input)
            data_node = GraphDatasetNode(id=node_id, data_set_definition=dataset_def)
            return data_node

    @staticmethod
    def _extract_mlc_compute_type(target_type):
        if target_type == AmlCompute._compute_type or target_type == RemoteCompute._compute_type or \
                target_type == HDInsightCompute._compute_type or target_type == ComputeInstance._compute_type:
            if target_type == AmlCompute._compute_type:
                return 'AmlCompute'
            elif target_type == ComputeInstance._compute_type:
                return 'ComputeInstance'
            elif target_type == HDInsightCompute._compute_type:
                return 'Hdi'
        return None

    def _generate_node_id(self) -> str:
        """
        Generate an 8-character node Id.

        :return: node_id
        :rtype: str
        """
        guid = str(uuid.uuid4())
        id_len = 8
        while guid[:id_len] in self._nodes:
            guid = str(uuid.uuid4())

        return guid[:id_len]


def _int_str_to_run_setting_ui_widget_type_enum(int_str_value):
    return list(RunSettingUIWidgetTypeEnum)[int(int_str_value)]
