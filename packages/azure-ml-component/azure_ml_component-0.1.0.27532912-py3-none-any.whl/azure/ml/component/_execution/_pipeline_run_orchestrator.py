# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import copy
from datetime import datetime
import concurrent.futures

from .._util._utils import _get_short_path_name, trans_to_valid_file_name
from ..component import Output, Input
from .._util._loggerfactory import _LoggerFactory, track
from ._component_run_helper import ComponentRunHelper, update_pipeline_in_visualizer
from ._component_snapshot import snapshot_cache
from ._constants import NODE_ID, STEP_PREFIX, WORKING_DIR, RUN_ID, \
    STEP_STATUS as PIPELINE_STATUS, RUN_STATUS, PARENT_NODE_ID, EXECUTION_LOGFILE, \
    RUNNING, COMPLETED, FAILED


datetime_format = '%Y-%m-%d %H:%M:%S'
submit_log_format = '[{}] Submitting {} runs, first five are: {} \n'
complete_log_format = '[{}] Completing processing {}\n'
failed_log_format = '[{}] Execution of experiment failed, update experiment status and cancel running nodes.'

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


@track(_get_logger)
def _orchestrate_pipeline_run(pipeline, working_dir, component_node_to_graph_node_mapping, datasource, tracker=None,
                              visualizer=None, pipeline_parameters=None, show_output=False,
                              continue_on_step_failure=None, max_workers=None, use_docker=True,
                              python_interpreter_path=None, raise_on_error=True):
    """
    Orchestrate pipeline run

    Orchestrating pipeline run to make steps executing in parallel. Firstly will submit no dependency
    steps to start pipeline run, using threadpool to parallel execute steps. When previous steps completed,
    will push no dependency steps to threadpool, until all steps completed.

    :param pipeline: Orchestrated pipeline
    :type pipeline: azure.ml.component.Pipeline
    :param working_dir: pipline run data and snapshot store path
    :type working_dir: str
    :param component_node_to_graph_node_mapping: mapping of component node to graph node
    :type component_node_to_graph_node_mapping: dict
    :param datasource: Input datasets of pipeline
    :type datasource: list
    :param tracker: Used for tracking run history.
    :type tracker: RunHistoryTracker
    :param visualizer: To show pipeline graph in notebook
    :type visualizer: azure.ml.component._widgets._visualize
    :param pipeline_parameters: An optional dictionary of pipeline parameter
    :type pipeline_parameters: dict({str:str})
    :param show_output: Indicates whether to show the pipeline run status on sys.stdout.
    :type show_output: bool
    :param continue_on_step_failure: Indicates whether to continue pipeline execution if a step fails.
        If True, only steps that have no dependency on the output of the failed step will continue execution.
    :type continue_on_step_failure: bool
    :param max_workers:  The maximum number of threads that can be used to execute pipeline steps.
        If max_workers is None, it will default to the number of processors on the machine.
    :type max_workers: int
    :param use_docker: If use_docker=True, will pull image from azure and run component in container.
                           If use_docker=False, will directly run component script.
    :type use_docker: bool
    :param python_interpreter_path: When use_docker=False and python_interpreter_path not None, will use
                                    python_interpreter_path to run steps.
    :type python_interpreter_path: str
    :param raise_on_error: Indicates whether to raise an error when the Run is in a failed state
    :type raise_on_error: bool

    :return: whether pipeline run successful finished
    :rtype: bool
    """
    # prepare for node run
    node_list, component_to_node_mapping = pipeline._expand_pipeline_nodes('', component_node_to_graph_node_mapping)
    node_dict = {node._instance_id: node for node in node_list}
    node_output_dict, begin_exec_node = _prepare_pipeline_run(node_dict)
    executed_nodes = []
    cur_pipeline_run_success = True
    pipeline_status = {}
    execution_log_path = os.path.join(working_dir, EXECUTION_LOGFILE)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    try:
        # start downloading node input datset
        ComponentRunHelper.download_datasets(
            datasource, pipeline.workspace, working_dir, pipeline_parameters)

        # start getting beginning node images
        if use_docker or not python_interpreter_path:
            for node in [node_dict[node_id] for node_id in begin_exec_node]:
                ComponentRunHelper.prepare_component_env(node, working_dir, use_docker)

        # start running node
        if visualizer:
            pipeline_status = update_pipeline_status('Running', run_details_url=tracker.get_run_details_url())
            update_pipeline_in_visualizer(visualizer, PARENT_NODE_ID, pipeline_status)

        with open(execution_log_path, 'w') as execution_file:
            # start nodes execution
            futures = _execute_steps(executor, begin_exec_node, tracker, node_dict, working_dir,
                                     pipeline_parameters, component_to_node_mapping, show_output,
                                     visualizer, execution_file, node_output_dict, use_docker,
                                     python_interpreter_path, pipeline_status)

            current_futures = futures.keys()
            while current_futures:
                done_futures, current_futures = concurrent.futures.wait(
                    current_futures, return_when=concurrent.futures.FIRST_COMPLETED)
                # update running node task list
                next_node_list, pipeline_run_success, exception = _handle_done_futures(
                    done_futures, futures, execution_file, executed_nodes, node_output_dict)
                cur_pipeline_run_success = cur_pipeline_run_success and pipeline_run_success
                if raise_on_error and not pipeline_run_success:
                    raise exception
                if not pipeline_run_success and not continue_on_step_failure:
                    concurrent.futures.wait(current_futures, return_when=concurrent.futures.ALL_COMPLETED)
                    break
                else:
                    next_nodes = _find_next_run_node(next_node_list, executed_nodes, node_dict)
                    next_futures = _execute_steps(executor, next_nodes, tracker, node_dict, working_dir,
                                                  pipeline_parameters, component_to_node_mapping, show_output,
                                                  visualizer, execution_file, node_output_dict, use_docker,
                                                  python_interpreter_path, pipeline_status)
                    current_futures.update(next_futures.keys())
                    futures.update(next_futures)
    except Exception as e:
        cur_pipeline_run_success = False
        if raise_on_error:
            raise e
    finally:
        # update pipeline run status
        executor.submit(tracker.update_run_result_status, cur_pipeline_run_success)
        # upload pipeline log and get log url
        update_log_future = executor.submit(tracker.upload_run_log, EXECUTION_LOGFILE, execution_log_path)
        if visualizer:
            result_status = COMPLETED if cur_pipeline_run_success else FAILED
            update_pipeline_in_visualizer(
                visualizer,
                PARENT_NODE_ID,
                update_pipeline_status(result_status, status=pipeline_status),
                update_log_future.result()
            )
        # Remove long time no used snapshots in cache
        snapshot_cache.clean_up_snapshot_cache()
        # Executor.shutdown will wait for threads in it completed.
        executor.shutdown()
    return cur_pipeline_run_success


def get_node_input_dset(input_dset):
    if isinstance(input_dset, Input):
        return get_node_input_dset(input_dset._dset)
    else:
        return input_dset


def _prepare_pipeline_run(node_dict):
    node_output_dict = {}
    begin_exec_node = []
    for node in node_dict.values():
        pre_input_list = []
        for input in node.inputs.values():
            dset = get_node_input_dset(input._dset)
            if isinstance(dset, Output):
                pre_input_list.append(dset)
        if len(pre_input_list) == 0:
            begin_exec_node.append(node._instance_id)
        for input in pre_input_list:
            if input._owner._id not in node_output_dict.keys():
                node_output_dict[input._owner._id] = []
            node_output_dict[input._owner._id].append(node._instance_id)

    return node_output_dict, begin_exec_node


def _execute_steps(executor, steps, tracker, node_dict, working_dir, pipeline_parameters,
                   component_to_node_mapping, show_output, visualizer, execution_file,
                   node_output_dict, use_docker, python_interpreter_path, pipeline_status):
    futures = {}
    next_node_list = set()
    for node in steps:
        child_tracker = tracker.get_child_tracker(name=node_dict[node].name, path=EXECUTION_LOGFILE)
        submit_future = executor.submit(
            exec_node, node_dict[node], child_tracker, working_dir, pipeline_parameters,
            component_to_node_mapping, show_output, visualizer, node, use_docker,
            python_interpreter_path, pipeline_status)
        futures[submit_future] = {
            NODE_ID: node,
            RUN_ID: child_tracker.get_run_id()
        }
        if node in node_output_dict:
            next_node_list.update(node_output_dict[node])
    if len(steps) > 0:
        run_id_list = [value[RUN_ID] or value[NODE_ID] for value in futures.values()]
        execution_file.write(
            submit_log_format.format(datetime.now().strftime(datetime_format),
                                     len(steps),
                                     ','.join(run_id_list[0:5])))
    if use_docker or not python_interpreter_path:
        # prepare for getting next nodes image
        for node in [node_dict[node_id] for node_id in next_node_list]:
            ComponentRunHelper.prepare_component_env(node, working_dir, use_docker)
    return futures


def _find_next_run_node(next_node_list, executed_nodes, node_dict):
    next_nodes = set()
    for node_id in next_node_list:
        node = node_dict[node_id]
        node_inputs = [get_node_input_dset(input) for input in node.inputs.values()]
        if all([input._owner._id in executed_nodes
                for input in node_inputs if isinstance(input, Output)]):
            next_nodes.add(node._instance_id)
    return next_nodes


def _handle_done_futures(done_futures, futures, execution_file, executed_nodes, node_output_dict):
    # check and log step run status
    # if step completed get next executing node list
    next_node_list = set()
    pipeline_run_success = True
    exception = None
    for future in done_futures:
        if future.result()[0] != COMPLETED:
            pipeline_run_success = False
            execution_file.write(failed_log_format.format(datetime.now().strftime(datetime_format)))
            if not exception:
                exception = future.result()[1]
            continue
        node_id = futures[future][NODE_ID]
        execution_file.write(
            complete_log_format.format(
                datetime.now().strftime(datetime_format),
                'run id {}'.format(futures[future][RUN_ID])
                if futures[future][RUN_ID] else 'node id {}'.format(node_id)))
        executed_nodes.append(node_id)
        if node_id in node_output_dict:
            next_node_list.update(node_output_dict[node_id])
    return next_node_list, pipeline_run_success, exception


def update_pipeline_status(pipeline_status, status=None, run_details_url=None):
    if not status or PARENT_NODE_ID not in status:
        status = {PARENT_NODE_ID: copy.deepcopy(PIPELINE_STATUS)}
    if run_details_url:
        status[PARENT_NODE_ID]['runDetailsUrl'] = run_details_url

    status[PARENT_NODE_ID]['runStatus'] = RUN_STATUS[pipeline_status]

    if pipeline_status == RUNNING and not status[PARENT_NODE_ID]['startTime']:
        status[PARENT_NODE_ID]['startTime'] = datetime.now().isoformat()
    elif pipeline_status == COMPLETED or pipeline_status == FAILED:
        status[PARENT_NODE_ID]['endTime'] = datetime.now().isoformat()
    return status


def trans_node_name(node_name, node_id=None):
    node_name = trans_to_valid_file_name(node_name)
    if node_id:
        return '%s_%s' % (node_name.strip(), node_id)
    else:
        return node_name.strip()


def exec_node(node, tracker, working_dir, pipeline_parameters, component_to_node_mapping,
              show_output, visualizer, node_id, use_docker, python_interpreter_path, pipeline_status):
    try:
        node_run_filename = trans_node_name(node.name, tracker.get_run_id() or node_id)
        node_working_dir = _get_short_path_name(
            os.path.join(working_dir, component_to_node_mapping[node._instance_id][STEP_PREFIX], node_run_filename),
            create_dir=True)
        component_run_helper = ComponentRunHelper(
            component=node,
            working_dir=node_working_dir,
            tracker=tracker,
            use_docker=use_docker,
            node_id=component_to_node_mapping[node._instance_id][NODE_ID],
            visualizer=visualizer,
            show_output=show_output,
            component_to_node_mapping=component_to_node_mapping,
            pipeline_parameters=pipeline_parameters)
        status = component_run_helper.component_run(
            python_interpreter_path, raise_on_error=True, pipeline_status=pipeline_status)
        component_to_node_mapping[node._instance_id][WORKING_DIR] = node_working_dir
    except Exception as ex:
        return FAILED, ex
    return status, None
