# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
SLEEP_INTERVAL = 5
MODULE_PROPERTY_NAME = 'azureml.moduleid'
MOCK_PARALLEL_DRIVER = '_mock_parallel_driver.py'

# File/folder name
OUTPUT_DIR_NAME = 'outputs'
IMAGE_DIR_NAME = 'image_logs'
CONDA_DIR_NAME = 'conda_logs'
SCRIPTE_DIR_NAME = 'scripts'
EXECUTION_LOGFILE = 'excutionlogs.txt'

# Input/output/script path in container
CONTAINER_INPUT_PATH = '/mnt/input'
CONTAINER_OUTPUT_PATH = '/mnt/{}'.format(OUTPUT_DIR_NAME)
CONTAINER_MOUNT_SCRIPTS_PATH = '/mnt/scripts'

# Prefix of component run log
RUN_PREPARE_LOG = 'Run prepare stage'
RUN_EXEC_LOG = 'Run execute stage'
RUN_RELEASE_LOG = 'Run release stage'
USER_ERROR_MSG = 'Executing script failed with a non-zero exit code; see the %s for details.'

# Component run status
PREPAREING = 'Preparing'
RUNNING = 'Running'
COMPLETED = 'Completed'
FAILED = 'Failed'

RUN_STATUS = {
    'NotStarted': '0',
    'Preparing': '3',
    'Running': '5',
    'Completed': '8',
    'Failed': '9'
}
STATUS_CODE = {
    'NotStarted': '0',
    'Preparing': '2',
    'Running': '3',
    'Failed': '4',
    'Completed': '5',
}

# Keyword of visualizer
PARENT_NODE_ID = '@parent'
NODE_LOG_KEY = '70_driver_log.txt'
PARENT_LOG_KEY = 'logs/azureml/executionlogs.txt'

# Step status info of visualizer
STEP_STATUS = {
    'runStatus': None,
    'startTime': None,
    'endTime': None,
    'status': None,
    'statusCode': None,
    'statusDetail': None,
    'runDetailsUrl': None
}

# Pipeline run keyword
NODE_ID = 'node_id'
STEP_PREFIX = 'prefix'
WORKING_DIR = 'working_dir'
RUN_ID = 'run_id'
