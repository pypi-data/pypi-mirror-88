# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, List, Any

from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.exceptions._azureml_exception import UserErrorException
from .component import Component, Input
from ._pipeline_data import PipelineData
from ._pipeline_parameters import PipelineParameter
from ._restclients.designer.models import SubPipelinesInfo, SubGraphPortInfo, PipelineGraph, DataInfo, \
    GraphDatasetNode, DataSetPathParameter, DataSetDefinitionValue, ModuleDto, ModuleEntity, GraphModuleNode
from ._util._utils import _sanitize_python_variable_name, _get_data_info_hash_id
from ._widgets._visualization_builder import _Port, _ComponentDef, _DataNode, _Component, \
    _SubGraphPort, _SubGraph, _SubPipelinesInfo


class VisualizationContext(object):
    """
    Provide visualization meta infos used to build the visualization dict.
    """

    def __init__(self, step_nodes: List[_Component], module_defs: List[_ComponentDef],
                 data_nodes: List[_DataNode] = None, module_node_to_graph_node_mapping: Dict[str, str] = None,
                 sub_pipelines_info: SubPipelinesInfo = None):
        self.step_nodes = step_nodes
        self.module_defs = module_defs
        self.data_nodes = data_nodes
        self.sub_pipelines_info = sub_pipelines_info
        # only used for unit test
        self.module_node_to_graph_node_mapping = module_node_to_graph_node_mapping

    @classmethod
    def from_pipeline_component(cls, pipeline_component: 'PipelineComponent',
                                module_node_to_graph_node_mapping: Dict[str, str],
                                pipeline_parameters: Dict[str, Any] = None,
                                sub_pipelines_info: SubPipelinesInfo = None,
                                support_local_dataset=False):
        """Build visualization context for pipeline from pipeline component.

        :param pipeline_component: The pipeline_component.
        :type pipeline_component: azure.ml.component.PipelineComponent.
        :param module_node_to_graph_node_mapping: module node instance id to graph node id mapping.
        :type module_node_to_graph_node_mapping: Dict[str, str].
        :param pipeline_parameters: An optional dictionary of pipeline parameter.
        :type pipeline_parameters: dict.
        :param sub_pipelines_info: the sub pipeline info.
        :type sub_pipelines_info: ._restclients.designer.models.SubPipelinesInfo.
        :param support_local_dataset: support local dataset or not.
        :type support_local_dataset: bool.
        :return: The visualization context.
        :rtype: azure.ml.component.VisualizationContext.
        """
        module_nodes, _ = pipeline_component._expand_pipeline_nodes()
        input_to_data_info_dict = pipeline_component._build_input_to_data_info_dict(module_nodes,
                                                                                    pipeline_parameters,
                                                                                    support_local_dataset)
        internal_input_to_data_info_dict = {}
        for k, v in input_to_data_info_dict.items():
            if isinstance(k, Input):
                k = k._build()

            if isinstance(k, DatasetConsumptionConfig):
                internal_input_to_data_info_dict[k.dataset] = v
            else:
                internal_input_to_data_info_dict[k] = v

        # construct data nodes
        data_nodes = []
        for di in input_to_data_info_dict.values():
            # use data info hash key as it's node id since we don't have one here
            node_id = _get_data_info_hash_id(di)
            data_nodes.append(_data_info_to_data_node(node_id, di))

        # construct module definitions
        module_defs = []
        for node in module_nodes:
            module_defs.append(_build_module_def_from_component_def(node))

        # construct step nodes
        module_to_step_dict = {}
        for node in module_nodes:
            node_id = module_node_to_graph_node_mapping[node._get_instance_id()]
            module_to_step_dict[node] = _build_step_node_from_module_node(node, node_id, pipeline_parameters)

        from ._graph import _topology_sort_nodes
        sorted_module_nodes = _topology_sort_nodes(module_nodes)
        for node in sorted_module_nodes:
            step = module_to_step_dict[node]
            # node._build_outputs_map(producer=node)
            inputs_map = node._build_inputs_map()
            for input_name, i in inputs_map.items():
                if isinstance(i, DatasetConsumptionConfig):
                    i = i.dataset
                if i in internal_input_to_data_info_dict.keys():
                    port = _Port(_get_data_info_hash_id(internal_input_to_data_info_dict[i]))
                    step.add_input_port(input_name, port)
                elif isinstance(i, PipelineData):
                    producder = i._producer
                    if isinstance(producder, Component):
                        source_step = module_to_step_dict[producder]
                    elif isinstance(producder, GraphModuleNode):
                        # this branch of logic should be removed when graph entity builder logic is removed
                        # or we don't need build output/input logic
                        source_step = _find_graph_module_node_step(module_nodes, module_to_step_dict, producder,
                                                                   module_node_to_graph_node_mapping)
                    else:
                        continue
                    source_port = _Port(source_step.id, i._port_name)
                    step.add_input_port(input_name, source_port)
                    source_step.add_output_port(i._port_name, source_port)
                else:
                    raise ValueError("Invalid input type: {0}".format(type(i)))

        return cls(step_nodes=module_to_step_dict.values(),
                   module_defs=module_defs,
                   data_nodes=data_nodes,
                   module_node_to_graph_node_mapping=module_node_to_graph_node_mapping,
                   sub_pipelines_info=_build_visual_sub_pipelines_info(sub_pipelines_info))

    @classmethod
    def from_run_graph(cls, run_graph: PipelineGraph, selected_node_id: str = None):
        """Build visualization context for pipeline run from its graph.

        :param run_graph: The pipeline graph for one pipeline run.
        :type run_graph: ._restclients.designer.models.PipelineGraph.
        :param selected_node_id: The node id of one step run.
         If specified, will only build visualization dict for the select step run,
         otherwise, will build visualization dict for the whole pipeline run.
        :type selected_node_id: str.
        :return: The visualization context.
        :rtype: azure.ml.component.VisualizationContext.
        """
        # construct data nodes
        data_nodes = []
        for node in run_graph.dataset_nodes:
            data_info = _get_data_node_referenced_data_source(node, run_graph.graph_data_sources,
                                                              run_graph.entity_interface.data_path_parameter_list)
            if data_info is not None:
                data_nodes.append(_data_info_to_data_node(node.id, data_info))
            elif node.data_set_definition is not None and node.data_set_definition.parameter_name is not None:
                data_nodes.append(_build_data_node_from_parameter(
                    node.data_set_definition.parameter_name,
                    node.id,
                    run_graph.entity_interface.data_path_parameter_list))
            else:
                data_info = _build_data_info_from_data_set_value(node.data_set_definition.value)
                data_nodes.append(_data_info_to_data_node(node.id, data_info))

        # construct step nodes
        step_nodes = []
        for node in run_graph.module_nodes:
            module_dto = next((dto for dto in run_graph.graph_module_dtos
                               if dto.module_version_id == node.module_id), None)
            assert module_dto is not None, 'no module dto found for node {}'.format(node.id)

            module_entity = next((entity for entity in run_graph.graph_modules
                                  if entity.id == node.module_id), None)
            assert module_dto is not None, 'no module entity found for node {}'.format(node.id)

            input_edges = [edge for edge in run_graph.edges
                           if edge.destination_input_port.node_id == node.id]
            output_edges = [edge for edge in run_graph.edges
                            if edge.source_output_port.node_id == node.id]

            inputs = {}
            for edge in input_edges:
                dest_port_name = edge.destination_input_port.port_name
                source_node_id = edge.source_output_port.node_id
                source_port_name = edge.source_output_port.port_name

                data_node = next((node for node in run_graph.dataset_nodes if node.id == source_node_id), None)
                if data_node is None:
                    inputs[dest_port_name] = _Port(node_id=source_node_id, port_name=source_port_name)
                else:
                    inputs[dest_port_name] = _Port(node_id=data_node.id)

            outputs = {}
            for edge in output_edges:
                source_port_name = edge.source_output_port.port_name
                outputs[source_port_name] = _Port(node_id=node.id, port_name=source_port_name)

            interface_params = [para.name for para in module_entity.structured_interface.parameters]
            parameters = {}
            for para in node.module_parameters:
                if para.name in interface_params:
                    parameters[para.name] = para.value

            step_nodes.append(_Component(
                id=node.id,
                inputs=inputs,
                outputs=outputs,
                parameters=parameters,
                module_identifier=node.module_id))

        # construct module definitions
        module_defs = []
        for dto in run_graph.graph_module_dtos:
            entity = next((entity for entity in run_graph.graph_modules
                           if entity.id == dto.module_version_id), None)
            module_defs.append(_build_module_def_from_module_dto(dto, entity))

        if selected_node_id is None:
            return cls(step_nodes=step_nodes,
                       module_defs=module_defs,
                       data_nodes=data_nodes,
                       sub_pipelines_info=_build_visual_sub_pipelines_info(run_graph.sub_pipelines_info))
        else:
            step_nodes = [step for step in step_nodes if step.id == selected_node_id]
            return cls(step_nodes=step_nodes,
                       module_defs=module_defs,
                       data_nodes=[])


# region helper_functions
def _get_data_node_referenced_data_source(node: GraphDatasetNode, data_sources: List[DataInfo],
                                          data_path_parameter_list: List[DataSetPathParameter]):
    if node.data_set_definition:
        # first try to get data set definition from data node directly
        def_val = node.data_set_definition.value
        # if not exist, try to get data set definition from data_path_parameter_list
        if def_val is None and node.data_set_definition.parameter_name is not None:
            para_name = node.data_set_definition.parameter_name
            def_val = next((x.default_value for x in data_path_parameter_list if x.name == para_name), None)

        if def_val is not None:
            if def_val.data_set_reference is not None:
                dataset_id = def_val.data_set_reference.id
                source = next((s for s in data_sources if s.id == dataset_id), None)
            elif def_val.saved_data_set_reference is not None:
                saved_dataset_id = def_val.saved_data_set_reference.id
                source = next((s for s in data_sources if s.saved_dataset_id == saved_dataset_id), None)
            elif def_val.literal_value is not None:
                literal_value = def_val.literal_value
                source = next((s for s in data_sources if s.aml_data_store_name == literal_value.data_store_name and
                               s.relative_path == literal_value.relative_path), None)
            else:
                source = None
    elif node.dataset_id is not None:
        source = next((s for s in data_sources if s.id == node.dataset_id), None)
    else:
        source = None

    return source


def _data_info_to_data_node(node_id: str, data_info: DataInfo) -> _DataNode:
    return _DataNode(name=data_info.name,
                     node_id=node_id,
                     data_id=_get_data_info_hash_id(data_info),
                     description=data_info.description,
                     path_on_datastore=data_info.relative_path,
                     datastore=data_info.aml_data_store_name,
                     version=data_info.dataset_version_id,
                     reg_id=data_info.id,
                     saved_id=data_info.saved_dataset_id)


def _build_data_node_from_parameter(para_name: str,
                                    node_id: str,
                                    data_path_parameter_list: List[DataSetPathParameter]) -> _DataNode:
    exist = next((x for x in data_path_parameter_list if x.name == para_name), None)
    if exist is not None and exist.default_value is not None:
        data_info = _build_data_info_from_data_set_value(exist.default_value)
    else:
        data_info = DataInfo(name=para_name, dataset_type='parameter')

    return _data_info_to_data_node(node_id, data_info)


def _build_data_info_from_data_set_value(value: DataSetDefinitionValue) -> DataInfo:
    if value.data_set_reference is not None:
        return DataInfo(id=value.data_set_reference.id,
                        name=value.data_set_reference.name)
    elif value.saved_data_set_reference is not None:
        return DataInfo(saved_dataset_id=value.saved_data_set_reference.id,
                        name='saved_dataset_' + value.saved_data_set_reference.id)
    elif value.literal_value is not None:
        return DataInfo(aml_data_store_name=value.literal_value.data_store_name,
                        relative_path=value.literal_value.relative_path,
                        name=_sanitize_python_variable_name(value.literal_value.relative_path))
    else:
        raise UserErrorException("Invalid data set definition value.")


def _build_module_def_from_module_dto(module_dto: ModuleDto, entity: ModuleEntity = None) -> _ComponentDef:
    if entity is None:
        entity = module_dto.module_entity

    inputs = []
    for input in entity.structured_interface.inputs:
        inputs.append(
            {'name': input.name,
             'label': input.label,
             'data_type_ids_list': input.data_type_ids_list})

    outputs = []
    for output in entity.structured_interface.outputs:
        outputs.append({'name': output.name, 'label': output.label, 'data_type_id': output.data_type_id})

    return _ComponentDef(identifier=entity.id,
                         name=module_dto.module_name,
                         display_name=module_dto.display_name,
                         version=module_dto.module_version,
                         description=module_dto.description,
                         inputs=inputs,
                         outputs=outputs)


def _build_module_def_from_component_def(component: Component) -> _ComponentDef:
    component_def = component._definition
    inputs = []
    for v in component_def.inputs.values():
        inputs.append(
            {'name': v.name, 'label': v.name, 'data_type_ids_list': [v.type]})

    outputs = []
    for v in component_def.outputs.values():
        outputs.append(
            {'name': v.name, 'label': v.name, 'data_type_id': v.type})

    return _ComponentDef(identifier=component_def.identifier,
                         name=component_def.name,
                         display_name=component_def.display_name,
                         version=component_def.version,
                         description=component_def.description,
                         inputs=inputs,
                         outputs=outputs)


def _build_step_node_from_module_node(module: Component, node_id, pipeline_parameters) -> _Component:
    module_identifier = module._identifier
    parameters = module._get_default_parameters()
    validation_info = module._validate(raise_error=False, pipeline_parameters=pipeline_parameters)

    user_provided_params = module._build_params()
    for param_name, param_value in user_provided_params.items():
        if param_name in parameters.keys():
            value = param_value
            if isinstance(param_value, PipelineParameter):
                value = param_value.default_value
                # check if it is override in provided pipeline parameters
                if pipeline_parameters is not None:
                    for k, v in pipeline_parameters.items():
                        if k == param_value.name:
                            value = v
                parameters.update({param_name: value})
            elif isinstance(param_value, Input):
                internal_data = param_value._get_internal_data_source()
                value = internal_data.default_value if isinstance(internal_data, PipelineParameter) else internal_data
                parameters.update({param_name: value})

            parameters.update({param_name: value})

    return _Component(id=node_id,
                      inputs={},
                      outputs={},
                      parameters=parameters,
                      module_identifier=module_identifier,
                      validation_info=validation_info)


def _build_visual_sub_graph_port(port: SubGraphPortInfo) -> _SubGraphPort:
    return _SubGraphPort(name=port.name,
                         internal=[_Port(i.node_id, i.port_name) for i in port.internal],
                         external=[_Port(e.node_id, e.port_name) for e in port.external])


def _build_visual_sub_pipelines_info(sub_pipelines_info: SubPipelinesInfo) -> _SubPipelinesInfo:
    # check if sub pipeline info is valid
    if sub_pipelines_info is None or sub_pipelines_info.sub_graph_info is None:
        return None

    sub_graphs = []
    for graph in sub_pipelines_info.sub_graph_info:
        sub_graph = _SubGraph(id=graph.id, name=graph.name, parent_graph_id=graph.parent_graph_id,
                              inputs=[_build_visual_sub_graph_port(p) for p in graph.inputs],
                              outputs=[_build_visual_sub_graph_port(p) for p in graph.outputs])
        sub_graphs.append(sub_graph)

    return _SubPipelinesInfo(sub_graphs, sub_pipelines_info.node_id_to_sub_graph_id_mapping)


def _find_graph_module_node_step(module_nodes, module_to_step_dict, graph_node, module_node_to_graph_node_mapping):
    module_instance_id = None
    for k, v in module_node_to_graph_node_mapping.items():
        if v == graph_node.id:
            module_instance_id = k
    if module_instance_id is None:
        return None

    module_node = next((node for node in module_nodes if node._get_instance_id() == module_instance_id), None)
    return module_to_step_dict[module_node]
# endregion
