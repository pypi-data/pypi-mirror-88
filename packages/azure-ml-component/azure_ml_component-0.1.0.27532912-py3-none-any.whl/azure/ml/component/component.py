# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains classes for creating and managing reusable computational units of an Azure Machine Learning pipeline.

A component is self-contained set of code that performs one step in the ML workflow (pipeline), such as data
preprocessing, model training, model scoring and so on. A component is analogous to a function, in that it has a name,
parameters, expects certain input and returns some value.

Component is designed to be reused in different jobs and can be evolved to adapt to different specific computation
logics in different usage cases. Anonymous Component can be used to improve an algorithm in a fast iteration mode,
and once the goal is achieved, the algorithm can be published as a registered Component which enables reuse.
"""

import importlib
import inspect
import json
import logging
import os
from pathlib import Path
import tempfile
import time
import types
from typing import Any, List, Callable, Mapping
import uuid

from azure.ml.component._api._api import _dto_2_definition
from azureml.core import Workspace, Datastore, Experiment, ScriptRunConfig
from azureml.core.run import Run
from azureml.core.runconfig import RunConfiguration, Data
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.tabular_dataset import TabularDataset
from azureml.data.abstract_datastore import AbstractDatastore
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data.data_reference import DataReference
from azureml.exceptions._azureml_exception import UserErrorException

from ._core._component_definition import CommandComponentDefinition, ComponentType
from ._debug._constants import DATA_REF_PREFIX
from ._dynamic import KwParameter, create_kw_method_from_parameters
from ._component_func import to_component_func, get_dynamic_input_parameter, \
    to_component_func_from_definition
from ._execution._component_run_helper import ComponentRunHelper
from ._execution._component_snapshot import _prepare_component_snapshot
from ._execution._tracker import RunHistoryTracker
from ._execution._component_run_helper import EXECUTION_LOGFILE
from ._component_validator import ComponentValidator
from ._module_dto import ModuleDto
from ._pipeline_parameters import PipelineParameter
from ._pipeline_data import PipelineData, DatasetRegistration
from .run_settings import RunSettings, _K8sRunSettings, _set_compute_field
from ._util._attr_dict import _AttrDict
from ._util._exceptions import ComponentValidationError
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._telemetry import TelemetryMixin, WorkspaceTelemetryMixin
from ._util._utils import _sanitize_python_variable_name, _get_or_sanitize_python_name, \
    _get_short_path_name, trans_to_valid_file_name

INPUT_TYPES = ['LocalPath', 'Dataset', 'Uri', 'Artifact']
_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class Input(TelemetryMixin):
    """Define one input of a Component."""

    _AVAILABLE_MODE = ['mount', 'download', 'direct']

    def __init__(self, dset, name: str, mode=None, owner=None):
        """Initialize an input of a component.

        :param dset: The input dataset.
        :type dset: azureml.core.Dataset
        :param name: The name of the input.
        :type name: str
        :param mode: The mode of the input.
        :type mode: str
        :param owner: The owner component of the input.
        :type owner: azure.ml.component.Component
        """
        super().__init__()
        self._dset = dset
        self._name = name
        self._owner = owner
        mode = 'direct' if isinstance(dset, TabularDataset) else 'mount'
        self._mode = mode

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="input_configure")
    def configure(self, mode='mount'):
        """
        Use this method to configure the input.

        :param mode: The mode that will be used for this input. Available options are
            'mount' and 'download'. See https://aka.ms/dataset-mount-vs-download for more details.
        :type mode: str
        """
        if mode not in self._AVAILABLE_MODE:
            raise UserErrorException("Invalid mode: '{}', only 'mount' or 'download' is allowed.".format(mode))

        if self._owner is not None:
            self._owner._specify_input_mode = True
        self._mode = mode

    @property
    def name(self):
        """Return the name of the input.

        :return: The name.
        :rtype: str
        """
        return self._name

    @property
    def mode(self):
        """Return the mode that will be used for this input.

        :return: The mode.
        :rtype: str
        """
        return self._mode

    def _is_dset_data_source(self):
        """Indicate whether the internal dset is a real data source."""
        if isinstance(self._dset, Input):
            return self._dset._is_dset_data_source()
        else:
            return self._dset is not None and not isinstance(self._dset, Output) \
                and not isinstance(self._dset, PipelineData)

    def _get_internal_data_source(self):
        """Get the dset iterativly until the dset is not an _InputBuilder."""
        if isinstance(self._dset, Input):
            return self._dset._get_internal_data_source()
        else:
            return self._dset

    def _build(self):
        from .pipeline import Pipeline
        if isinstance(self._dset, PipelineParameter):
            return self._dset
        if isinstance(self._dset, AbstractDataset):
            _last_build = None
            if hasattr(self._dset, 'last_build'):
                _last_build = self._dset.last_build
            elif self._mode == 'mount':
                _last_build = self._dset.as_named_input(self._name).as_mount()
            elif self._mode == 'download':
                _last_build = self._dset.as_named_input(self._name).as_download()
            elif self._mode == 'direct':
                _last_build = self._dset.as_named_input(self._name)
            self._dset.last_build = _last_build
            return _last_build
        elif isinstance(self._dset, Output):
            return self._dset._last_build
        elif isinstance(self._dset, Input):
            # usually, the _dset should always comes from a source or a output
            # the _dest may be _InputBuilder only to describe that
            # the destination comes from a specific subgraph dummy input port
            return self._dset._build()
        elif isinstance(self._dset, Component) or isinstance(self._dset, Pipeline):
            output_len = len(self._dset.outputs.values()) \
                if self._dset.outputs is not None else 0
            if output_len != 1:
                raise UserErrorException('{0} output(s) found of specified component/pipeline "{1}",'
                                         ' exactly 1 output required.'.format(output_len, self._dset.name))
            self._dset = list(self._dset.outputs.values())[0]
            return self._dset._last_build
        elif isinstance(self._dset, _AttrDict):
            output_len = len(self._dset.values())
            if output_len != 1:
                raise UserErrorException('{0} output(s) found of specified outputs,'
                                         ' exactly 1 output required.'.format(output_len))
            self._dset = list(self._dset.values())[0]
            return self._dset._last_build
        else:
            return self._dset

    def _get_telemetry_values(self):
        return self._owner._get_telemetry_values()


class Output(TelemetryMixin):
    """Define one output of a Component."""

    _AVAILABLE_MODE = ['mount', 'upload']

    def __init__(self, name: str, datastore=None, output_mode='mount', port_name=None,
                 owner=None):
        """Initialize an output of a component.

        :param name: The name of the output.
        :type name: str
        :param datastore: The datastore that will be used for the output.
        :type datastore: azureml.core.datastore.Datastore
        :param output_mode: Specifies whether to use "upload" or "mount" to access the data.
        :type output_mode: str
        :param port_name: The name to be shown of the output.
        :type port_name: str
        :param owner: The owner component of the output.
        :type owner: azure.ml.component.Component
        """
        super().__init__()
        self._datastore = datastore
        self._name = name
        self._output_mode = output_mode
        self._last_build = None
        self._port_name = port_name
        self._owner = owner
        self._dataset_registration = None

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="output_configure")
    def configure(self, datastore=None, output_mode='mount'):
        """
        Use this method to configure the output.

        :param datastore: The datastore that will be used for the output.
        :type datastore: azureml.core.datastore.Datastore
        :param output_mode: Specifies whether to use "upload" or "mount" to access the data.
        :type output_mode: str
        """
        if datastore is not None:
            if not isinstance(datastore, AbstractDatastore):
                raise UserErrorException(
                    'Invalid datastore type. Use azureml.core.Datastore for datastore construction.')
            self._datastore = datastore
            if self._owner is not None:
                self._owner._specify_output_datastore = True

        if output_mode != 'mount':
            if output_mode not in self._AVAILABLE_MODE:
                raise UserErrorException('Invalid mode: {}'.format(output_mode))

            self._output_mode = output_mode
            if self._owner is not None:
                self._owner._specify_output_mode = True

    @property
    def datastore(self):
        """Return the datastore of this output.

        :return: The datastore.
        :rtype: azureml.core.datastore.Datastore
        """
        return self._datastore

    @property
    def output_mode(self):
        """Return the output mode that will be used for the output.

        :return: The output mode.
        :rtype: str
        """
        return self._output_mode

    @property
    def port_name(self):
        """Return the output port name displayed to the user.

        :return: The displayed output port name.
        :rtype: str
        """
        return self._port_name

    def _build(self, producer=None, default_datastore=None):
        if self._datastore is None:
            self._datastore = default_datastore
        if self._datastore is None:
            raise ValueError("datastore is required")

        self._last_build = PipelineData(self._port_name, datastore=self._datastore, output_mode=self._output_mode,
                                        dataset_registration=self._dataset_registration)
        self._last_build._set_producer(producer)
        self._last_build._set_port_name(self._port_name)
        return self._last_build

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="OutputBuilder_register_as")
    def register_as(self, name, create_new_version: bool = True):
        """Register the output dataset to the workspace.

        .. remarks::

            Registration can only be applied to output but not input, this means if you only pass the object returned
            by this method to the inputs parameter of a pipline step, nothing will be registered. You must pass the
            object to the outputs parameter of a pipeline step for the registration to happen.

        :param name: The name of the registered dataset once the intermediate data is produced.
        :type name: str
        :param create_new_version: Whether to create a new version of the dataset if the data source changes. Defaults
            to True. By default, all intermediate output will output to a new location when a pipeline runs, so
            it is highly recommended to keep this flag set to True.
        :type create_new_version: bool
        :return: The output itself.
        :rtype: azure.ml.component.component.Output
        """
        self._dataset_registration = DatasetRegistration(name=name, create_new_version=create_new_version)
        return self

    def _get_telemetry_values(self):
        return self._owner._get_telemetry_values()


class _ComponentLoadSource(object):
    UNKNOWN = 'unknown'
    REGISTERED = 'registered'
    FROM_YAML = 'from_yaml'
    FROM_FUNC = 'from_func'
    FROM_NOTEBOOK = 'from_notebook'


class Component(WorkspaceTelemetryMixin):
    r"""
    An operational unit that can be used to produce a pipeline.

    A pipeline consists of a series of :class:`azure.ml.component.Component` nodes.

    .. remarks::

        Note that you should not use the constructor yourself. Use :meth:`azure.ml.component.Component.load`
        and related methods to acquire the needed :class:`azure.ml.component.Component`.

        The main functionality of the Component class resides at where we call "component function".
        A "component function" is essentially a function that you can call in Python code, which has parameters
        and returns the value that mimics the component definition in Azure Machine Learning.

        The following example shows how to create a pipeline using :class:`azure.ml.component.Component` class:

        .. code-block:: python

            # Suppose we have a workspace as 'ws'
            input1 = Dataset.get_by_name(ws, name='dset1')
            input2 = Dataset.get_by_name(ws, name='dset2')

            # Loading built-in component "Join Data" and "remove_duplicate_rows_func" as component functions
            join_data_component_func = Component.load(ws, name='azureml://Join Data')
            remove_duplicate_rows_func = Component.load(ws, name='azureml://Remove Duplicate Rows')

            # Use `azure.ml.component.dsl.Pipeline` to create a pipeline with two component nodes
            @dsl.pipeline(name='Sample pipeline',
                          description='Sample pipeline with two nodes',
                          default_compute_target='aml-compute')
            def sample_pipeline():
                # join_data_component_func is a dynamic-generated function, which has the signature of
                # the actual inputs & parameters of the "Join Data" component.
                join_data = join_data_component_func(
                    dataset1=input1,
                    dataset2=input2,
                    comma_separated_case_sensitive_names_of_join_key_columns_for_l=
                        "{\"KeepInputDataOrder\":true,\"ColumnNames\":[\"MovieId\"]}",
                    comma_separated_case_sensitive_names_of_join_key_columns_for_r=
                        "{\"KeepInputDataOrder\":true,\"ColumnNames\":[\"Movie ID\"]}",
                    match_case="True",
                    join_type="Inner Join",
                    keep_right_key_columns_in_joined_table="True"
                )
                # join_data is now a `azure.ml.component.Component` instance.

                # Note that function parameters are optional, you can just use remove_duplicate_rows_func()
                # and set the parameters afterwards using `set_inputs` method.
                remove_duplicate_rows = remove_duplicate_rows_func()

                remove_duplicate_rows.set_inputs(
                    # Note that we can directly use outputs of previous components.
                    dataset=join_data.outputs.result_dataset,
                    key_column_selection_filter_expression=
                        "{\"KeepInputDataOrder\":true,\"ColumnNames\":[\"Movie Name\", \"UserId\"]}",
                    retain_first_duplicate_row = "True"
                )

            pipeline = sample_pipeline()

            # Submit the run
            pipeline.submit(experiment_name="SamplePipeline", ws)

        Note that we prefer to use Dataset over DataReference in component SDK. The following example demonstrates
        how to register a dataset from data in Designer global datasets store:

        .. code-block:: python

            try:
                dset = Dataset.get_by_name(ws, 'Automobile_price_data_(Raw)')
            except Exception:
                global_datastore = Datastore(ws, name="azureml_globaldatasets")
                dset = Dataset.File.from_files(global_datastore.path('GenericCSV/Automobile_price_data_(Raw)'))
                dset.register(workspace=ws,
                            name='Automobile_price_data_(Raw)',
                            create_new_version=True)
                dset = Dataset.get_by_name(ws, 'Automobile_price_data_(Raw)')
            blob_input_data = dset
            component = some_component_func(input=blob_input_data)


    For more information about components, see:

    * `What's an azure ml component <https://github.com/Azure/DesignerPrivatePreviewFeatures>`_

    * `Define a component using component specs <https://aka.ms/azureml-component-specs>`_
    """

    def __init__(self, definition: CommandComponentDefinition, _init_params: Mapping[str, str],
                 _is_direct_child=True):
        """Initialize a component with a component definition.

        :param definition: The CommandComponentDefinition object which describe the interface of the component.
        :type definition: azure.ml.component._core._component_definition.CommandComponentDefinition
        :param _init_params: (Internal use only.) The init params will be used to initialize inputs and parameters.
        :type _init_params: dict
        :param _is_direct_child: If there is a pipeline component definition
            is_direct_child means whether the component is current definition's direct child.
        :type _is_direct_child: bool
        """
        WorkspaceTelemetryMixin.__init__(self, definition.workspace)
        self._workspace = definition.workspace
        self._definition = definition
        self._name_to_argument_name_mapping = {
            **{p.name: arg for arg, p in definition.inputs.items()},
            **{p.name: arg for arg, p in definition.parameters.items()},
            **{p.name: arg for arg, p in definition.outputs.items()},
        }

        # Generate an id for every component instance
        self._instance_id = str(uuid.uuid4())

        # Telemetry
        self._specify_input_mode = False
        self._specify_output_mode = False
        self._specify_output_datastore = False
        self._specify_runsettings = False
        self._specify_k8srunsettings = False

        self._init_public_interface(_init_params)

        self._name = definition.name
        self._runsettings = RunSettings(definition.runsettings, definition.name, definition.workspace, self)
        self._k8srunsettings = _K8sRunSettings(definition.k8srunsettings, self) if definition.k8srunsettings else None
        self._env = None

        self._init_dynamic_method()
        self._regenerate_output = None

        if _is_direct_child:
            # Add current component to global parent pipeline if there is one
            from ._pipeline_component_definition_builder import _add_component_to_current_definition_builder
            _add_component_to_current_definition_builder(self)

    #  region Private Methods

    def _init_public_interface(self, init_params):
        # Pipeline component definition usage
        self._init_params = {} if init_params is None else init_params
        # Extra settings record the inputs and parameters using configure function after component created.
        self._extra_input_settings = {}
        self._extra_runsettings = {}

        # Keep order of inputs as definition
        input_builder_map = {
            name: Input(init_params[name], name=name, owner=self)
            for name, _input in self._definition.inputs.items()
            if name in init_params.keys()
        }
        self._inputs = _AttrDict(input_builder_map)

        # Keep order of parameters as definition
        self._parameter_params = {
            name: init_params[name] for name, _input in self._definition.parameters.items()
            if name in init_params.keys()
        }

        output_builder_map = {
            name: Output(name, port_name=output.name, owner=self)
            for name, output in self._definition.outputs.items()
        }
        self._outputs = _AttrDict(output_builder_map)

        self._pythonic_name_to_parameter_map = {name: name for name in self._definition.parameters}

        self._pythonic_name_to_input_map = {
            name: input.name
            for name, input in self._definition.inputs.items()
        }
        self._pythonic_name_to_output_map = {
            name: output.name
            for name, output in self._definition.outputs.items()
        }

        # TODO: Remove the following properties once the validation logic is refined
        interface = self._definition._module_dto.module_entity.structured_interface
        self._interface_inputs = interface.inputs
        self._interface_parameters = interface.parameters
        self._interface_outputs = interface.outputs

    def _init_dynamic_method(self):
        """Update methods set_inputs according to the component input/param definitions."""
        # Here we set all default values as None to avoid overwriting the values by default values.
        transformed_parameters = [
            KwParameter(name=name, annotation=str(param.type), default=None, _type=str(param.type))
            for name, param in self._definition.parameters.items()]
        self.set_inputs = create_kw_method_from_parameters(
            self.set_inputs, get_dynamic_input_parameter(self._definition) + transformed_parameters,
        )

    def _build_outputs_map(self, producer=None, default_datastore=None) -> Mapping[str, Any]:
        """Build a map from output name -> DatasetConsumptionConfig."""
        return {
            output.name: self._outputs[arg_name]._build(producer, default_datastore)
            for arg_name, output in self._definition.outputs.items()
        }

    def _build_inputs_map(self) -> Mapping[str, Any]:
        """Build a map from input name -> DatasetConsumptionConfig."""
        inputs_map = {}
        for arg_name, input in self._definition.inputs.items():
            value = self._inputs.get(arg_name)
            if value is None:
                continue
            value = value._build()
            if value is not None:
                inputs_map[input.name] = value
        return inputs_map

    def _build_params(self) -> Mapping[str, Any]:
        """Build a map from param name -> param value."""
        return {
            param.name: self._parameter_params[name] for name, param in self._definition.parameters.items()
            if self._parameter_params.get(name) is not None
        }

    def _resolve_compute(self, default_compute, is_local_run=False):
        """
        Resolve compute to tuple.

        :param default_compute: pipeline compute specified.
        :type default_compute: tuple(name, type)
        :param is_local_run: whether component execute in local
        :type is_local_run: bool
        :return: (resolve compute, use_component_compute)
        :rtype: tuple(tuple(name, type), bool)
        """
        if not isinstance(default_compute, tuple):
            raise TypeError("default_compute must be a tuple")

        runsettings = self._runsettings
        target = runsettings.target

        if target is None or target == 'local':
            if default_compute[0] is None and not is_local_run:
                raise UserErrorException("A compute target must be specified")
            return default_compute, False

        if isinstance(target, tuple):
            return target, True
        elif isinstance(target, str):
            default_compute_name, _ = default_compute
            if target == default_compute_name:
                return default_compute, True

            # try to resolve
            _targets = self._workspace.compute_targets
            target_in_workspace = _targets.get(target)
            if target_in_workspace is None:
                print('target={}, not found in workspace, assume this is an AmlCompute'.format(target))
                return (target, "AmlCompute"), True
            else:
                return (target_in_workspace.name, target_in_workspace.type), True
        else:
            return target, True

    def _get_telemetry_values(self, compute_target=None, additional_value=None):
        """
        Get telemetry value out of a Component.

        The telemetry values include the following entries:

        * load_source: The source type which the component node is loaded.
        * specify_input_mode: Whether the input mode is being by users.
        * specify_output_mode: Whether the output mode is being by users.
        * specify_output_datastore: Whether the output datastore is specified by users.
        * specify_runsettings: Whether the runsettings is specified by users.
        * specify_k8srunsettings: Whether the k8srunsettings is specified by users.
        * pipeline_id: the pipeline_id if the component node belongs to some pipeline.
        * specify_node_level_compute: Whether the node level compute is specified by users.
        * compute_type: The compute type that the component uses.

        :param compute_target: The compute target.
        :return: telemetry values.
        :rtype: dict
        """
        telemetry_values = super()._get_telemetry_values()
        telemetry_values.update(self._module_dto._get_telemetry_values())
        telemetry_values['load_source'] = self._definition._load_source
        telemetry_values['specify_input_mode'] = self._specify_input_mode
        telemetry_values['specify_output_mode'] = self._specify_output_mode
        telemetry_values['specify_output_datastore'] = self._specify_output_datastore
        telemetry_values['specify_runsettings'] = self._specify_runsettings
        telemetry_values['specify_k8srunsettings'] = self._specify_k8srunsettings

        node_compute_target, specify_node_level_compute = self._resolve_compute(compute_target) \
            if compute_target is not None else (None, False)

        if hasattr(self, 'pipeline'):
            telemetry_values['pipeline_id'] = self.pipeline._id
        if node_compute_target is not None:
            telemetry_values['specify_node_level_compute'] = specify_node_level_compute
            telemetry_values['compute_type'] = node_compute_target[1]

        telemetry_values.update(additional_value or {})
        return telemetry_values

    def _get_instance_id(self):
        return self._instance_id

    def _get_run_setting(self, name, expected_type, default_value=None):
        """Get run setting with name, returns default_value if didn't find or type did not match expected_type."""
        try:
            val = getattr(self._runsettings, name)
            if not isinstance(val, expected_type):
                raise ValueError("{} should be returned.".format(expected_type))
            else:
                return val
        except (AttributeError, ValueError):
            return default_value

    def _get_default_parameters(self):
        """Get exposed parameters' key-value pairs."""
        return {param.name: param.default for param in self._definition.parameters.values()}

    def _populate_runconfig(self, use_local_compute=False):
        """Populate runconfig from component."""
        raw_conf = json.loads(self._module_dto.module_entity.runconfig)
        run_config = RunConfiguration._get_runconfig_using_dict(raw_conf)
        run_config._target, compute_type = ('local', None) if use_local_compute else self._runsettings.target

        _set_compute_field(self._k8srunsettings, compute_type, run_config)

        if hasattr(self._runsettings, 'process_count_per_node'):
            if use_local_compute:
                # When running in local, process count per node can be absent, we will set 1 for it.
                if self.type == ComponentType.MPIComponent.value:
                    run_config.mpi.process_count_per_node = self._get_run_setting('process_count_per_node', int, 1)
            else:
                run_config.mpi.process_count_per_node = self._runsettings.process_count_per_node
        if hasattr(self._runsettings, 'node_count'):
            if use_local_compute:
                # When running in local, node count is always 1
                run_config.node_count = 1
            else:
                run_config.node_count = self._runsettings.node_count

        return run_config

    def _replace(self, new_component: 'Component'):
        """Replace component in pipeline. Use it cautiously."""
        self._workspace = new_component.workspace
        self._definition = new_component._definition

    def _replace_inputs(self, *args, **kwargs) -> 'Component':
        """Replace the inputs of component."""
        self._inputs = _AttrDict({k: Input(v, k, owner=self) for k, v in kwargs.items()})
        return self

    def _replace_parameters(self, *args, **kwargs) -> 'Component':
        """Replace the parameters of component."""
        self._parameter_params = {k: v for k, v in kwargs.items()}
        return self

    def _is_replace_target(self, target: 'Component'):
        """
        Provide for replace a component in pipeline.

        Check if current node(component) is the target one we want

        :return: Result of comparision between two components
        :rtype: bool
        """
        if target.name != self.name:
            return False
        if target._identifier != self._identifier:
            return False
        return True

    def _get_environment(self):
        """Get environment of component by deserializing runconfig or definition."""
        if self._env is None:
            # When component is initialized by ComponentDefinition, using _definition to get environment.
            env = self._definition.environment._to_aml_sdk_env()
            # When register environment, it need to set environment name and will generate conda env name by hash
            # env info, except name. Since environments with same env info and diff name, have same conda env name.
            # Because component name may containe strange character, using component identifier as env name to
            # avoid registering failure.
            env.name = self._identifier
            self._env = env.register(self.workspace)
        return self._env

    @staticmethod
    def _from_func_imp(
            workspace: Workspace,
            func: types.FunctionType,
            force_reload=True,
            load_source=_ComponentLoadSource.UNKNOWN
    ) -> Callable[..., 'Component']:
        def _reload_func(f: types.FunctionType):
            """Reload the function to make sure the latest code is used to generate yaml."""
            module = importlib.import_module(f.__module__)
            # if f.__name__ == '__main__', reload will throw an exception
            if f.__module__ != '__main__':
                from azure.ml.component.dsl._utils import _force_reload_module
                _force_reload_module(module)
            return getattr(module, f.__name__)

        if force_reload:
            func = _reload_func(func)
        # Import here to avoid circular import.
        from azure.ml.component.dsl._component import ComponentExecutor
        from azure.ml.component.dsl._module_spec import SPEC_EXT
        from azure.ml.component.dsl._utils import _temporarily_remove_file
        # If a ComponentExecutor instance is passed, we directly use it,
        # otherwise we construct a ComponentExecutor with the function
        executor = func if isinstance(func, ComponentExecutor) else ComponentExecutor(func)
        # Use a temp spec file to register.
        temp_spec_file = Path(inspect.getfile(func)).absolute().with_suffix(SPEC_EXT)
        temp_conda_file = temp_spec_file.parent / 'conda.yaml'
        conda_exists = Path(temp_conda_file).is_file()
        # the conda may be the notebook gen conda, cannot temporarily remove if exists
        with _temporarily_remove_file(temp_spec_file):
            try:
                temp_spec_file = executor.to_spec_yaml(folder=temp_spec_file.parent,
                                                       spec_file=temp_spec_file.name)
                return Component._from_module_spec(workspace=workspace, yaml_file=str(temp_spec_file),
                                                   load_source=load_source)
            finally:
                if not conda_exists and Path(temp_conda_file).is_file():
                    Path(temp_conda_file).unlink()

    @staticmethod
    def _from_module_spec(
            workspace: Workspace,
            yaml_file: str,
            load_source: str
    ) -> Callable[..., 'Component']:
        definition = CommandComponentDefinition.register(
            workspace, spec_file=yaml_file, package_zip=None,
            anonymous_registration=True,
            set_as_default=False, amlignore_file=None, version=None,
        )
        definition._load_source = load_source

        return Component._component_func_from_definition(definition)

    @staticmethod
    def _component_func(
            workspace: Workspace,
            module_dto: ModuleDto,
            load_source: str = _ComponentLoadSource.UNKNOWN,
            return_yaml=True
    ) -> Callable[..., 'Component']:
        """
        Get component func from ModuleDto.

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param module_dto: ModuleDto instance
        :type module_dto: azure.ml.component._module_dto
        :param load_source: The source which the component is loaded.
        :type load_source: str
        :return: a function that can be called with parameters to get a :class:`azure.ml.component.Component`
        :rtype: function
        """
        def create_component_func(**kwargs) -> 'Component':
            definition = _dto_2_definition(module_dto, workspace)
            # TODO: Set the source when initialize the definition.
            definition._load_source = load_source
            return Component(definition, _init_params=kwargs)

        return to_component_func(ws=workspace, module_dto=module_dto, return_yaml=return_yaml,
                                 component_creation_func=create_component_func)

    @staticmethod
    def _component_func_from_definition(
            definition: CommandComponentDefinition,
    ):
        def create_component_func(**kwargs) -> 'Component':
            return Component(definition, _init_params=kwargs)

        return to_component_func_from_definition(definition=definition,
                                                 component_creation_func=create_component_func)

    # endregion

    # region Local run

    def _transfer_params(self, run_id, params, runconfig):
        """Transfer params from DataReference to runconfig's setting."""
        transfered_params = {}
        for key, value in params.items():
            # Use command line option from module dto
            k = self._get_argument_name_by_name(key)
            v = "{}{}".format(DATA_REF_PREFIX, key)
            if isinstance(value, DataReference):
                runconfig.data_references[key] = value.to_config()
            elif isinstance(value, DatasetConsumptionConfig):
                value.dataset._ensure_saved(self._workspace)
                runconfig.data[key] = Data.create(value)
            elif isinstance(value, PipelineData):
                # ScriptRunConfig can't use DataReference directly
                out_key = "outputs"
                # This path will be showed on portal's outputs if datastore is workspaceblobstore
                path = "{}/{}/{}/{}".format("azureml", run_id, out_key, key)
                data_ref = value.datastore.path(path)
                runconfig.data_references[key] = data_ref.to_config()
            else:
                v = value
            transfered_params[k] = v
        return transfered_params

    def _get_argument_name_by_name(self, name):
        """Return the argument name of an input/output according its name."""
        return self._name_to_argument_name_mapping.get(name)

    def _input_is_optional(self, argument_name):
        return self._definition.inputs[argument_name].optional

    def _get_input_name_by_argument_name(self, argument_name):
        return self._definition.inputs[argument_name].name

    def _output_is_file(self, argument_name):
        """Return True if the output is expected to be a file instead of a directory.

        This is only used in Component.run, will be refined in the future.
        """
        return self._definition.outputs[argument_name].type == 'AnyFile'

    def _build_arguments_for_run_config(self, run_config, run_id):
        """Build argument for run config and fill data reference in it."""
        arguments = []
        default_datastore = Datastore.get(self._workspace, 'workspaceblobstore')
        input_params = self._transfer_params(run_id, self._build_inputs_map(), run_config)
        output_params = self._transfer_params(
            run_id,
            self._build_outputs_map(default_datastore=default_datastore),
            run_config)
        arguments = self._get_arguments(input_params, output_params)
        return arguments

    def _get_script(self):
        """Get component script."""
        runconfig = json.loads(self._module_dto.module_entity.runconfig)
        framework = None if 'Framework' not in runconfig else runconfig['Framework']
        if framework and framework.lower() != 'python':
            raise NotImplementedError('Unsupported framework {}, only Python is supported now.'.format(framework))
        elif not framework:
            raise Exception('Framework in runconfig is None')
        script = None if 'Script' not in runconfig else runconfig['Script']
        if not script:
            raise Exception('Script in runconfig is None')
        return script

    def _get_arguments(self, input_path, output_path, remove_none_value=True):
        """
        Get component arguments.

        :param input_path: Replace input port value
        :type input_path: dict
        :param output_path: Replace output port value
        :type output_path: dict
        :return: a list that contains component arguments, and a dict contains environment variables component needed
        :rtype: list
        """
        # TODO: Refine the logic with definition.command
        def _get_argument_value(argument, parameter_params, input_path, output_path):
            arg_value = None

            if argument.value_type == '0':
                # Handle anonymous_component output
                output_prefix = 'DatasetOutputConfig:'
                if argument.value.startswith(output_prefix):
                    arg_value_key = _get_or_sanitize_python_name(argument.value[len(output_prefix):],
                                                                 self._module_dto.module_python_interface
                                                                 .outputs_name_mapping)
                    if arg_value_key in output_path:
                        return output_path[arg_value_key]
                return argument.value
            elif argument.value_type == '1':
                # Get parameter argument value
                arg_value_key = self._module_dto\
                    .module_python_interface.parameters_name_mapping.get(argument.value)
                if arg_value_key is None:
                    arg_value_key = _sanitize_python_variable_name(argument.value)
                if arg_value_key in parameter_params:
                    if parameter_params[arg_value_key] is not None:
                        arg_value = str(parameter_params[arg_value_key])
                    else:
                        arg_value = parameter_params[arg_value_key]
                else:
                    arg_value = argument.value
            elif argument.value_type == '2':
                # Get input argument value
                arg_value_key = self._module_dto\
                    .module_python_interface.inputs_name_mapping.get(argument.value)
                if arg_value_key is None:
                    arg_value_key = _sanitize_python_variable_name(argument.value)
                if arg_value_key in input_path:
                    arg_value = input_path[arg_value_key]
                else:
                    arg_value = None
            elif argument.value_type == '3':
                # Get output argument value
                arg_value_key = self._module_dto\
                    .module_python_interface.outputs_name_mapping.get(argument.value)
                if arg_value_key is None:
                    arg_value_key = _sanitize_python_variable_name(argument.value)
                if arg_value_key in output_path:
                    arg_value = output_path[arg_value_key]
            elif argument.value_type == '4':
                # Get nestedList argument value
                arg_value = []
                for sub_arg in argument.nested_argument_list:
                    sub_arg_value = _get_argument_value(sub_arg, parameter_params, input_path, output_path)
                    arg_value.append(sub_arg_value)
            return arg_value

        arguments = self._module_dto.module_entity.structured_interface.arguments
        parameter_params = self._parameter_params
        ret = []

        for arg in arguments:
            arg_value = _get_argument_value(arg, parameter_params, input_path, output_path)
            ret.append(arg_value)

        def flatten(arr):
            for element in arr:
                if hasattr(element, "__iter__") and not isinstance(element, str):
                    for sub in flatten(element):
                        yield sub
                else:
                    yield element

        ret = list(flatten(ret))
        if remove_none_value:
            # Remove None value and its flag in arguments
            ret = [x[0]
                   for x in zip(ret, ret[1:] + ret[-1::]) if (x[0] and x[1])]

        return ret

    def _validate_parameters(self, parameters):
        if parameters is None:
            return
        # Print warning if there is unrecognized parameter key.
        for _p in parameters.keys():
            if _p not in self._parameter_params and _p not in self._inputs:
                logging.warning('Parameter \'{}={}\' was unrecognized by pipeline {} and will be ignored.'.format(
                    _p, parameters[_p], self.name
                ))
    # endregion

    # region Public Methods

    @property
    def name(self):
        """
        Get the name of the Component.

        :return: The name.
        :rtype: str
        """
        return self._definition.name

    @property
    def display_name(self):
        """
        Get the display name of the Component.

        :return: The display name.
        :rtype: str
        """
        return self._definition.display_name

    @property
    def type(self):
        """
        Get the type of the Component.

        :return: The type.
        :rtype: str
        """
        return self._definition.type.value

    @property
    def inputs(self) -> _AttrDict[str, Input]:
        """Get the inputs of the Component.

        :return: The dict in which the keys are input names, the values are input instances initialized by datasets.
        :rtype: dict[str, Input]
        """
        return self._inputs

    @property
    def outputs(self) -> _AttrDict[str, Output]:
        """Get the outputs of the Component.

        :return: The dict in which the keys are the output names, the values are the output instances.
        :rtype: dict[str, Output]
        """
        return self._outputs

    @property
    def runsettings(self):
        """
        Get run settings of the Component.

        :return: The run settings.
        :rtype: azure.ml.component.RunSettings
        """
        return self._runsettings

    @property
    def k8srunsettings(self):
        """
        Get compute run settings of the Component.

        :return: The compute run settings
        :rtype: _K8sRunSettings
        """
        return self._k8srunsettings

    @property
    def workspace(self):
        """
        Get the workspace of the Component.

        :return: The workspace.
        :rtype: azureml.core.Workspace
        """
        return self._definition.workspace

    @property
    def regenerate_output(self):
        """
        Get or set the flag indicating whether the component should be run again.

        Set to True to force a new run (disallows component/datasource reuse).

        :return: the regenerate_output value.
        :rtype: bool
        """
        return self._regenerate_output

    @regenerate_output.setter
    def regenerate_output(self, regenerate_output):
        self._regenerate_output = regenerate_output

    @property
    def _module_dto(self):
        # TODO: Remove all reference to this
        return self._definition._module_dto

    @property
    def _identifier(self):
        """Return the identifier of the component.

        :return: The identifier.
        :rtype: str
        """
        return self._definition.identifier

    @property
    def version(self):
        """Return the version of the component.

        :return: The version.
        :rtype: str
        """
        return self._definition.version

    @property
    def created_by(self):
        """Return the name who created the corresponding component in the workspace.

        :return: The name who created the component.
        :rtype: str
        """
        return self._definition.creation_context.created_by

    @property
    def created_date(self):
        """Return the created date of the corresponding component in the workspace.

        :return: The created date with the ISO format.
        :rtype: str
        """
        return self._definition.creation_context.created_date

    @property
    def _id(self):
        """Return the instance id of component.

        :return: The unique instance id.
        :rtype: str
        """
        return self._instance_id

    def set_inputs(self, *args, **kwargs) -> 'Component':
        """Update the inputs and parameters of the component.

        :return: The component itself.
        :rtype: azure.ml.component.Component
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        self._validate_parameters(kwargs)
        self.inputs.update(
            {k: Input(v, k, owner=self) for k, v in kwargs.items()
             if v is not None and k in self._inputs.keys()})
        self._parameter_params.update(
            {k: v for k, v in kwargs.items()
             if v is not None and k in self._pythonic_name_to_parameter_map.keys()})
        self._extra_input_settings.update(kwargs)
        return self

    def _validate(self, raise_error=False, pipeline_parameters=None):
        """
        Validate that all the inputs and parameters are in fact valid.

        :param raise_error: Whether to raise exceptions on error
        :type raise_error: bool
        :param pipeline_parameters: The pipeline parameters provided.
        :type pipeline_parameters: dict

        :return: The errors found during validation.
        :rtype: builtin.list
        """
        # Validate inputs
        errors = []

        def process_error(e: Exception, error_type):
            ve = ComponentValidationError(str(e), e, error_type)
            if raise_error:
                raise ve
            else:
                errors.append({'message': ve.message, 'type': ve.error_type})

        def update_provided_inputs(provided_inputs, pipeline_parameters):
            if pipeline_parameters is None:
                return provided_inputs
            _provided_inputs = {}
            for k, v in provided_inputs.items():
                _input = v._get_internal_data_source()
                if not isinstance(_input, PipelineParameter) or _input.name not in pipeline_parameters.keys():
                    _provided_inputs[k] = v
                else:
                    _provided_inputs[k] = (Input(PipelineParameter(
                        name=_input.name, default_value=pipeline_parameters[_input.name]),
                        name=v.name, mode=v.mode, owner=v._owner))
            return _provided_inputs

        def update_provided_parameters(provided_parameters, pipeline_parameters):
            _params = {}
            for k, v in provided_parameters.items():
                _input = v._get_internal_data_source() if isinstance(v, Input) else v
                if not isinstance(_input, PipelineParameter) or \
                        pipeline_parameters is None or \
                        _input.name not in pipeline_parameters.keys():
                    _params[k] = _input
                else:
                    _params[k] = pipeline_parameters[_input.name]
            return _params

        provided_inputs = update_provided_inputs(self._inputs, pipeline_parameters)
        ComponentValidator.validate_module_inputs(provided_inputs=provided_inputs,
                                                  interface_inputs=self._interface_inputs,
                                                  param_python_name_dict=self._module_dto.module_python_interface
                                                  .inputs_name_mapping,
                                                  process_error=process_error)

        provided_parameters = update_provided_parameters(self._parameter_params, pipeline_parameters)
        ComponentValidator.validate_module_parameters(provided_parameters=provided_parameters,
                                                      interface_parameters=self._interface_parameters,
                                                      param_python_name_dict=self._module_dto.module_python_interface
                                                      .parameters_name_mapping,
                                                      process_error=process_error)

        ComponentValidator.validate_runsettings(runsettings=self._runsettings,
                                                process_error=process_error)

        ComponentValidator.validate_k8srunsettings(k8srunsettings=self._k8srunsettings,
                                                   process_error=process_error)

        return errors

    def run(self, experiment_name=None, working_dir=None, use_docker=True,
            track_run_history=True, show_output=True, python_interpreter_path=None,
            skip_validation=True, raise_on_error=True, **kwargs):
        """
        Run component in local environment.

        .. remarks::

            Note that after execution of this method, scripts, output dirs, and log files will be created in
            working dir. Below is an usage example.

            .. code-block:: python

                # Suppose we have a workspace as 'ws'
                # First, load a component, and set parameters of component
                ejoin = Component.load(ws, name='microsoft.com.bing.ejoin')
                component = ejoin(leftcolumns='m:name;age', rightcolumns='income',
                    leftkeys='m:name', rightkeys='m:name', jointype='HashInner')
                # Second, set prepared input path and output path to run component in local. If not set working_dir,
                # will create it in temp dir. In this example, left_input and right_input are input port of ejoin.
                # And after running, output data and log will write in working_dir
                component.set_inputs(left_input=your_prepare_data_path)
                component.set_inputs(right_input=your_prepare_data_path)

                # Run component with docker-based environment
                result = component.run(working_dir=dataset_output_path, use_docker=True)

                # Run component with conda-based environment
                result = component.run(working_dir=dataset_output_path, use_docker=False)

                # Run component with user-managed environment
                result = component.run(
                    working_dir=dataset_output_path, use_docker=False, python_interpreter_path=sys.executable())

        :param experiment_name: The experiment_name will show in portal. If not set, will use component name.
        :type experiment_name: str
        :param working_dir: The output path for component output info
        :type working_dir: str
        :param use_docker: If use_docker=True, will pull image from azure and run component in system-managed
                           docker-based environment.
                           If use_docker=False and python_interpreter_path is None, will run component in
                           system-managed conda-based environment.
                           If use_docker=False and python_interpreter_path is not None, will directly run component
                           in user-managed environment.
        :type use_docker: bool
        :param track_run_history: If track_run_history=True, will create azureml.core.Run and upload component output
                                  and log file to portal.
                                  If track_run_history=False, will not create azureml.core.Run to upload outputs
                                  and log file.
        :type track_run_history: bool
        :param show_output: Indicates whether to show the component run status on sys.stdout.
        :type show_output: bool
        :param python_interpreter_path: When use_docker=False and python_interpreter_path not None, will directly
                                        run component in user-managed environment.
                                        When use_docker=False and python_interpreter_path is None, will run component
                                        in system-managed conda-based environment.
        :type python_interpreter_path: str
        :param skip_validation: Indicates whether to skip the validation of the component.
        :type skip_validation: bool
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool

        :return: The run status, such as, Completed and Failed.
        :rtype: str
        """
        from .pipeline import Pipeline
        if isinstance(self, Pipeline):
            return self._run(experiment_name=experiment_name, working_dir=working_dir, use_docker=use_docker,
                             track_run_history=track_run_history, show_output=show_output,
                             python_interpreter_path=python_interpreter_path, raise_on_error=raise_on_error, **kwargs)
        else:
            return self._run(experiment_name=experiment_name, working_dir=working_dir, use_docker=use_docker,
                             track_run_history=track_run_history, show_output=show_output,
                             python_interpreter_path=python_interpreter_path,
                             skip_validation=skip_validation, raise_on_error=raise_on_error)

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name='Component_run')
    def _run(self, experiment_name=None, working_dir=None, use_docker=True,
             track_run_history=True, show_output=True, python_interpreter_path=None,
             skip_validation=True, raise_on_error=True):
        """
        Run component in local environment.

        :param experiment_name: The experiment_name will show in portal. If not set, will use component name.
        :type experiment_name: str
        :param working_dir: The output path for component output info
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
        :param show_output: Indicates whether to show the component run status on sys.stdout.
        :type show_output: bool
        :param python_interpreter_path: When use_docker=False and python_interpreter_path not None, will directly
                                        run component in user-managed environment.
                                        When use_docker=False and python_interpreter_path is None, will run component
                                        in system-managed conda-based environment.
        :type python_interpreter_path: str
        :param skip_validation: Indicates whether to skip the validation of the component.
        :type skip_validation: bool
        :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
        :type raise_on_error: bool

        :return: The run status, such as, Completed and Failed.
        :rtype: str
        """
        # TODO: Do not skip validation in default, ignore runsetting parameter validation when using component.run
        if not skip_validation:
            self._validate(raise_error=True)
        if not self.type or self.type not in {
            ComponentType.CommandComponent.value, ComponentType.MPIComponent.value,
            ComponentType.ParallelComponent.value,
        }:
            raise UserErrorException(
                'Unsupported component type {}, " \
                "only Command/MPI/Parallel Component is supported now.'.format(self.type))
        if not working_dir:
            working_dir = os.path.join(tempfile.gettempdir(), trans_to_valid_file_name(self.name))
        short_working_dir = _get_short_path_name(working_dir, create_dir=True)
        print('working dir is {}'.format(working_dir))

        # prepare input dataset
        ComponentRunHelper.download_datasets(
            [dataset._dset for dataset in self.inputs.values()], self.workspace, short_working_dir)
        # prepare component image
        if use_docker or not python_interpreter_path:
            ComponentRunHelper.prepare_component_env(self, short_working_dir, use_docker)

        experiment_name = experiment_name if experiment_name else _sanitize_python_variable_name(self.display_name)
        tracker = RunHistoryTracker.with_definition(
            experiment_name=experiment_name,
            track_run_history=track_run_history,
            component=self,
            working_dir=None,
            path=EXECUTION_LOGFILE)
        component_run_helper = ComponentRunHelper(
            self, short_working_dir, use_docker=use_docker, tracker=tracker, show_output=show_output)
        return component_run_helper.component_run(python_interpreter_path, raise_on_error)

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="Component_submit")
    def _submit(self, experiment_name=None, source_dir=None, tags=None) -> Run:
        """Submit component to remote compute target.

        .. remarks::

            Submit is an asynchronous call to the Azure Machine Learning platform to execute a trial on
            remote hardware.  Depending on the configuration, submit will automatically prepare
            your execution environments, execute your code, and capture your source code and results
            into the experiment's run history.
            An example of how to submit an experiment from your local machine is as follows:

            .. code-block:: python

                # Suppose we have a workspace as 'ws'
                # First, load a component, and set parameters of component
                train_component_func = Component.load(ws, name='microsoft.com/aml/samples://Train')
                train_data = Dataset.get_by_name(ws, 'training_data')
                train = train_component_func(training_data=train_data, max_epochs=5, learning_rate=0.01)
                # Second, set compute target for component then add compute running settings.
                # After running finish, the output data will be in outputs/$output_file
                train.runsettings.configure(target="k80-16-c")
                train.runsettings.resource_configuration.configure(gpu_count=1, is_preemptible=True)
                run = train.submit(experiment_name="component-submit-test")
                print(run.get_portal_url())
                run.wait_for_completion()

        :param experiment_name: The experiment name
        :type experiment_name: str
        :param source_dir: The source dir is where the machine learning scripts locate
        :type source_dir: str
        :param tags: Tags to be added to the submitted run, e.g., {"tag": "value"}
        :type tags: dict

        :return: The submitted run.
        :rtype: azureml.core.Run
        """
        if self._runsettings.target is None:
            raise UserErrorException("Submit require a remote compute configured.")
        if experiment_name is None:
            experiment_name = _sanitize_python_variable_name(self.display_name)
        if source_dir is None:
            source_dir = os.path.join(tempfile.gettempdir(), self._identifier)
            print("[Warning] script_dir is None, create tempdir: {}".format(source_dir))
        experiment = Experiment(self._workspace, experiment_name)
        run_config = self._populate_runconfig()

        script = run_config.script
        if not os.path.isfile("{}/{}".format(source_dir, script)):
            print("[Warning] Can't find {} from {}, will download from remote".format(script, source_dir))
            _prepare_component_snapshot(self, source_dir)

        run_id = experiment_name + "_" + \
            str(int(time.time())) + "_" + str(uuid.uuid4())[:8]
        arguments = self._build_arguments_for_run_config(run_config, run_id)

        src = ScriptRunConfig(source_directory=source_dir, script=script,
                              arguments=arguments, run_config=run_config)
        run = experiment.submit(config=src, tags=tags, run_id=run_id)
        print('Link to Azure Machine Learning Portal:', run.get_portal_url())
        return run

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API)
    def batch_load(workspace: Workspace, selectors: List[str] = None, ids: List[str] = None) -> \
            List[Callable[..., 'Component']]:
        """
        Batch load components by identifier list.

        If there is an exception with any component, the batch load will fail. Partial success is not allowed.

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param selectors: A list of str formatted as name:version or name@label
        :type selectors: builtin.list[str]
        :param ids: The component version ids
        :type ids: builtin.list[str]

        :return: A tuple of component functions
        :rtype: tuple(function)
        """
        definitions = CommandComponentDefinition.batch_get(workspace, ids, selectors)
        telemetry_values = WorkspaceTelemetryMixin._get_telemetry_value_from_workspace(workspace)
        telemetry_values.update({
            'count': len(definitions),
        })
        _LoggerFactory.add_track_dimensions(_get_logger(), telemetry_values)
        for definition in definitions:
            definition._load_source = _ComponentLoadSource.REGISTERED

        component_funcs = [Component._component_func_from_definition(definition)
                           for definition in definitions]
        if len(definitions) == 1:
            component_funcs = component_funcs[0]
        return component_funcs

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API)
    def load(workspace: Workspace, name: str = None,
             version: str = None, selector: str = None, id: str = None) -> Callable[..., 'Component']:
        """
        Get component function from workspace.

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param name: The name of component
        :type name: str
        :param version: The version
        :type version: str
        :param selector: A string formatted as name:version or name@label, when loading component,
            you can choose one between selector and name, version.
        :type selector: str
        :param id: The component version id of an existing component
        :type id: str

        :return: A function that can be called with parameters to get a :class:`azure.ml.component.Component`
        :rtype: function
        """
        if id is not None:
            definition = CommandComponentDefinition.get_by_id(workspace, id)
        elif name is not None or selector is not None:
            if selector is not None:
                from ._restclients.service_caller import _resolve_parameter_from_selector
                name, version = _resolve_parameter_from_selector(selector)
            definition = CommandComponentDefinition.get(workspace, name, version)
        else:
            raise UserErrorException('Load component failed: One of the name/id/selector must not be empty.')

        definition._load_source = _ComponentLoadSource.REGISTERED

        return Component._component_func_from_definition(definition)

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="Component_from_notebook")
    def _from_notebook(workspace: Workspace, notebook_file: str, source_dir=None) -> Callable[..., 'Component']:
        """Register an anonymous component from a jupyter notebook file and return the registered component func.

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param notebook_file: The jupyter notebook file run in component.
        :type notebook_file: str
        :param source_dir: The source directory of the component.
        :type source_dir: str

        :return: A function that can be called with parameters to get a :class:`azure.ml.component.Component`
        :rtype: function
        """
        from azure.ml.component.dsl._component_from_notebook import gen_component_by_notebook
        if source_dir is None:
            source_dir = Path(notebook_file).parent
            notebook_file = Path(notebook_file).name
        if not notebook_file.endswith('.ipynb'):
            raise UserErrorException("'%s' is not a jupyter notebook file" % notebook_file)
        temp_target_file = '_' + Path(notebook_file).with_suffix('.py').name
        temp_target_path = Path(source_dir) / Path(temp_target_file)
        conda_file = temp_target_path.parent / 'conda.yaml'

        from azure.ml.component.dsl._utils import _temporarily_remove_file, _change_working_dir
        with _temporarily_remove_file(temp_target_path), _temporarily_remove_file(conda_file):
            generator = gen_component_by_notebook(
                notebook_file,
                working_dir=source_dir,
                target_file=temp_target_file,
                force=True)

            with _change_working_dir(source_dir):
                from runpy import run_path
                notebook_component = run_path(temp_target_file)
                notebook_func = notebook_component[generator.func_name]
                return Component._from_func_imp(workspace=workspace, func=notebook_func,
                                                force_reload=False, load_source=_ComponentLoadSource.FROM_NOTEBOOK)

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="Component_from_func")
    def _from_func(workspace: Workspace, func: types.FunctionType, force_reload=True) -> Callable[..., 'Component']:
        """Register an anonymous component from a wrapped python function and return the registered component func.

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param func: A wrapped function to be loaded or a ComponentExecutor instance.
        :type func: types.FunctionType
        :param force_reload: Whether reload the function to make sure the code is the latest.
        :type force_reload: bool

        :return: A function that can be called with parameters to get a :class:`azure.ml.component.Component`
        :rtype: function
        """
        return Component._from_func_imp(workspace=workspace, func=func,
                                        force_reload=force_reload, load_source=_ComponentLoadSource.FROM_FUNC)

    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="Component_export_yaml")
    def _export_yaml(self, directory=None):
        """
        Export component to yaml files.

        This is an experimental function, will be changed anytime.

        :param directory: The target directory path. Default current working directory
            path will be used if not provided.
        :type directory: str
        :return: The directory path
        :rtype: str
        """
        pass

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API)
    def from_yaml(workspace: Workspace, yaml_file: str) -> Callable[..., 'Component']:
        """
        Register an anonymous component from yaml file to workspace and return the registered component func.

        Assumes source code is in the same directory with yaml file. Then return the registered component func.

        For example:

        .. code-block:: python

            # Suppose we have a workspace as 'ws'
            # Register and get an anonymous component from yaml file
            component = from_yaml(workspace, "custom_component/component_spec.yaml")
            # Register and get an anonymous component from Github url
            component = from_yaml(
                workspace,
                https://github.com/wangchao1230/hello-aml-modules/blob/wanhan/add_component_sample/sample_components_do_not_delete/build_artifact_demo_0.0.1/component_spec.yaml")

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param yaml_file: The component spec file. The spec file could be located in local or Github.
        :type yaml_file: str

        :return: A function that can be called with parameters to get a :class:`azure.ml.component.Component`
        :rtype: function
        """
        return Component._from_module_spec(workspace=workspace, yaml_file=yaml_file,
                                           load_source=_ComponentLoadSource.FROM_YAML)

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API, activity_name="Component_register")
    def _register(workspace: Workspace, yaml_file: str, amlignore_file: str = None,
                  set_as_default: bool = False, version: str = None) -> \
            Callable[..., 'Component']:
        """
        Register an component from yaml file to workspace.

        Assumes source code is in the same directory with yaml file. Then return the registered component func.

        For example:

        .. code-block:: python

            # Suppose we have a workspace as 'ws'
            # Register and get an anonymous component from yaml file
            component = from_yaml(workspace, "custom_component/component_spec.yaml")
            # Register and get an anonymous component from Github url
            component = from_yaml(
                workspace,
                https://github.com/wangchao1230/hello-aml-modules/blob/wanhan/add_component_sample/sample_components_do_not_delete/build_artifact_demo_0.0.1/component_spec.yaml")

        :param workspace: The workspace object this component will belong to.
        :type workspace: azureml.core.Workspace
        :param yaml_file: The component spec file. The spec file could be located in local or Github.
        :type yaml_file: str
        :param amlignore_file: The .amlignore or .gitignore file path used to exclude files/directories in the snapshot
        :type amlignore_file: str
        :param set_as_default: By default false, default version of the component will not be updated
            when registering a new version of component. Specify this flag to set the new version as the component's
            default version.
        :type set_as_default: bool
        :param version: If specified, registered component will use specified value as version
            instead of the version in the yaml.
        :type version: str

        :return: A function that can be called with parameters to get a :class:`azure.ml.component.Component`
        :rtype: function
        """
        if version is not None:
            if not isinstance(version, str):
                raise UserErrorException('Only string type of supported for param version.')
            elif version == "":
                # Hint user when accidentally set empty string to set_version
                raise UserErrorException('Param version does not allow empty value.')
        definition = CommandComponentDefinition.register(
            workspace, spec_file=yaml_file,
            package_zip=None,
            anonymous_registration=False,
            set_as_default=set_as_default,
            amlignore_file=amlignore_file,
            version=version
        )
        definition._load_source = _ComponentLoadSource.FROM_YAML

        return Component._component_func_from_definition(definition)
    # endregion
