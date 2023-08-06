# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains classes for creating and managing reusable computational units of an Azure Machine Learning pipeline.

An Azure Machine Learning pipeline is an independently executable workflow of a complete machine learning task.
Azure Machine Learning pipelines help you build, optimize, and manage machine learning workflows with simplicity,
repeatability and quality assurance.

A pipeline can be composited by several Components.

These benefits become significant as soon as your machine learning project moves beyond pure exploration and into
iteration. Even simple one-step pipelines can be valuable. Machine learning projects are often in a complex state,
and it can be a relief to make the precise accomplishment of a single workflow a trivial process.

"""
import os
from inspect import Parameter
from pathlib import Path
import tempfile
import uuid
from typing import List, Union, Mapping, Callable, Dict, Any

from azureml.core import Datastore, Experiment
from azureml.data._dataset import _Dataset
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data.abstract_dataset import AbstractDataset
from azureml.exceptions._azureml_exception import UserErrorException

from ._core._io_definition import ParameterDefinition
from .component import Component, Output, Input
from .run import Run
from ._pipeline_parameters import PipelineParameter
from ._pipeline_component_definition_builder import PipelineComponentDefinitionBuilder, \
    _add_component_to_current_definition_builder, _definition_builder_stack, _build_pipeline_parameter, \
    _extract_input_port_value, _unify_input_port_name
from ._dataset import _GlobalDataset
from ._execution._pipeline_run_orchestrator import _orchestrate_pipeline_run, STEP_PREFIX, NODE_ID, WORKING_DIR, \
    trans_node_name
from ._execution._tracker import RunHistoryTracker
from ._pipeline_data import PipelineData
from ._graph import _GraphEntityBuilder, _GraphEntityBuilderContext
from ._component_validator import ComponentValidator
from ._visible import Visible
from ._visualization_context import VisualizationContext
from ._pipeline_validator import PipelineValidator
from ._published_pipeline import PublishedPipeline
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._restclients.designer.models import SubmitPipelineRunRequest, PipelineDraft, \
    CreatePublishedPipelineRequest, DataInfo
from ._util._attr_dict import _AttrDict
from ._util._exceptions import PipelineValidationError
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._telemetry import WorkspaceTelemetryMixin, _get_telemetry_value_from_pipeline_parameter
from ._util._utils import _get_short_path_name, _is_prod_workspace, _can_visualize

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class Pipeline(Component, Visible, WorkspaceTelemetryMixin):
    """A Pipeline aggregates other Components and connects their inputs and outputs to form a pipeline."""

    def __init__(self, nodes: List[Union[Component, 'Pipeline']],
                 outputs: Mapping[str, Output] = None,
                 workspace=None, name=None, description=None,
                 default_compute_target=None, default_datastore=None, _use_dsl=False,
                 _definition=None, _init_params=None, _is_direct_child=True):
        """
        Initialize Pipeline.

        :param nodes: The nodes of component used to create the pipeline.
        :type nodes: list[azure.ml.component.Component
            or azure.ml.component.Pipeline]
        :param outputs: The pipeline outputs.
        :type outputs: dict
        :param workspace: The workspace of the pipeline
        :type workspace: azureml.core.Workspace
        :param name: The name of the pipeline
        :type name: str
        :param description: The description of the pipeline
        :type description: str
        :param default_compute_target: The compute target name of built pipeline.
            The priority of compute target assignment goes: module's run settings >
            sub pipeline's default compute target > parent pipeline's default compute target.
        :type default_compute_target: str
        :param default_datastore: The default datastore of pipeline.
        :type default_datastore: str or azureml.core.Datastore
        :param _use_dsl: Whether created by @dsl.pipeline
        :type _use_dsl: bool
        :param _definition: the definition of pipeline component
        :type _definition: _PipelineComponentDefinition
        :param _init_params: the pipeline parameters from input
        :type _init_params: dict
        :param _is_direct_child: If there is a pipeline component definition
            is_direct_child means whether the component is current definition's direct child.
        :type _is_direct_child: bool
        """
        _init_params = {} if _init_params is None else _init_params

        if outputs is None:
            outputs = {}
        if _definition is None:
            _definition = PipelineComponentDefinitionBuilder.from_nodes(
                nodes=nodes, name=name, workspace=workspace, pipeline_outputs=outputs,
                description=description, default_compute_target=default_compute_target,
                default_datastore=default_datastore).create_definition()
        self._definition = _definition
        # If current pipeline not direct child from a definition component(child node of direct_child)
        # or definition stack is not empty, then it is a sub pipeline.
        self._is_sub_pipeline = not _is_direct_child or not _definition_builder_stack.is_empty()
        self._init_params = _init_params
        self._workspace = _definition.workspace
        self._description = description
        self._instance_id = str(uuid.uuid4())

        _copied_id_field = '_copied_id'
        if not _use_dsl:
            self.nodes = list(self._definition.components.values())
            self._outputs = _AttrDict(**outputs)
            self._parameter_params = _init_params
        else:
            self.nodes = self._copy_nodes(
                nodes, _copied_id_field, **_init_params)
            self._copy_outputs(outputs, _copied_id_field)

        self._set_inputs()
        # Note self.workspace is only available after self.nodes is set.
        WorkspaceTelemetryMixin.__init__(self, workspace=self.workspace)
        self._default_datastore = default_datastore
        self._default_compute_target = default_compute_target
        self._name = name if name is not None else self._definition.name
        self._description = description
        self._parent = None
        self._resolve_node_id_variable_name_dict()
        self._validate_parameters(self._init_params)

        self._use_dsl = _use_dsl

        from ._sub_pipeline_info_builder import _build_sub_pipeline_definition
        all_parameters = list(_definition._parameters.values())
        all_parameters.extend([ParameterDefinition(name=i.name, type=i.type) for i in _definition._inputs.values()])
        self._pipeline_definition = _build_sub_pipeline_definition(
            name=self._name, description=self._description,
            default_compute_target=_definition._default_compute_target,
            default_data_store=default_datastore, id=_definition._id,
            parent_definition_id=_definition._parent_definition_id,
            from_module_name=_definition._from_module_name,
            parameters=all_parameters,
            func_name=_definition._pipeline_function_name)

        # correct sub pipelines filed `is_sub_pipeline`
        for node in self.nodes:
            if isinstance(node, Pipeline):
                node._is_sub_pipeline = True
                node._parent = self

        if _is_direct_child:
            _add_component_to_current_definition_builder(self)

    @property
    def name(self):
        """
        Get or set the name of the Pipeline.

        :return: The name.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        """
        Get or set the description of the Pipeline.

        :return: The description.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def inputs(self):
        """
        Get the inputs of the Pipeline.

        :return: pipeline inputs.
        :rtype: dict
        """
        return self._inputs

    @property
    def outputs(self):
        """
        Get the outputs of the Pipeline.

        :return: pipeline outputs.
        :rtype: dict
        """
        return self._outputs

    @property
    def workspace(self):
        """
        Get the workspace of the Pipeline.

        This will check if all nodes in pipeline are from the same workspace.

        :return: The workspace.
        :rtype: azureml.core.Workspace
        """
        for node in self.nodes:
            new_workspace = node.workspace
            if new_workspace is None:
                continue

            if self._workspace is None:
                self._workspace = new_workspace
            else:
                is_same_workspace = self._workspace._workspace_id == new_workspace._workspace_id
                if not is_same_workspace:
                    raise UserErrorException(
                        'Not all pipeline nodes are from the same workspace: {}, {}'.format(
                            self._workspace, new_workspace
                        ))

        return self._workspace

    def _get_instance_id(self):
        return self._id

    @property
    def default_datastore(self):
        """
        Get the default datastore of the Pipeline.

        :return: the default datastore.
        :rtype: azureml.core.Datastore
        """
        if self._default_datastore is None or isinstance(self._default_datastore, str):
            ws = self.workspace
            if isinstance(self._default_datastore, str) and ws is not None:
                self._default_datastore = Datastore(ws, name=self._default_datastore)
            elif ws is not None:
                service_caller = _DesignerServiceCallerFactory.get_instance(ws)
                self._default_datastore = service_caller.get_default_datastore()
        return self._default_datastore

    def _resolve_node_id_variable_name_dict(self):
        """
        Resolve node id to variable name dict.

        This dict is used to store variable name definied by user
            inside dsl.pipeline function, for example, `p1=pipeline()`,
            then p1 is the variable name of the pipeline node.
        """
        components_names = self._definition._components_variable_names
        self._node_id_variable_name_dict = {}
        if len(components_names) != len(self.nodes):
            return
        self._node_id_variable_name_dict = {
            node._id: components_names[idx]
            for idx, node in enumerate(self.nodes) if components_names[idx] is not None}

    def _copy_nodes(self, original_nodes, _copied_id_field, **kwargs):
        """
        Copy nodes of original nodes with new input kwargs.

        Direct child of pipeline is copied from definition component.
        Children of child is copied from definition components' nodes.
        """
        nodes = []

        # Add default parameter if is creating a root pipeline
        if not self._is_sub_pipeline:
            kwargs.update({
                name: param.default for name, param in self._definition.parameters.items()
                if name not in kwargs.keys() and param.default is not Parameter.empty})
        self._parameter_params = {_k: _v for _k, _v in kwargs.items() if _k in self._definition.parameters}

        # Wrap args with PipelineParameter/InputBuilder
        _, kwargs = _build_pipeline_parameter(
            is_sub_pipeline=self._is_sub_pipeline, func=None, args=None, kwargs=kwargs)

        def copy_params(_kwargs, param_dict, old_to_new_dict):
            """Copy params in param dict to kwargs, replace the input/output builder to the correct one."""
            def update_value(value):
                _value = value
                # Replace pipeline data with the new one
                if isinstance(_value, Output):
                    # Only dsl pipeline will reach here and nodes already topology sorted,
                    #   indicates that the inputs of node must exists inside(replace) or outside(not replace).
                    if _value._owner._id in old_to_new_dict.keys():
                        _value = old_to_new_dict[_value._owner._id].outputs[_value._name]
                elif isinstance(_value, Input):
                    if _value._owner is not None:
                        _value = old_to_new_dict[_value._owner._id].inputs[_value._name]
                elif isinstance(_value, Component):
                    # Only dsl pipeline will reach here and nodes already topology sorted,
                    #   indicates that the inputs of node must exists inside(replace) or outside(not replace).
                    if _value._id in old_to_new_dict.keys():
                        _value = old_to_new_dict[_value._id]
                return _value

            for _k, _v in param_dict.items():
                if _k in _kwargs.keys():
                    continue
                value = update_value(_v) if not isinstance(_v, dict) \
                    else {key: update_value(val) for key, val in _v.items() if update_value(val) is not None}
                _kwargs[_k] = value

        def get_old_to_new_dict(comp):
            """Get the dict of original node id to copy node."""
            pipeline_nodes, _ = comp._expand_pipeline_nodes()
            _dict = {
                getattr(node, _copied_id_field): node
                for node in pipeline_nodes if hasattr(node, _copied_id_field)}
            _dict.update({
                getattr(node, _copied_id_field): node
                for node in comp._expand_pipeline_to_pipelines() if hasattr(node, _copied_id_field)})
            return _dict

        def convert_component_kwargs(_index, _kwargs, matched_dict_list):
            """Convert pipeline parameters to the matched input of components."""
            updated_kwargs = {}
            for _k, _v in _kwargs.items():
                if _k not in matched_dict_list[_index].keys():
                    continue
                updated_kwargs.update({
                    _name: _v for _name in list(matched_dict_list[_index][_k])})
            return updated_kwargs

        def copy_component_init(node):
            """
            Create a component with new kwargs and the same _init_params of node.

            Notice that configuration added using .configure() includes
                runsetting, inputs and parameters will not be added here.
            """
            sub_definition = original_node._definition
            # Convert arg keys to new keys by using match dict in definition
            _kwargs = convert_component_kwargs(
                _index, kwargs, self._definition._components_args_matched_dict_list)

            # Add default parameter from component definition
            component_default_args = original_node._init_params
            copy_params(_kwargs, component_default_args, old_to_new_dict)
            if isinstance(node, Pipeline):
                _c = Pipeline(
                    nodes=node.nodes, outputs=node.outputs, name=node.name, description=node.description,
                    _definition=sub_definition, workspace=node.workspace, _use_dsl=True,
                    default_datastore=node._default_datastore, default_compute_target=node._default_compute_target,
                    _init_params=_kwargs, _is_direct_child=False)
                old_to_new_dict.update(get_old_to_new_dict(_c))
            else:
                _c = Component(sub_definition, _init_params=_kwargs, _is_direct_child=False)
            return _c

        def update_component_extra_settings(_pipeline_parameters, complete_node, unfinished_node):
            """Update extra input/parameter/run settings of new node."""
            updated_inputs = {}
            # Replace inputs with the correct one of new node if output builder
            copy_params(updated_inputs, complete_node._extra_input_settings, old_to_new_dict)
            # Update input value if is pipelineparameter auto wrapped
            # e.g.
            # @dsl.pipeline
            # def pipeline(param):
            #   comp = func()
            #   comp.set_inputs(a=param)
            # Here we will give param a default value None when build pipeline definition,
            #   so the comp._extra_input_settings will be PipelineParameter('param', None).
            # Then we build a real pipeline 'pipeline(param=1)',
            #   the comp._extra_input_settings should be updated to PipelineParameter('param', 1).
            for _k, _v in updated_inputs.items():
                value = _v._get_internal_data_source() if isinstance(_v, Input) else _v
                if isinstance(value, PipelineParameter) and value._auto_wrap_for_build:
                    updated_inputs[_k] = _pipeline_parameters[_v.name]
            unfinished_node.set_inputs(**updated_inputs)
            if complete_node._specify_runsettings:
                unfinished_node.runsettings.configure(**complete_node._extra_runsettings)
                unfinished_node._specify_runsettings = True

            # Update outputs _dataset_registration parameter
            for name, output in complete_node.outputs.items():
                unfinished_node.outputs[name]._dataset_registration = output._dataset_registration

        # Used to replace component inside output builder to new component
        old_to_new_dict = {}
        for _index, original_node in enumerate(original_nodes):
            _id = original_node._id
            component = copy_component_init(original_node)
            setattr(component, _copied_id_field, _id)
            old_to_new_dict[_id] = component
            nodes += (component,)

        # Copy extra inputs/parameters config and run settings
        for original_node, node in zip(original_nodes, nodes):
            if isinstance(node, Pipeline):
                continue
            update_component_extra_settings(kwargs, original_node, node)

        return nodes

    def _set_inputs(self):
        """Map original inputs to new to set pipeline inputs."""
        all_pipeline_node_outputs = [output for node in self.nodes for output_name, output in node.outputs.items()]
        # append all nodes, since node with one output could be used as input as well
        all_pipeline_node_outputs.extend([node for node in self.nodes])
        # append all nodes' outputs, since node's outputs _AttrDict with one output could be used as input as well
        all_pipeline_node_outputs.extend([node.outputs for node in self.nodes])

        inputs = {}
        for node in self.nodes:
            for input_name, input in node.inputs.items():
                if input._dset and input._dset not in all_pipeline_node_outputs and \
                        not isinstance(input._dset, _GlobalDataset) and \
                        not isinstance(input._dset, _Dataset) and \
                        not isinstance(input._dset, DatasetConsumptionConfig) and \
                        not isinstance(input._dset, AbstractDataset):
                    instance_id = node._id
                    name = _unify_input_port_name(node.name, instance_id, input_name, input)
                    if name not in self._definition.inputs and name not in self._definition.parameters:
                        continue
                    inputs[name] = \
                        _extract_input_port_value(input)
        self._inputs = _AttrDict(**inputs)

    def _copy_outputs(self, _original_outputs, _copied_id_field):
        """Map original outputs to new to set pipeline inputs."""
        all_nodes, _ = self._expand_pipeline_nodes()
        old_to_new_dict = {getattr(node, _copied_id_field): node
                           for node in all_nodes if hasattr(node, _copied_id_field)}
        for output in _original_outputs.values():
            if output._owner._id not in old_to_new_dict.keys():
                raise UserErrorException('Component node inside Pipeline must be created'
                                         ' inside dsl.pipeline function. node {}'.format(output._owner.name))
        # Use original outputs owner id to find new owners' outputs port
        outputs = {_k: old_to_new_dict[_v._owner._id]._outputs[_v._name]
                   for _k, _v in _original_outputs.items()}
        self._outputs = _AttrDict(**outputs)

    def _get_default_compute_target(self, default_compute_target=None):
        """
        Try to resolve the default compute target to tuple(compute_name, compute_type).

        :param default_compute_target
        :type str or AmlCompute or tuple(str, str)
        :return:
        """
        if default_compute_target is None:
            default_compute_target = self._default_compute_target

        if default_compute_target is None:
            return None, "AmlCompute"

        # try to resolve compute target
        if isinstance(default_compute_target, str):
            if self.workspace is None:
                # this should only happens in dsl pipeline, when we initialize a Pipeline with no nodes
                return default_compute_target, "AmlCompute"
            target = self._get_compute_in_workspace_by_name(default_compute_target)
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

    def _get_compute_in_workspace_by_name(self, compute_name: str):
        """
        Get compute by name. Return None if compute does not exist in current workspace.

        :param compute_name
        :type str
        :return: compute
        :rtype: ~designer.models.ExperimentComputeMetaInfo or None
        """
        service_caller = _DesignerServiceCallerFactory.get_instance(self.workspace)
        return service_caller.get_compute_by_name(compute_name)

    @track(_get_logger, activity_type=_PUBLIC_API, flush=True)
    def submit(self, experiment_name=None, default_compute_target=None, description=None, pipeline_parameters=None,
               tags=None, continue_on_step_failure=None, regenerate_outputs=None, skip_validation=False) \
            -> Run:
        """
        Submit current pipeline run to workspace.

        :param experiment_name: The experiment name, if experiment_name is None will default to pipeline name
        :type experiment_name: str
        :param default_compute_target: The default compute target used to run pipeline
        :type default_compute_target: str
        :param description: The description of the submitted pipeline run
        :type description: str
        :param pipeline_parameters: An optional dictionary of pipeline parameter assignments for the PipelineDraft
        :type pipeline_parameters: dict({str:str})
        :param tags: Tags to be added to the submitted run, {"tag": "value"}
        :type tags: dict
        :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
            If True, only steps that have no dependency on the output of the failed step will continue execution.
        :type continue_on_step_failure: bool
        :param regenerate_outputs: Indicates whether to force regeneration of all step outputs and disallow data
            reuse for this run. If False, this run may reuse results from previous runs and subsequent runs may reuse
            the results of this run.
        :type regenerate_outputs: bool
        :param skip_validation: Set this parameter True to skip pipeline validation triggered before submit.
        :type skip_validation: bool

        :return: The submitted run.
        :rtype: azure.ml.component.Run
        """
        workspace = self.workspace
        default_compute_target = self._get_default_compute_target(default_compute_target)
        # _parameter_params should also added, or else component parameter will be treated as constants.
        pipeline_parameters = self._expand_default_pipeline_parameters(pipeline_parameters)

        module_nodes, _ = self._expand_pipeline_nodes()
        graph_builder_context = _GraphEntityBuilderContext(compute_target=default_compute_target,
                                                           pipeline_parameters=pipeline_parameters,
                                                           pipeline_regenerate_outputs=regenerate_outputs,
                                                           module_nodes=module_nodes,
                                                           workspace=workspace,
                                                           default_datastore=self.default_datastore)

        graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
        graph, module_node_run_settings = graph_entity_builder.build_graph_entity()

        input_to_data_info_dict = self._build_input_to_data_info_dict(module_nodes, pipeline_parameters)
        sub_pipelines_info = self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping,
                                                           pipeline_parameters)
        graphyaml = self._build_visualization_dict(graph=graph,
                                                   pipeline_parameters=pipeline_parameters,
                                                   sub_pipelines_info=sub_pipelines_info)
        if not skip_validation:
            self._validate(graphyaml=graphyaml, raise_error=True)

        compute_target_name, _ = default_compute_target
        if not experiment_name:
            experiment_name = self.name.replace(' ', '_')
        if not description:
            description = self.description if self.description else self.name
        request = SubmitPipelineRunRequest(
            experiment_name=experiment_name,
            description=description,
            compute_target=compute_target_name,
            graph=graph,
            module_node_run_settings=module_node_run_settings,
            tags=tags,
            continue_run_on_step_failure=continue_on_step_failure,
            sub_pipelines_info=sub_pipelines_info
            # Pipeline parameters already resolved into graph, no need to added here.
        )

        run = self._submit_pipeline(request=request)

        telemetry_value = self._get_telemetry_values(
            pipeline_parameters=pipeline_parameters,
            compute_target=default_compute_target,
            data_sources=input_to_data_info_dict.values(),
            sub_pipelines_info=sub_pipelines_info,
            additional_value={
                'run_id': run._id,
            })

        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)
        for node in module_nodes:
            _LoggerFactory.trace(_get_logger(),
                                 "Pipeline_submit_module",
                                 node._get_telemetry_values(default_compute_target, {
                                     'run_id': run._id,
                                 }),
                                 adhere_custom_dimensions=False)

        return run

    def _submit_pipeline(self, request: SubmitPipelineRunRequest) -> Run:
        service_caller = _DesignerServiceCallerFactory.get_instance(self._workspace)
        # Special case for kubeflow
        draft_id = None
        compute_target_name = request.compute_target
        if compute_target_name is not None and "kubeflow" in compute_target_name:
            draft = self._save_pipeline_as_draft(_id=None, request=request)
            draft_id = draft.id
            run_id = service_caller.submit_pipeline_draft_run(request=request, draft_id=draft_id)
        else:
            run_id = service_caller.submit_pipeline_run(request)

        print('Submitted PipelineRun', run_id)
        experiment = Experiment(self._workspace, request.experiment_name)
        run = Run(experiment, run_id)
        print('Link to Azure Machine Learning Portal:', run._get_portal_url())
        return run

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="PipelineComponent_save")
    def _save(self, experiment_name=None, id=None, default_compute_target=None,
              pipeline_parameters=None, tags=None, properties=None):
        """
        Save pipeline as PipelineDraft.

        :param experiment_name: The experiment name for the PipelineDraft,
            if experiment_name is None will default to pipeline name
        :type experiment_name: str
        :param id: Existing pipeline draft id. If specified, pipeline will be save to that pipeline draft.
        :type id: str
        :param default_compute_target: the default compute target used to run pipeline
        :type default_compute_target: str
        :param pipeline_parameters: An optional dictionary of pipeline parameter assignments for the PipelineDraft.
        :type pipeline_parameters: dict({str:str})
        :param tags: Tags to be added to the submitted run, {"tag": "value"}
        :type tags: dict
        :param properties: Optional properties dictionary for the PipelineDraft,
            only needed when saving as a new PipelineDraft
        :type properties: dict({str:str})

        :return: The created PipelineDraft.
        :rtype: azureml.pipeline.core.PipelineDraft
        """
        workspace = self.workspace
        default_compute_target = self._get_default_compute_target(default_compute_target)
        experiment_name = experiment_name if experiment_name else self.name.replace(' ', '_')
        pipeline_parameters = self._expand_default_pipeline_parameters(pipeline_parameters)

        module_nodes, _ = self._expand_pipeline_nodes()
        graph_builder_context = _GraphEntityBuilderContext(compute_target=default_compute_target,
                                                           pipeline_parameters=pipeline_parameters,
                                                           module_nodes=module_nodes,
                                                           workspace=workspace,
                                                           default_datastore=self.default_datastore)

        graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
        graph, module_node_run_settings = graph_entity_builder.build_graph_entity()

        input_to_data_info_dict = self._build_input_to_data_info_dict(module_nodes, pipeline_parameters)
        sub_pipelines_info = self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping,
                                                           pipeline_parameters)

        compute_target, _ = default_compute_target
        request = SubmitPipelineRunRequest(
            experiment_name=experiment_name,
            graph=graph,
            sub_pipelines_info=sub_pipelines_info,
            module_node_run_settings=module_node_run_settings,
            compute_target=compute_target,
            pipeline_parameters=pipeline_parameters,
            tags=tags,
            properties=properties
        )

        telemetry_value = self._get_telemetry_values(
            pipeline_parameters=pipeline_parameters,
            compute_target=default_compute_target,
            data_sources=input_to_data_info_dict.values(),
            sub_pipelines_info=sub_pipelines_info,
            additional_value={
                'draft_id': id if id is not None else ''
            })

        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)

        return self._save_pipeline_as_draft(_id=id, request=request)

    def _save_pipeline_as_draft(self, _id, request: SubmitPipelineRunRequest) -> PipelineDraft:
        service_caller = _DesignerServiceCallerFactory.get_instance(self._workspace)
        if _id is None:
            pipeline_draft_id = service_caller.create_pipeline_draft(
                draft_name=self.name,
                draft_description=self.description,
                graph=request.graph,
                module_node_run_settings=request.module_node_run_settings,
                tags=request.tags,
                properties=request.properties,
                sub_pipelines_info=request.sub_pipelines_info)
            pipeline_draft = service_caller.get_pipeline_draft(pipeline_draft_id, include_run_setting_params=False)
        else:
            service_caller.save_pipeline_draft(
                draft_id=_id,
                draft_name=self.name,
                draft_description=self.description,
                graph=request.graph,
                sub_pipelines_info=request.sub_pipelines_info,
                module_node_run_settings=request.module_node_run_settings,
                tags=request.tags)
            pipeline_draft = service_caller.get_pipeline_draft(_id, include_run_setting_params=False)
        return pipeline_draft

    def _publish(self, experiment_name: str, name: str, description: str = None,
                 parameters=None, tags=None):
        """
        Publish a pipeline and make it available for rerunning.

        You can get the pipeline rest endpoint from the PublishedPipeline object returned by this function. With the
        rest endpoint, you can invoke the pipeline from external applications using REST calls. For information
        about how to authenticate when calling REST endpoints, see https://aka.ms/pl-restep-auth.

        The original pipeline associated with the pipeline run is used as the base for the published pipeline.

        :param experiment_name: The name of the published pipeline's experiment.
        :type experiment_name: str
        :param name: The name of the published pipeline.
        :type name: str
        :param description: The description of the published pipeline.
        :type description: str
        :param parameters: parameters of published pipeline.
        :type parameters: dict[str, str]
        :param tags: tags of pipeline to publish
        :type tags: dict[str, str]

        :return: Created published pipeline.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        parameters = self._expand_default_pipeline_parameters(parameters)
        graph_builder_context = _GraphEntityBuilderContext(
            compute_target=self._get_default_compute_target(),
            module_nodes=self._expand_pipeline_nodes()[0],
            workspace=self.workspace,
            default_datastore=self.default_datastore,
            pipeline_parameters=parameters)

        graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
        graph, _ = graph_entity_builder.build_graph_entity()
        request = CreatePublishedPipelineRequest(
            pipeline_name=name,
            experiment_name=experiment_name,
            pipeline_description=description,
            pipeline_endpoint_name=None,
            pipeline_endpoint_description=None,
            tags=tags,
            graph=graph,
            set_as_default_pipeline_for_endpoint=True,
            use_existing_pipeline_endpoint=False,
            use_pipeline_endpoint=False,
            properties=None
        )
        result = PublishedPipeline.create(workspace=self.workspace, request=request, pipeline=self)
        published_pipeline = PublishedPipeline._from_service_caller_model(self.workspace, result)

        telemetry_values = self._get_telemetry_values(pipeline_parameters=parameters)
        telemetry_values.update({
            'pipeline_id': result.id,
            'use_pipeline_endpoint': False,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        return published_pipeline

    def _publish_to_endpoint(self, experiment_name, name: str, pipeline_endpoint_name: str,
                             description: str = None, pipeline_endpoint_description: str = None,
                             set_as_default: bool = True, use_existing_pipeline_endpoint: bool = True,
                             tags: dict = None, parameters=None):
        """
        Publish a pipeline to pipeline_endpoint.

        A pipeline enpoint is a :class:`azure.ml.component.Pipeline` workflow
         that can be triggered from a unique endpoint URL.

        :param experiment_name: The name of the published pipeline's experiment.
        :type experiment_name: str
        :param name: The name of the published pipeline.
        :type name: str
        :param description: The description of the published pipeline.
        :type description: str
        :param pipeline_endpoint_name: The name of pipeline endpoint.
        :type pipeline_endpoint_name: str
        :param pipeline_endpoint_description: The description of pipeline endpoint.
        :type pipeline_endpoint_description: str
        :param set_as_default: Whether to use pipeline published as the default version of pipeline endpoint.
        :type set_as_default: bool
        :param use_existing_pipeline_endpoint: Whether to use existing pipeline endpoint.
        :type use_existing_pipeline_endpoint: bool
        :param tags: tags of pipeline to publish
        :type tags: dict[str, str]
        :param parameters: parameters of published pipeline.
        :type parameters: dict[str, str]

        :return: Created published pipeline inside pipeline endpoint.
        :rtype: azure.ml.component._published_pipeline.PublishedPipeline
        """
        parameters = self._expand_default_pipeline_parameters(parameters)
        graph_builder_context = _GraphEntityBuilderContext(
            compute_target=self._get_default_compute_target(),
            module_nodes=self._expand_pipeline_nodes()[0],
            workspace=self.workspace,
            default_datastore=self.default_datastore,
            pipeline_parameters=parameters)

        graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
        graph, _ = graph_entity_builder.build_graph_entity()
        request = CreatePublishedPipelineRequest(
            pipeline_name=name,
            experiment_name=experiment_name,
            pipeline_description=description,
            pipeline_endpoint_name=pipeline_endpoint_name,
            pipeline_endpoint_description=pipeline_endpoint_description,
            tags=tags,
            graph=graph,
            set_as_default_pipeline_for_endpoint=set_as_default,
            use_existing_pipeline_endpoint=use_existing_pipeline_endpoint,
            use_pipeline_endpoint=True,
            properties=None
        )
        result = PublishedPipeline.create(workspace=self.workspace, request=request, pipeline=self)
        published_pipeline = PublishedPipeline._from_service_caller_model(self.workspace, result)

        telemetry_values = self._get_telemetry_values(pipeline_parameters=parameters)
        telemetry_values.update({
            'pipeline_id': result.id,
            'use_pipeline_endpoint': True,
            'set_as_default': set_as_default,
            'use_existing_pipeline_endpoint': use_existing_pipeline_endpoint,
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        return published_pipeline

    @track(_get_logger, activity_type=_PUBLIC_API, flush=True)
    def validate(self, raise_error=False):
        """Graph/component validation and visualization.

        :param raise_error: Whether directly raises the error or just shows the error list.
        :type raise_error: bool
        :return: List of errors
        :rtype: builtin.list
        """
        graphyaml = self._build_visualization_dict()

        if _can_visualize():
            from ._widgets._visualize import _visualize
            is_prod = _is_prod_workspace(self.workspace)
            envinfo = {
                "subscription_id": self.workspace.subscription_id
            }
            _visualize(graphyaml, envinfo=envinfo, is_prod=is_prod, ignore_fallback=True)
        else:
            from ._widgets import VISUALIZATION_NOT_SUPPORTED_MESSAGE
            print(VISUALIZATION_NOT_SUPPORTED_MESSAGE)

        validate_result = self._validate(graphyaml=graphyaml, raise_error=raise_error)

        return validate_result

    def _validate(self, graphyaml, raise_error=False):
        pipeline_steps = graphyaml['pipeline']['steps']
        errors = []

        def process_cycle_error(cycle):
            cycles_nodes = [
                "{0}({1})".format(pipeline_steps[node.node_id]['validate']['module_display_name'], node.node_id)
                for node in cycle
            ]
            error = PipelineValidationError(message="Module cycle detected, including nodes: {}".format(cycles_nodes),
                                            error_type=PipelineValidationError.MODULE_CYCLE)
            errors.append({'error': [
                {'message': error.message,
                 'type': error.error_type}
            ]})

        PipelineValidator.validate_pipeline_steps(pipeline_steps, errors)
        PipelineValidator.validate_module_cycle(pipeline_steps, process_cycle_error)

        result = "validation passed"
        if len(errors) > 0:
            result = "validation failed"
            if raise_error:
                raise PipelineValidationError(
                    'Validation failed! Errors: {}'.format(errors),
                    error_type=PipelineValidationError.AGGREGATED,
                )

        telemetry_value = self._get_telemetry_values(additional_value={
            'validation_passed': len(errors) == 0
        })

        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_value)
        if len(errors) > 0:
            for module_errors in errors:
                if 'ModuleCycle' in module_errors['error'][0]['type']:
                    pass
                else:
                    module_info = {
                        'module_id': module_errors['module_id'],
                        'module_version': module_errors['module_version'],
                    }
                    for one_error in module_errors['error']:
                        if 'type' in one_error:
                            telemetry_value = self._get_telemetry_values()
                            telemetry_value.update(module_info)
                            telemetry_value.update({
                                'error_message': one_error['message'],
                                'error_type': one_error['type']
                            })
                            _LoggerFactory.trace(_get_logger(), "Pipeline_module_validate_error", telemetry_value,
                                                 adhere_custom_dimensions=False)

        return {
            "result": result,
            "errors": errors
        }

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="PipelineComponent_export_yaml")
    def _export_yaml(self, directory=None):
        """
        Export pipeline to yaml files.

        This is an experimental function, will be changed anytime.

        :param directory: The target directory path. Default current working directory
            path will be used if not provided.
        :type directory: str
        :return: The directory path
        :rtype: str
        """
        from ._pipeline_export_provider import PipelineExportProvider

        if directory is None:
            directory = os.getcwd()
        if not os.path.exists(directory):
            raise UserErrorException('Target directory not exists, path {}'.format(directory))
        elif not os.path.isdir(directory):
            raise UserErrorException('Expected a directory path , got {}'.format(directory))

        module_nodes, _ = self._expand_pipeline_nodes()
        pipelines = self._expand_pipeline_to_pipelines()

        graph_builder_context = _GraphEntityBuilderContext(
            compute_target=self._get_default_compute_target(),
            module_nodes=module_nodes,
            workspace=self.workspace,
            default_datastore=self.default_datastore,
            pipeline_parameters=self._expand_default_pipeline_parameters(None))

        graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
        graph, _ = graph_entity_builder.build_graph_entity(is_local_run=True)
        input_to_data_info_dict = self._build_input_to_data_info_dict(
            module_nodes)

        return PipelineExportProvider(graph, self, pipelines, module_nodes, input_to_data_info_dict.values()). \
            export_pipeline_entity(directory_path=directory)

    def _get_telemetry_values(self, pipeline_parameters=None, compute_target=None, data_sources=None,
                              sub_pipelines_info=None, on_create=False, additional_value=None):
        """
        Get telemetry value out of a pipeline.

        The telemetry values include the following entries:

        * pipeline_id: A uuid generated for each pipeline created.
        * defined_by: The way the pipeline is created, using @dsl.pipeline or raw code.
        * node_count: The total count of all module nodes.
        * pipeline_parameters_count: The total count of all pipeline parameters.
        * data_pipeline_parameters_count: The total count of all pipeline parameters that are dataset.
        * literal_pipeline_parameters_count: The total count of all pipeline parameters that are literal values.
        * input_count: The total count of data sources.
        * compute_count: The total count of distinct computes.
        * compute_type_count: The total count of distinct compute types.
        * top_level_node_count: The total count of top level nodes & pipelines.
        * subpipeline_count: The total count of sub pipelines.

        :param pipeline_parameters: The pipeline parameters.
        :param compute_target: The compute target.
        :param data_sources: Data sources of the pipeline.
        :param sub_pipelines_info: Sub pipeline infos of the pipeline.
        :param on_create: Whether the pipeline was just created, which means compute target, pipeline parameters, etc
                       are not available.
        :return: telemetry values.
        :rtype: dict
        """
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(self.workspace)
        all_nodes, _ = self._expand_pipeline_nodes()
        telemetry_values['pipeline_id'] = self._id
        telemetry_values['defined_by'] = "dsl" if self._use_dsl else "raw"
        telemetry_values['node_count'] = len(all_nodes)
        telemetry_values['top_level_node_count'] = len(self.nodes)
        if on_create:
            # We do not have enough information to populate all telemetry values.
            if additional_value is not None:
                telemetry_values.update(additional_value)
            return telemetry_values

        telemetry_values.update(
            _get_telemetry_value_from_pipeline_parameter(pipeline_parameters))

        if compute_target is not None:
            compute_set = set([node._resolve_compute(compute_target)[0] for node in all_nodes])
            compute_type_set = set([node._resolve_compute(compute_target)[1] for node in all_nodes])
            telemetry_values['compute_count'] = len(compute_set)
            telemetry_values['compute_type_count'] = len(compute_type_set)

        if data_sources is not None:
            telemetry_values['input_count'] = len(data_sources)
        if sub_pipelines_info is not None:
            telemetry_values['subpipeline_count'] = len(
                sub_pipelines_info.sub_graph_info) - 1

        if additional_value is not None:
            telemetry_values.update(additional_value)

        return telemetry_values

    def _replace_module(self, old_module: Component, new_module: Component,
                        recursive: bool):
        if recursive:
            nodes, _ = self._expand_pipeline_nodes()
        else:
            nodes = self.nodes
        for node in nodes:
            if isinstance(node, Component) and \
                    not isinstance(node, Pipeline) and \
                    node._is_replace_target(old_module):
                # replace target node's module_version
                node._replace(new_module)

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="PipelineComponent_replace_component_func")
    def _replace_component_func(self, old_component_func: Callable, new_component_func: Callable,
                                recursive=False, force=False):
        """
        Replace modules by module_function.

        :param old_component_func: A component function which can generate the old module you want to replace
        :type old_component_func: function
        :param new_component_func: A component function which can generate the new module to replace the old one
        :type new_component_func: function
        :param recursive: Indicates this function will replace the modules
                        in the specified pipeline and in all sub pipelines
        :type recursive: bool
        :param force: Whether to force replace, skip validation check
        :type force: bool

        :return: The pipeline itself
        :rtype: azure.ml.component.pipeline.Pipeline
        """
        old_module = old_component_func()
        new_module = new_component_func()
        if not force:
            errors = ComponentValidator.validate_compatibility(old_module, new_module)

            if len(errors) > 0:
                raise UserErrorException('Module incompatible! Errors:{0}'.format(errors))
        self._replace_module(old_module, new_module, recursive)
        return self

    def _expand_pipeline_to_pipelines(self):
        pipelines = []
        _expand_pipeline_to_pipelines(self, pipelines)
        return pipelines

    def _expand_pipeline_nodes(self, prefix="", module_node_to_graph_node_mapping=None):
        """
        Expand pipeline to node list, and mapping of module instance_id to node info.

        :param prefix: parent pipeline name
        :type prefix: str
        :param module_node_to_graph_node_mapping: mapping of module node to graph node
        :type module_node_to_graph_node_mapping: dict
        :return: node list and mapping of module instance_id to node info
        :rtype: list, dict({str: dict})
        """
        module_to_node_mapping = {}
        steps = []
        for node in self.nodes:
            if isinstance(node, Pipeline):
                sub_pipeline_steps, sub_pipeline_module_mapping = node._expand_pipeline_nodes(
                    os.path.join(prefix, trans_node_name(node.name, node._id)), module_node_to_graph_node_mapping)
                module_to_node_mapping.update(sub_pipeline_module_mapping)
                steps.extend(sub_pipeline_steps)
            elif isinstance(node, Component):
                step = node
                setattr(step, 'pipeline', self)
                setattr(step, 'module_node', node)
                module_to_node_mapping[step._instance_id] = {
                    STEP_PREFIX: prefix,
                    NODE_ID:
                        None if not module_node_to_graph_node_mapping
                        else module_node_to_graph_node_mapping[step._instance_id],
                    WORKING_DIR: ''
                }
                steps.append(step)
        return steps, module_to_node_mapping

    def _expand_default_pipeline_parameters(self, pipeline_parameters):
        """Add pipeline parameter with default value to pipeline_parameters."""
        if pipeline_parameters is None:
            pipeline_parameters = {}
        self._validate_parameters(pipeline_parameters)
        pipeline_parameters.update({
            _k: _v for _k, _v in self._parameter_params.items() if _k not in pipeline_parameters})
        return pipeline_parameters

    def _get_visualization_context(self, graph=None, pipeline_parameters=None,
                                   sub_pipelines_info=None, support_local_dataset=False):
        module_nodes, _ = self._expand_pipeline_nodes()

        if graph is None:
            graph_builder_context = _GraphEntityBuilderContext(compute_target=self._get_default_compute_target(),
                                                               module_nodes=module_nodes,
                                                               workspace=self.workspace,
                                                               default_datastore=self.default_datastore)
            graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
            graph, _ = graph_entity_builder.build_graph_entity(is_local_run=True)

        if sub_pipelines_info is None:
            sub_pipelines_info = self._build_sub_pipeline_info(graph.module_node_to_graph_node_mapping,
                                                               pipeline_parameters)

        context = VisualizationContext.from_pipeline_component(
            self,
            graph.module_node_to_graph_node_mapping,
            pipeline_parameters,
            sub_pipelines_info,
            support_local_dataset=support_local_dataset)

        return context

    def _build_visualization_dict(self, graph=None, pipeline_parameters=None,
                                  sub_pipelines_info=None, support_local_dataset=False):
        context = self._get_visualization_context(graph, pipeline_parameters,
                                                  sub_pipelines_info, support_local_dataset)

        from ._widgets._visualization_builder import VisualizationBuilder
        visualization_builder = VisualizationBuilder(step_nodes=context.step_nodes,
                                                     module_defs=context.module_defs,
                                                     data_nodes=context.data_nodes,
                                                     sub_pipelines_info=context.sub_pipelines_info)

        return visualization_builder.build_visualization_dict()

    @track(_get_logger, activity_type=_PUBLIC_API, record_inner_depth=5, activity_name="PipelineComponent_run")
    def _run(self, experiment_name=None, working_dir=None, use_docker=True, track_run_history=True,
             show_output=False, show_graph=True, python_interpreter_path=None, pipeline_parameters=None,
             continue_on_step_failure=None, max_workers=None, raise_on_error=True):
        """
        Run pipeline in local.

        Currently support basic/mpi/parallel components run in local environment.

        :param experiment_name: The experiment name, if experiment_name is None will default to pipeline name
        :type experiment_name: str
        :param working_dir: The path where pipeline run data and snapshot will be stored.
        :type working_dir: str
        :param use_docker: If use_docker=True, will pull image from azure and run component in system-managed
                           docker-based environment.
                           If use_docker=False and python_interpreter_path is None, will run component in
                           system-managed conda-based environment.
                           If use_docker=False and python_interpreter_path is not None, will directly run component
                           in user-managed environment.
        :type use_docker: bool
        :param track_run_history: If track_run_history=True, will create azureml.Run and upload component output
                                  and log file to portal.
                                  If track_run_history=False, will not create azureml.Run to upload outputs
                                  and log file.
        :type track_run_history: bool
        :param show_output: Indicates whether to show the pipeline run status on sys.stdout.
        :type show_output: bool
        :param show_graph: Indicates whether to show the graph with run status on notebook.
            If not in notebook environment, overwrite this value to False
        :type show_graph: bool
        :param python_interpreter_path: When use_docker=False and python_interpreter_path not None, will directly
                                        run component in user-managed environment.
                                        When use_docker=False and python_interpreter_path is None, will run component
                                        in system-managed conda-based environment.
        :type python_interpreter_path: str
        :param pipeline_parameters: An optional dictionary of pipeline parameter
        :type pipeline_parameters: dict({str:str})
        :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
            If True, only steps that have no dependency on the output of the failed step will continue execution.
        :type continue_on_step_failure: bool
        :param max_workers:  The maximum number of threads that can be used to execute pipeline steps.
            If max_workers is None, it will decide depends on the number of processors on the machine.
        :type max_workers: int
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool

        :return: The run status, such as, Completed and Failed.
        :rtype: str
        """
        # in notebook show pipeline
        from ._widgets._visualize import _can_visualize, _visualize
        visualizer = None

        module_nodes, _ = self._expand_pipeline_nodes()
        graph_builder_context = _GraphEntityBuilderContext(compute_target=self._get_default_compute_target(),
                                                           module_nodes=module_nodes,
                                                           workspace=self.workspace,
                                                           default_datastore=self.default_datastore)

        graph_entity_builder = _GraphEntityBuilder(graph_builder_context)
        graph, _ = graph_entity_builder.build_graph_entity(is_local_run=True)
        module_node_to_graph_node_mapping = graph.module_node_to_graph_node_mapping

        input_to_data_info_dict = self._build_input_to_data_info_dict(module_nodes,
                                                                      pipeline_parameters,
                                                                      support_local_dataset=True)
        sub_pipelines_info = self._build_sub_pipeline_info(module_node_to_graph_node_mapping,
                                                           pipeline_parameters,
                                                           support_local_dataset=True)

        if show_graph:
            if _can_visualize():
                graphyaml = self._build_visualization_dict(graph, pipeline_parameters,
                                                           sub_pipelines_info, support_local_dataset=True)
                is_prod = _is_prod_workspace(self.workspace)
                envinfo = {
                    "subscription_id": self.workspace.subscription_id
                }
                visualizer = _visualize(graphyaml, envinfo=envinfo, is_prod=is_prod)
            else:
                from ._widgets import VISUALIZATION_NOT_SUPPORTED_MESSAGE
                print(VISUALIZATION_NOT_SUPPORTED_MESSAGE)

        # create experiment
        experiment_name = experiment_name if experiment_name else self.name.replace(' ', '_')
        with RunHistoryTracker.without_definition(self.workspace, experiment_name, track_run_history) as tracker:
            if not working_dir:
                working_dir = os.path.join(tempfile.gettempdir(), experiment_name, tracker.get_run_id() or self._id)
            short_working_dir = _get_short_path_name(working_dir, True)

            print('Working dir:', working_dir)
            tracker.print_run_info()

            pipeline_run_success = True
            pipeline_run_success = _orchestrate_pipeline_run(self,
                                                             short_working_dir,
                                                             module_node_to_graph_node_mapping,
                                                             tracker=tracker,
                                                             visualizer=visualizer,
                                                             pipeline_parameters=pipeline_parameters,
                                                             show_output=show_output,
                                                             continue_on_step_failure=continue_on_step_failure,
                                                             max_workers=max_workers,
                                                             datasource=input_to_data_info_dict.keys(),
                                                             use_docker=use_docker,
                                                             python_interpreter_path=python_interpreter_path,
                                                             raise_on_error=raise_on_error)
        return 'Completed' if pipeline_run_success else 'Failed'

    def _build_sub_pipeline_info(self, module_node_to_graph_node_mapping,
                                 pipeline_parameters=None, support_local_dataset=False):
        """Build sub pipelines info for pipeline."""
        from ._sub_pipeline_info_builder import SubPipelinesInfoBuilder
        return SubPipelinesInfoBuilder(self, module_node_to_graph_node_mapping,
                                       pipeline_parameters, support_local_dataset=support_local_dataset).build()

    def _build_input_to_data_info_dict(self, module_nodes, pipeline_parameters=None, support_local_dataset=False):
        all_data_inputs = [n.inputs[input_name]._get_internal_data_source() for n in module_nodes
                           for input_name in n.inputs if n.inputs[input_name]._dset is not None]
        inputs = [i for i in all_data_inputs
                  if not isinstance(i, PipelineData) and not isinstance(i, Output)]

        input_to_data_info_dict = {}

        for input in inputs:
            input_to_data_info_dict[input] = \
                _build_data_info_from_input(input, pipeline_parameters, support_local_dataset)

        return input_to_data_info_dict


def _expand_pipeline_to_pipelines(pipeline, pipelines, parent=None):
    """Expand the pipeline into list."""
    pipelines.append(pipeline)
    pipeline._parent = parent
    for node in pipeline.nodes:
        if isinstance(node, Pipeline):
            _expand_pipeline_to_pipelines(node, pipelines, pipeline)


def _build_data_info_from_input(input, pipeline_parameters: Dict[str, Any], support_local_dataset):
    if isinstance(input, PipelineParameter):
        if input.default_value is not None:
            input = input.default_value
        else:
            # pipeline parameter which has not been assigned in pipeline initialization
            # try to find if the parameter is assigned after initialization
            if pipeline_parameters is not None and input.name in pipeline_parameters.keys():
                input = pipeline_parameters[input.name]
            else:
                return DataInfo(name=input.name, dataset_type='parameter')

    if isinstance(input, DataReference) or isinstance(input, _GlobalDataset):
        return DataInfo(aml_data_store_name=input.datastore.name,
                        relative_path=input.path_on_datastore,
                        name=input.data_reference_name)
    elif hasattr(input, '_registration'):  # registered dataset
        # Filter FileDataset/Dataset
        reg = input._registration
        return DataInfo(id=reg.registered_id, saved_dataset_id=reg.saved_id, name=reg.name)
    elif hasattr(input, 'dataset'):  # saved dataset
        # Filter DatasetConsumptionConfig
        return DataInfo(saved_dataset_id=input.dataset.id, name=input.name)
    elif support_local_dataset and (isinstance(input, str) or isinstance(input, Path)):
        # pipeline run support local dataset
        if not Path(input).exists():
            raise UserErrorException("Input is not found, {0}".format(input))
        name = input if isinstance(input, str) else str(input)
        return DataInfo(name=name)
    else:
        raise UserErrorException("Invalid input type: {0}".format(type(input)))
