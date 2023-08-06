# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""A decorator which builds a :class:azure.ml.component.Pipeline."""
import logging
from collections import OrderedDict
from functools import wraps
from inspect import Parameter, signature
from typing import Callable, Any, TypeVar

from azure.ml.component._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ..pipeline import Pipeline
from .._pipeline_component_definition_builder import PipelineComponentDefinitionBuilder, _definition_builder_stack, \
    _definition_id_now_build

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


# hint vscode intellisense
_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])


def pipeline(name=None, description=None, default_compute_target=None, default_datastore=None):
    """Build a pipeline which contains all nodes and sub-pipelines defined in this function.

    .. remarks::
        Note that a dsl.pipeline can be used to create pipelines with a complex layered structure.
        The following pseudo-code shows how to create a nested pipeline using this decorator.

        .. code-block:: python

            # A sub-pipeline defined with decorator
            @dsl.pipeline(name='sub pipeline', description='sub-pipeline description')
            def sub_pipeline(pipeline_parameter1, pipeline_parameter2):
                # component1 and component2 will be added into the current sub pipeline
                component1 = component1_func(xxx, xxx)
                component2 = component2_func(xxx, xxx)
                # A decorated pipeline function needs to return outputs.
                # In this case, the sub_pipeline has two outputs: component1's output1 and component2's output1, and
                # let's rename them to 'renamed_output1' and 'renamed_output2'
                return {'renamed_output1': component1.outputs.output1, 'renamed_output2': component2.outputs.output1}

            # Assign values to parameters. "xxx" is the real value of the parameter, it might be a Dataset or other
            # hyperparameters.
            param1 = xxx
            param2 = xxx

            # A parent pipeline defined with the decorator
            @dsl.pipeline(name='pipeline', description='parent pipeline description')
            def parent_pipeline(pipeline_parameter1):
                # component3 and sub_pipeline1 will be added into the current parent pipeline
                component3 = component3_func(xxx, xxx)
                # the sub_pipeline is called in the pipeline decorator, this call will return a pipeline with
                # nodes=[component1, component2] and its outputs=component2.outputs
                sub_pipeline1 = sub_pipeline(pipeline_parameter1=param1, pipeline_parameter2=param2)
                # The outputs of the components in the pipeline are not exposed.

            # E.g.: This call returns a pipeline with nodes=[component1, component2], outputs=component2.outputs.
            sub_pipeline2 = sub_pipeline(pipeline_parameter1=param1, pipeline_parameter2=param2)

            # E.g.: This call returns a pipeline with nodes=[sub_pipeline1, component3], outputs={}.
            pipeline1 = parent_pipeline(pipeline_parameter1=param1)

        Note: Parameters in pipeline decorator functions will be stored as a substitutable part of the pipeline,
        which means you can change them directly in the re-submit or other operations in the future without
        re-construct a new pipeline.
        E.g.: change pipeline_parameter1 of parent_pipeline when submit it.

        .. code-block:: python

            pipeline1.submit(parameters={"pipeline_parameter1": changed_param})

        Besides, If there are nested pipelines decorators, as illustrated below, only the outermost pipeline
        parameters, i.e. outer_parameter in this example, will be transformed to a changeable parameter for this
        pipeline.
        E.g.:

        .. code-block:: python

            @dsl.pipeline(name='nested pipeline', description='nested-pipeline description')
            def outer_pipeline(outer_parameter):
                component1 = component1_func(xxx, xxx)
                @dsl.pipeline(name='inner pipeline', description='inner-pipeline description')
                    def inner_pipeline(inner_parameter):
                        component2 = component2_func(xxx, xxx)

    :param name: the name of the built pipeline
    :type: str
    :param description: the description of the built pipeline
    :type: str
    :param default_compute_target: The compute target of the built pipeline.
        Could be a compute target object or the string name of a compute target in the workspace.
        The priority of the compute target assignment: the component's runsettings > the sub pipeline's default compute
        target > the parent pipeline's default compute target.
        Optionally, if the compute target is not available at pipeline creation time, you may specify a tuple of
        ('compute target name', 'compute target type') to avoid fetching the compute target object (AmlCompute
        type is 'AmlCompute' and RemoteCompute type is 'VirtualMachine').
    :type: default_compute_target: azureml.core.compute.DsvmCompute
                        or azureml.core.compute.AmlCompute
                        or azureml.core.compute.RemoteCompute
                        or azureml.core.compute.HDInsightCompute
                        or str
                        or tuple
    :param default_datastore: The default datastore of pipeline.
    :type default_datastore: str or azureml.core.Datastore
    """
    def pipeline_decorator(func: _TFunc) -> _TFunc:
        parent_def_id = None if len(_definition_id_now_build) == 0 else _definition_id_now_build[-1]
        _definition_builder = PipelineComponentDefinitionBuilder.from_func(
            name, description, default_compute_target, default_datastore, func, parent_def_id)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Pipeline:
            # Default args will be added here.
            provided_positional_args = _validate_args(func, args, kwargs)
            # Convert args to kwargs
            kwargs.update(provided_positional_args)

            @track(_get_logger, activity_type=_PUBLIC_API, activity_name="pipeline_decorator")
            def construct_top_pipeline():
                """
                Construct top pipeline function.

                This function was extracted to ensure log behavior
                    perform only once even if there are sub pipeline inside function.
                """
                top_pipeline = construct_sub_pipeline()
                return top_pipeline

            def construct_sub_pipeline():
                _definition = _definition_builder.build()
                # Print warning before create pipeline instance if is top pipeline.
                if _definition_builder_stack.is_empty() and len(_definition_builder.not_used_parameter_key) > 0:
                    for _p in _definition_builder.not_used_parameter_key:
                        logging.warning(
                            'Parameter \'{}\' was not used in pipeline {}.'.format(_p, _definition.name))
                    _definition_builder.not_used_parameter_key.clear()
                return Pipeline(
                    nodes=list(_definition.components.values()), outputs=_definition._outputs_mapping,
                    workspace=_definition.workspace, name=_definition.name, description=_definition.description,
                    default_compute_target=_definition._default_compute_target.name,
                    default_datastore=_definition._default_datastore,
                    _use_dsl=True, _definition=_definition, _init_params=kwargs)
            return construct_top_pipeline() if _definition_builder_stack.is_empty() else construct_sub_pipeline()

        return wrapper

    return pipeline_decorator


def _validate_args(func, args, kwargs):
    # Positional arguments validate
    all_parameters = [param for _, param in signature(func).parameters.items()]
    empty_parameters = {
        param.name: param for param in all_parameters
        if param.default is Parameter.empty}
    min_num = len(empty_parameters)
    max_num = len(all_parameters)
    if len(args) > max_num:
        raise TypeError('{}() takes {} positional argument but {} were given'.format(
            func.__name__, min_num if min_num == max_num else '{} to {}'.format(
                min_num, max_num), len(args)
        ))

    provided_args = OrderedDict({
        param.name: args[idx] for idx, param in enumerate(all_parameters) if idx < len(args)})
    for _k in kwargs.keys():
        if _k in provided_args.keys():
            raise TypeError('{}()got multiple values for argument \'{}\''.format(
                func.__name__, _k
            ))
        provided_args[_k] = kwargs[_k]

    if len(provided_args) < len(empty_parameters):
        missing_keys = empty_parameters.keys() - provided_args.keys()
        raise TypeError('{}() missing {} required positional argument(s): {}'.format(
            func.__name__, len(missing_keys), missing_keys))
    return provided_args
