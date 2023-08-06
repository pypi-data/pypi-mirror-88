# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
from abc import ABC, abstractmethod
from ruamel import yaml
from typing import Union

from azureml.data._dataset import AbstractDataset
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.exceptions._azureml_exception import UserErrorException

from .component import Component, Output, Input
from .dsl._module_spec import _str_representer, _YamlFlowList
from .pipeline import Pipeline
from ._dataset import _GlobalDataset
from ._restclients.designer.models import DataInfo
from ._pipeline_parameters import PipelineParameter
from ._util._utils import _sanitize_python_variable_name, _get_valid_directory_path, \
    _scrubbed_exception, _unique, _get_data_info_hash_id


def _get_source_val_from_dset(
        provider, current_node, dset, ref_name, ref_value, separate_file, parent_pipeline):
    if isinstance(dset, PipelineParameter):
        if ref_value:
            # Not pipeline' parameter or inputs, make value as real value
            all_pipeline_params = {_k: _v._get_internal_data_source() for _k, _v in parent_pipeline.inputs.items()}
            all_pipeline_params.update({_k: _v for _k, _v in parent_pipeline._parameter_params.items()})
            current_param_name = all_pipeline_params.keys()
            source_param_to_current_param = {_v.name: _k for _k, _v in all_pipeline_params.items() if
                                             isinstance(_v, PipelineParameter)}
            if dset.name in source_param_to_current_param.keys():
                # Parameter is pass by current pipeline and from more outer pipeline.
                # Convert name to current parameter's name.
                source_val = {ref_name: 'inputs/{}'.format(source_param_to_current_param[dset.name])}
            elif dset.name in current_param_name:
                # Parameter is from current pipeline.
                source_val = {ref_name: 'inputs/{}'.format(dset.name)}
            else:
                # Parameter is a hard code value.
                source_val = _get_source_val_from_dset(
                    provider, current_node, dset.default_value, ref_name, ref_value, separate_file, parent_pipeline)
        else:
            source_val = _get_source_val_from_dset(provider, current_node, dset.default_value,
                                                   ref_name, ref_value, separate_file, parent_pipeline)
        return source_val
    if isinstance(dset, Input):
        source_val = {ref_name: 'inputs/{}'.format(dset.name)}
        return source_val
    if isinstance(dset, DatasetConsumptionConfig):
        dset = dset.dataset.name

    global_dataset_ref_format = '/datasets/{}' if not separate_file else 'datasets/{}.yaml'
    if isinstance(dset, Output):
        current_pipeline = provider.get_parent_pipeline(current_node.instance)
        from_node_instance_id = next((n._get_instance_id() for n in current_pipeline.nodes
                                      if dset in n.outputs.values()), None)
        node = provider.get_node_by_instance_id(from_node_instance_id)
        source_val = {'$inputPath': 'graph/{}/outputs/{}'.format(node.graph_ref, dset._name)}
    elif isinstance(dset, AbstractDataset):
        source_val = dset.name if dset.name is not None else dset.id
        source_val = {'$inputPath': global_dataset_ref_format.format(source_val)}
    elif isinstance(dset, _GlobalDataset):
        source_val = {'$inputPath': global_dataset_ref_format.format(dset.data_reference_name)}
    else:
        source_val = dset
    return source_val


def _dump_file(entity_dict, directory_path, file_name, entity_dict_str=None, ignore_dup=True):
    file_path = os.path.join(directory_path, _sanitize_python_variable_name(file_name) + '.yaml')
    if os.path.exists(file_path):
        if not ignore_dup:
            msg = 'Target file path {} already exists!'
            raise _scrubbed_exception(UserErrorException, msg, file_path)
        else:
            return
    with open(file_path, 'w') as f:
        if entity_dict_str is not None:
            f.write(entity_dict_str)
        else:
            yaml.RoundTripRepresenter.add_representer(_YamlFlowList, _YamlFlowList.representer)
            yaml.RoundTripRepresenter.add_representer(str, _str_representer)
            yaml.dump(entity_dict, f, encoding='UTF-8', Dumper=yaml.RoundTripDumper)
    print('Successfully dump yaml file at {}'.format(file_path))


def _prepare_pipeline_to_parent_pipeline_dict(root_pipeline, pipeline_to_parent_dict):
    for node in root_pipeline.nodes:
        if isinstance(node, Pipeline):
            pipeline_to_parent_dict[node] = root_pipeline
            _prepare_pipeline_to_parent_pipeline_dict(node, pipeline_to_parent_dict)


class NodeBase(ABC):
    def __init__(self, node_id, node_type, compute_target_name=None, append_id=False,
                 instance=None, inline_ref_format='', graph_ref_format='{}', separate_file_ref_format='',
                 creation_context=None, node_name=None, ref_name=None):
        self.node_id = node_id
        self.type = node_type
        self.schema = 'http://azureml/sdk-2-0/{}.json'.format(self.type)
        self.compute_target_name = compute_target_name
        self.append_id = append_id
        self.instance = instance
        self.node_name = self.resolve_node_name(append_id, node_name)
        self.node_name = _sanitize_python_variable_name(self.node_name)
        self.target_ref = self.resolve_node_compute_ref(self.compute_target_name)
        ref_name = _sanitize_python_variable_name(ref_name)
        self.relative_ref_name = ref_name
        self.inline_ref = inline_ref_format.format(ref_name)
        self.graph_ref = graph_ref_format.format(self.node_name)
        self.separate_file_ref = separate_file_ref_format.format(_sanitize_python_variable_name(ref_name))
        self.creation_context = creation_context

    @abstractmethod
    def export_attribute(self, provider, directory_path, separate_file, parent_pipeline):
        """
        Export node attribute on graph.

        :param provider: export provider, to resolve input/output node
        :type provider: PipelineExportProvider
        :param directory_path: directory path about to save
        :type directory_path: str
        :return: attribute dict
        :param separate_file: export node to a separate file or not
        :type separate_file: bool
        :rtype: dict
        :param parent_pipeline: the node's parent
        :type parent_pipeline: Pipeline
        """
        raise NotImplementedError

    @abstractmethod
    def export_definition(self, provider, directory_path, separate_file, parent_pipeline):
        """
        Export definition of module and dataset as references.

        :param provider: export provider, to resolve input/output node
        :type provider: PipelineExportProvider
        :param directory_path: directory path about to save
        :type directory_path: str
        :return: definition dict
        :param separate_file: export node to a separate file or not
        :type separate_file: bool
        :rtype: dict
        :param parent_pipeline: the node's parent
        :type parent_pipeline: Pipeline
        """
        raise NotImplementedError

    @classmethod
    def _resolve_node_variable_name(cls, node, parent):
        if parent is None:
            return 'main'
        var_name_dict = parent._node_id_variable_name_dict
        all_names = [var_name_dict.values()]
        all_names.extend([node.name for node in parent.nodes if node._id not in var_name_dict.keys()])
        name = var_name_dict[node._id] if node._id in var_name_dict.keys() else node.name
        if len([n for n in all_names if n == name]) > 1:
            name = '{}-{}'.format(name, node._id)
        return name

    def resolve_node_name(self, append_id, node_name):
        """
        Resolve node name in yaml

        :param append_id: append node id after name or not
        :type append_id: bool
        :param node_name: node name from input
        :type node_name: str
        :return: node name
        :rtype: str
        """
        if node_name is not None:
            return node_name

        if not append_id:
            return self.instance.name
        return '{}-{}'.format(self.instance.name, self.node_id)

    def resolve_node_compute_ref(self, target_name):
        """
        Resolve the compute target dict of pipeline or module, it is not
            None if configured by user.

        :return: compute target name
        :rtype: str
        """
        if target_name is None:
            return None
        return {'$ref': 'aml:compute_targets/{}'.format(target_name)}

    def serialize_node_inputs_outputs(self, provider, separate_file, ref_value, parent_pipeline):
        """
        Serialize single module or pipeline's inputs and outputs provided.
        :return: A dict contains inputs, outputs, parameters and runsettings mappings.
        :rtype: dict
        """
        inputs_dict = {}
        outputs_dict = {}
        instance = self.instance
        real_inputs = {_k: _v for _k, _v in instance.inputs.items() if _v._dset is not None}
        # serialize inputs
        for _k, input in real_inputs.items():
            dset = input._dset
            source_val = _get_source_val_from_dset(
                provider, current_node=self, dset=dset, ref_name='$inputPath',
                ref_value=ref_value, separate_file=separate_file, parent_pipeline=parent_pipeline)
            inputs_dict[_k] = source_val
        # serialize parameters
        params = instance._parameter_params
        for k, v in params.items():
            # ignore duplicate input of input port
            if k in inputs_dict.keys():
                continue
            if isinstance(v, Input):
                v = v._get_internal_data_source()
            v = _get_source_val_from_dset(
                provider, current_node=self, dset=v, ref_name='$inputValue',
                ref_value=ref_value, separate_file=separate_file, parent_pipeline=parent_pipeline)
            inputs_dict.update({k: v})
        # serialize outputs
        for k, v in instance.outputs.items():
            outputs_dict.update({k: {'mode': v._output_mode}})
        return {'inputs': inputs_dict, 'outputs': outputs_dict}

    def get_full_ref_name(self, separate_file):
        return self.separate_file_ref if separate_file else self.inline_ref


class DatasetNode(NodeBase):
    def __init__(self, data_info: DataInfo, node_id=None):
        node_name = _sanitize_python_variable_name(data_info.name)
        super().__init__(node_id=node_id,
                         node_type='Dataset',
                         node_name=node_name,
                         instance=data_info,
                         separate_file_ref_format='{}.yaml',
                         ref_name=node_name)

    def export_attribute(self, provider, directory_path, separate_file, parent_pipeline):
        raise NotImplementedError

    def export_definition(self, provider, directory_path, separate_file, parent_pipeline):
        attr_dict = {'$schema': self.schema,
                     'type': self.type,
                     'name': self.node_name}
        # add data info dict
        for attr, value in self.instance.__dict__.items():
            if attr not in attr_dict.keys() and value is not None:
                attr_dict[attr] = value
        if separate_file:
            _dump_file(entity_dict=attr_dict, directory_path=os.path.join(directory_path, 'datasets'),
                       file_name=self.relative_ref_name)
        return {self.relative_ref_name: attr_dict}


class ModuleNode(NodeBase):
    def __init__(self, module: Component, node_id, ref_append_id):
        compute_target = module.runsettings._target
        if isinstance(compute_target, tuple):
            compute_target, _ = compute_target
        ref_name = module._definition.name if not ref_append_id \
            else module._definition.name + module.version
        node_variable_name = self._resolve_node_variable_name(module, module.pipeline)
        self.ref_append_id = ref_append_id
        super().__init__(node_id=node_id,
                         node_type='ContainerModule',
                         compute_target_name=compute_target,
                         instance=module,
                         inline_ref_format='/modules/{}',
                         separate_file_ref_format='modules/{}.yaml',
                         ref_name=ref_name,
                         node_name=node_variable_name)
        created_by = module.created_by
        if created_by is not None:
            self.creation_context = {'user': created_by,
                                     'create_time': module.created_date}

    def export_attribute(self, provider, directory_path, separate_file, parent_pipeline):
        # module node attribute in graph will not separate
        node_entity = {'$ref': self.get_full_ref_name(separate_file),
                       'type': self.type}
        inputs_outputs_dict = self.serialize_node_inputs_outputs(
            provider, separate_file, ref_value=True, parent_pipeline=parent_pipeline)
        # serialize compute run setting
        runsetting_dict = {}
        for p in self.instance.runsettings._params_spec:
            if p == 'target':
                continue
            attr_value = getattr(self.instance.runsettings, p)
            if attr_value is not None:
                runsetting_dict[p] = attr_value
        # TODO: ignore k8s param now
        # k8s_param = self.instance.k8srunsettings._params_spec
        # for section in k8s_param:
        #     for p in k8s_param[section]:
        #         attr_value = getattr(getattr(self.instance.k8srunsettings, section), p.argument_name)
        #         if attr_value is not None:
        #             runsetting_dict[p.argument_name] = attr_value
        if len(runsetting_dict) > 0:
            inputs_outputs_dict.update({'runsettings': runsetting_dict})
        node_entity.update(inputs_outputs_dict)

        # unpack parameter if v is PipelineParameter
        if self.target_ref is not None:
            node_entity.update({'target': self.target_ref})
        return {self.node_name: node_entity}

    def export_definition(self, provider, directory_path, parent_pipeline, separate_file=True):
        if separate_file:
            yaml_str = self.instance._module_dto.yaml_str
            # ignore duplicate reference export
            if separate_file:
                _dump_file(entity_dict=None, entity_dict_str=yaml_str,
                           directory_path=os.path.join(directory_path, 'modules'),
                           file_name=self.relative_ref_name)
        dto = self.instance._module_dto
        definition_dict = {
            '$schema': self.schema, 'module_id': dto.module_version_id,
            'version': dto.module_version, 'name': self.instance._definition.name,
            'description': dto.description,
            'creation_context': self.creation_context}

        _, transformed_parameters, _ = \
            self.instance._module_dto.get_module_inputs_outputs(return_yaml=False)
        interface_input_dict = {
            i.name: {"label": i.label, "description": i.description,
                     "data_type_ids_list": i.data_type_ids_list}
            for i in dto.module_entity.structured_interface.inputs
        }
        interface_input_dict.update(
            {p.name: {"label": p.annotation,
                      "type": p._type, "default": p.default}
             for p in transformed_parameters})
        interface_outputs_dict = {
            i.name: {"label": i.label, "description": i.description,
                     "data_type_id": i.data_type_id}
            for i in dto.module_entity.structured_interface.outputs
        }
        definition_dict.update({'structured_interface': {'inputs': interface_input_dict,
                                                         'outputs': interface_outputs_dict}})
        return {self.relative_ref_name: definition_dict}


class PipelineNode(NodeBase):
    def __init__(self, pipeline: Pipeline, node_id):
        compute_target, _ = pipeline._get_default_compute_target()
        self.is_primary = not pipeline._is_sub_pipeline
        node_variable_name = self._resolve_node_variable_name(pipeline, pipeline._parent)
        ref_name = self._resolve_ref_name(pipeline)

        super().__init__(node_id=node_id,
                         node_type='PipelineModule',
                         compute_target_name=compute_target,
                         instance=pipeline,
                         inline_ref_format='/pipelines/{}',
                         separate_file_ref_format='{}.yaml',
                         ref_name=ref_name,
                         node_name=node_variable_name)

    def _resolve_ref_name(self, pipeline):
        """Resolve duplicate pipeline definition name as reference name(file name)."""
        if self.is_primary:
            return "main"
        parent = pipeline
        # Find the root parent of current pipeline
        while parent._parent is not None:
            parent = parent._parent
        # Expand all pipelines' definition
        definitions = set(
            sub_pipeline._definition
            for sub_pipeline in parent._expand_pipeline_to_pipelines() if sub_pipeline != parent)
        # Append id if there is pipeline with same name with current
        return pipeline._definition.name if \
            len([definition.name for definition in definitions if pipeline._definition.name == definition.name]) == 1 \
            else '{}-{}'.format(pipeline._definition.name, pipeline._definition.id)

    def export_attribute(self, provider, directory_path, separate_file, parent_pipeline):
        """
        Export single pipeline to a dict, do not export it's sub pipeline.

        :param provider: pipeline export provider
        :type provider: PipelineExportProvider
        :param directory_path: target directory path
        :type directory_path: str
        :param separate_file: export node to a separate file or not
        :type separate_file: bool
        :param parent_pipeline: the node's parent
        :type parent_pipeline: Pipeline
        :return:
        """
        pipeline_result = {}
        # add step type and ref
        ref = {'$ref': self.get_full_ref_name(separate_file)}
        pipeline_result.update({'component': ref, 'type': self.type})
        inputs_outputs_dict = self.serialize_node_inputs_outputs(
            provider, separate_file, ref_value=True, parent_pipeline=parent_pipeline)
        param_set = set(self.instance._definition._parameters.keys())
        param_set.update(self.instance._definition._inputs.keys())
        inputs_outputs_dict['inputs'] = {k: v for k, v in inputs_outputs_dict['inputs'].items() if k in param_set}
        pipeline_result.update(inputs_outputs_dict)

        if self.target_ref is not None:
            pipeline_result.update({'target': self.target_ref})
        entity_dict = {self.node_name: pipeline_result}

        return entity_dict

    def export_definition(self, provider, directory_path, separate_file, parent_pipeline):

        # Update pipeline parameters type
        def update_pipeline_parameter():
            inputs_value_dict = self.serialize_node_inputs_outputs(
                provider, separate_file, ref_value=False, parent_pipeline=parent_pipeline)['inputs']
            for param in self.instance._pipeline_definition.parameter_list:
                entity_dict = {}
                param_type = 'Any'
                if param.key in inputs_value_dict.keys():
                    input_value = inputs_value_dict[param.key]
                    if isinstance(input_value, PipelineParameter):
                        input_value = input_value.default_value
                    if isinstance(input_value, dict) and '$inputPath' in input_value.keys():
                        input_value = input_value['$inputPath']
                        param_type = 'LocalPath'
                    else:
                        param_type = type(input_value).__name__
                    # only primary pipeline add parameter values
                    if self.is_primary:
                        entity_dict = {'value': input_value}
                if param.value is not None and param_type == 'Any':
                    param_type = type(param.value).__name__
                entity_dict.update({'default': param.value,
                                    'type': param_type})
                inputs_outputs_dict['inputs'].update({param.key: entity_dict})

        pipeline_result = {}
        # add step type and ref
        description = self.instance.description
        pipeline_result.update({'$schema': self.schema})
        if not self.is_primary:
            pipeline_result.update({'type': self.type})
        pipeline_result.update({'name': self.instance.name,
                                'description': description})
        inputs_outputs_dict = {'inputs': {}, 'outputs': {}}
        update_pipeline_parameter()
        # Update pipeline output type
        # Find owner's interface output from Output builder
        for k, v in self.instance._definition.outputs.items():
            entity_dict = {k: {'type': v.type}}
            inputs_outputs_dict['outputs'].update(entity_dict)
        pipeline_result.update(inputs_outputs_dict)

        # expand steps inside pipeline
        steps = {}
        for node_instance in self.instance.nodes:
            node = provider.get_node_by_instance_id(node_instance._get_instance_id())
            steps.update(node.export_attribute(provider, directory_path, separate_file, parent_pipeline=self.instance))
            pipeline_result.update({"graph": steps})

        if self.target_ref is not None:
            pipeline_result.update({'target': self.target_ref})
        entity_dict = {self.relative_ref_name: pipeline_result}

        if separate_file:
            _dump_file(entity_dict=pipeline_result, directory_path=directory_path,
                       file_name=self.relative_ref_name)
        return entity_dict


class PipelineExportProvider:
    def __init__(self, graph, root_pipeline, pipelines, module_nodes, data_infos):
        self.graph = graph
        self.root_pipeline = root_pipeline
        self.pipelines = pipelines
        self.module_nodes = module_nodes
        data_sources = _unique(data_infos, _get_data_info_hash_id)
        self.data_sources = [ds for ds in data_sources if ds.dataset_type != 'parameter']
        self.module_version_dict = self._resolve_module_node_version_dict()
        self.instance_id_to_node_dict = self._prepare_instance_id_to_node_dict()
        self._pipeline_to_parent_dict = {}
        _prepare_pipeline_to_parent_pipeline_dict(self.root_pipeline, self._pipeline_to_parent_dict)

    def get_instance_variable_name(self, instance_id):
        if instance_id in self.instance_id_variable_name_dict.keys():
            return self.instance_id_variable_name_dict[instance_id]
        return None

    def _resolve_module_node_version_dict(self):
        """
        Resolve module version dict to determine the module ref name append id or not.

        :return: A dict with module name as key and module version set as value
        :rtype: bool, dict, dict[str, set]
        """
        module_version_dict = {}
        # resolve module name config
        for node in self.module_nodes:
            if node._definition.name not in module_version_dict.keys():
                module_version_dict[node._definition.name] = set()
            module_version_dict[node._definition.name].add(node._module_dto.module_version)
        return module_version_dict

    def _prepare_instance_id_to_node_dict(self) -> dict:
        """
        prepare metadata id to node dict,
            metadata id indicates module._instance_id or pipeline._id.

        :return: module._instance_id/pipeline._id to identifier mapping
        :rtype: dict[str, Union[ModuleNode, PipelineNode]]
        """
        instance_id_to_node_id_mapping = self.graph.module_node_to_graph_node_mapping
        for node in self.module_nodes:
            step_id = instance_id_to_node_id_mapping[node._get_instance_id()]
            instance_id_to_node_id_mapping[node.pipeline._id] = step_id
        instance_id_to_node_id_mapping.update({self.root_pipeline._id: ''})

        # create module node
        instance_id_to_node_dict = {module._get_instance_id(): ModuleNode(
            module=module, node_id=instance_id_to_node_id_mapping[module._get_instance_id()],
            ref_append_id=len(self.module_version_dict[module._definition.name]) > 1) for module in self.module_nodes}
        # create pipeline node
        instance_id_to_node_dict.update({pipeline._get_instance_id(): PipelineNode(
            pipeline=pipeline, node_id=pipeline._get_instance_id()) for pipeline in self.pipelines})
        return instance_id_to_node_dict

    def get_node_by_instance_id(self, instance_id) -> Union[ModuleNode, PipelineNode]:
        if instance_id not in self.instance_id_to_node_dict:
            raise Exception('Related node not found. Instance id {}'.format(instance_id))
        return self.instance_id_to_node_dict[instance_id]

    def get_parent_pipeline(self, node):
        if isinstance(node, Component) and not isinstance(node, Pipeline):
            return node.pipeline
        elif node in self._pipeline_to_parent_dict.keys():
            return self._pipeline_to_parent_dict[node]
        else:
            return self.root_pipeline

    def export_pipeline_entity(self, directory_path, separate_file=True):
        """
        Export a pipeline entity includes sub pipelines.

        :param directory_path: target directory path
        :type directory_path: str
        :param separate_file: separate file or not
        :type separate_file: bool
        :return: pipeline entity dict
        :rtype: dict
        """
        if separate_file:
            # Append pipeline name and suffix if directory path not empty
            directory_path = _get_valid_directory_path(
                os.path.join(directory_path, _sanitize_python_variable_name(self.root_pipeline.name)))
            os.mkdir(directory_path)
            os.mkdir(os.path.join(directory_path, 'modules'))
            os.mkdir(os.path.join(directory_path, 'datasets'))
        # resolve pipeline graph
        pipelines = {}
        pipeline_def_ids = set()
        for pipeline in self.pipelines:
            # ignore same sub pipeline definition
            def_id = pipeline._definition._id
            if def_id in pipeline_def_ids:
                continue
            pipeline_def_ids.add(def_id)
            pipeline_dict = self.get_node_by_instance_id(pipeline._get_instance_id()). \
                export_definition(self, directory_path=directory_path,
                                  separate_file=separate_file,
                                  parent_pipeline=pipeline._parent if pipeline._parent is not None else pipeline)
            pipelines.update(pipeline_dict)

        # resolve module references
        module_references = {}
        for module in self.module_nodes:
            node = self.get_node_by_instance_id(module._get_instance_id())
            module_references.update(
                node.export_definition(
                    provider=self, directory_path=directory_path,
                    separate_file=separate_file, parent_pipeline=module.pipeline))
        # resolve dataset references
        dataset_references = {}
        for data in self.data_sources:
            node = DatasetNode(data_info=data)
            dataset_references.update(node.export_definition(
                self, directory_path, separate_file, parent_pipeline=self.root_pipeline))
        if not separate_file:
            result = {'pipelines': pipelines}
            result.update({'modules': module_references})
            # resolve dataset references
            result.update({'datasets': dataset_references})
            _dump_file(entity_dict=result, directory_path=directory_path, file_name=self.root_pipeline.name,
                       ignore_dup=False)
        return directory_path
