# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import json
from uuid import UUID

from azureml._restclient.snapshots_client import SnapshotsClient as BaseSnapshotsClient
from azureml._restclient.constants import SNAPSHOT_MAX_FILES, SNAPSHOT_BATCH_SIZE
from azureml._project.ignore_file import get_project_ignore_file
from azureml._base_sdk_common.merkle_tree import DirTreeJsonEncoder, create_merkletree, DirTreeNode
from azureml._base_sdk_common.merkle_tree_differ import compute_diff
from azureml.exceptions import SnapshotException
from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._base_sdk_common.utils import create_session_with_retry
from azureml._base_sdk_common.common import get_http_exception_response_string
from azureml._base_sdk_common.snapshot_dto import SnapshotDto
from ._snapshot_cache import SnapshotCache
from ._utils import default_content_hash_calculator


class SnapshotsClient(BaseSnapshotsClient):
    """
    Snapshot client class, extended from azureml._restclient.snapshots_client.SnapshotsClient.
    Add snapshot cache per component.

    :param service_context:
    :type service_context: azureml._restclient.service_context.ServiceContext
    """
    def __init__(self, *args, **kwargs):
        super(SnapshotsClient, self).__init__(*args, **kwargs)
        self._cache = SnapshotCache(self._service_context)

    def create_snapshot(self, file_or_folder_path, retry_on_failure=True, raise_on_validation_failure=True):
        """Create snapshot on file_or_folder_path, support cache and incrementally update based on latest snapshot
        """
        auth_headers = self.auth.get_authentication_header()

        ignore_file = get_project_ignore_file(file_or_folder_path)
        exclude_function = ignore_file.is_file_excluded

        self._validate_snapshot_size(file_or_folder_path, exclude_function, raise_on_validation_failure)

        # Get the previous snapshot for this project
        parent_root, parent_snapshot_id = self._cache.get_latest_snapshot_by_path(file_or_folder_path)

        # Compute the dir tree for the current working set
        curr_root = create_merkletree(file_or_folder_path, exclude_function)

        # Compute the diff between the two dirTrees
        entries = compute_diff(parent_root, curr_root)

        # If there are no changes, just return the previous snapshot_id
        if not len(entries):
            return parent_snapshot_id

        # Calculate new snapshot id
        snapshot_content_hash = default_content_hash_calculator(file_or_folder_path)
        snapshot_id = str(UUID(snapshot_content_hash))

        # Check whether the snapshot with new id already exists
        snapshot_dto = self.get_snapshot_metadata_by_id(snapshot_id)
        if snapshot_dto is None:
            entries_to_send = [entry for entry in entries if (
                entry.operation_type == 'added' or entry.operation_type == 'modified') and entry.is_file]
            if len(entries_to_send) > SNAPSHOT_MAX_FILES and not os.environ.get("AML_SNAPSHOT_NO_FILE_LIMIT"):
                error_message = "====================================================================\n" \
                                "\n" \
                                "While attempting to take snapshot of {}\n" \
                                "Your project exceeds the file limit of {}.\n" \
                                "\n" \
                                "====================================================================\n" \
                                "\n".format(file_or_folder_path, SNAPSHOT_MAX_FILES)
                if raise_on_validation_failure:
                    raise SnapshotException(error_message)
                else:
                    print(error_message)

            custom_headers = {
                "dirTreeRootFile": "true"
            }

            dir_tree_file_contents = json.dumps(curr_root, cls=DirTreeJsonEncoder)

            # Git metadata
            snapshot_properties = global_tracking_info_registry.gather_all(file_or_folder_path)

            with create_session_with_retry() as session:

                # There is an OS limit on how many files can be open at once, so we \
                # must batch the snapshot to not exceed the limit.
                # We take multiple snapshots, each building on each other, and return the final snapshot.
                new_snapshot_id = None
                # We always need to do at least one pass,
                # for the case where the only change is deleted files in dirTreeRootFile
                first_pass = True
                while len(entries_to_send) or first_pass:
                    first_pass = False
                    files_to_send = []
                    files_to_close = []
                    if new_snapshot_id:
                        # If updated files count >= 2000, we will get a new snapshot id
                        parent_snapshot_id = new_snapshot_id
                    new_snapshot_id = snapshot_id
                    try:
                        # Add entries until we hit batch limit
                        while len(files_to_send) < SNAPSHOT_BATCH_SIZE and len(entries_to_send):
                            entry = entries_to_send.pop()
                            path_env = (os.path.join(file_or_folder_path, entry.node_path)
                                        if os.path.isdir(file_or_folder_path)
                                        else entry.node_path)
                            file_obj = open(path_env, "rb")
                            files_to_send.append(("files", (entry.node_path, file_obj)))
                            files_to_close.append(file_obj)

                        # directory_tree needs to be added to all snapshot requests
                        files_to_send.append(
                            ("files", ("dirTreeRootFile", dir_tree_file_contents, "application/json", custom_headers)))
                        files_to_send.append(("properties", (None, json.dumps(snapshot_properties))))

                        url = self._service_context._get_project_content_url() + "/content/v1.0" + \
                            self._service_context._get_workspace_scope() + "/snapshots/" + \
                            new_snapshot_id + "?parentSnapshotId=" + parent_snapshot_id

                        response = self._execute_with_base_arguments(
                            session.post, url, files=files_to_send, headers=auth_headers)
                        if response.status_code >= 400:
                            if retry_on_failure:
                                # The cache may have been corrupted, so clear it and try again.
                                self._cache.remove_latest()
                                return self.create_snapshot(file_or_folder_path, retry_on_failure=False)
                            else:
                                raise SnapshotException(get_http_exception_response_string(response))
                    finally:
                        for f in files_to_close:
                            f.close()

            snapshot_dto = SnapshotDto(dir_tree_file_contents, new_snapshot_id)
        else:
            new_snapshot_id = snapshot_id

        # Update the cache
        self._cache.update_cache(snapshot_dto, file_or_folder_path)
        return new_snapshot_id

    def get_snapshot_metadata_by_id(self, snapshot_id):
        """
        200 indicates the snapshot with this id exists, 404 indicates not exists
        If other status codes returned, by default we will retry 3 times until we get 200 or 404
        """
        auth_headers = self.auth.get_authentication_header()
        url = self._service_context._get_project_content_url() + "/content/v1.0" + \
            self._service_context._get_workspace_scope() + "/snapshots/" + \
            snapshot_id + "/metadata"
        with create_session_with_retry() as session:
            response = self._execute_with_base_arguments(
                session.get, url, headers=auth_headers)
            if response.status_code == 200:
                response_data = response.content.decode('utf-8')
                snapshot_dict = json.loads(response_data)
                root_dict = snapshot_dict['root']
                snapshot_id = snapshot_dict['id']
                node = DirTreeNode()
                node.load_object_from_dict(root_dict)
                root = json.dumps(node, cls=DirTreeJsonEncoder)
                return SnapshotDto(root, snapshot_id)
            elif response.status_code == 404:
                return None
            else:
                raise SnapshotException(get_http_exception_response_string(response))
