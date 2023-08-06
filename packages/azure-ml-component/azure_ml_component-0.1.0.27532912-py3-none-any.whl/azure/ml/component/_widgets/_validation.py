# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from traitlets import Unicode, Int
import os

from ipywidgets import DOMWidget, register
from azureml.core import Workspace, Experiment


def _get_pipeline_run_from_content(content):
    run_id = content.get("runId")
    subscription_id = content.get("subscriptionId")
    resource_group = content.get("resourceGroup")
    workspace_name = content.get("workspaceName")
    experiment_name = content.get("experimentName")

    workspace = Workspace.get(subscription_id=subscription_id,
                              resource_group=resource_group,
                              name=workspace_name)
    experiment = Experiment(workspace, experiment_name)

    from azure.ml.component import Run
    return Run(experiment, run_id)


@register
class ValidateView(DOMWidget):
    """ A widget for the pipeline validate visualization.

    Especially, the widget accept message to update running status.
    And return the latest status into view.
    """

    _view_name = Unicode('ValidateView').tag(sync=True)
    _view_module = Unicode('validate_widget').tag(sync=True)
    _view_module_version = Unicode('0.0.0').tag(sync=True)

    graph_json = Unicode().tag(sync=True)
    env_json = Unicode().tag(sync=True)
    lib_url = Unicode().tag(sync=True)
    container_id = Unicode().tag(sync=True)
    visualize_id = Unicode().tag(sync=True)
    is_prod = Int().tag(sync=True)

    def __init__(self, **kwargs):
        """Create a ValidateView widget."""
        super(DOMWidget, self).__init__(**kwargs)
        self.graph_json = kwargs.get("graph_json")
        self.env_json = kwargs.get("env_json")
        self.lib_url = kwargs.get("lib_url")
        self.container_id = kwargs.get("container_id")
        self.visualize_id = kwargs.get("visualize_id")
        self.is_prod = kwargs.get("is_prod")

        def handle_msg(instance, message, params):
            if message.get("message") == "log_query:request":
                self.handle_log_query_request(message.get("body"))
            if message.get("message") == "fetch_profiling:request":
                self.handle_fetch_profiling_request(message.get("body"))

        self.on_msg(handle_msg)

    def handle_log_query_request(self, body):
        uid = body.get("uid")
        content = body.get("content")
        text = _get_url_content(content.get("url"))
        self.send_message("log_query:response", {
            "uid": uid,
            "result": text
        })

    def handle_fetch_profiling_request(self, body):
        uid = body.get("uid")
        content = body.get("content")

        run = _get_pipeline_run_from_content(content)
        profile_data = run._get_profile_data_dict()

        self.send_message("fetch_profiling:response", {
            "uid": uid,
            "profiling": profile_data
        })

    def send_message(self, message: str, content: dict):
        self.send({
            "message": message,
            "body": content
        })


def _get_url_content(url):
    """
    Get url content
    If url in a web link, will response content of url request.
    If url is a local file path, will response file content.
    """
    import requests
    try:
        content = ''
        if url.lstrip().lower().startswith('http'):
            content = requests.get(url).text
        elif os.path.exists(url):
            with open(url, 'r') as f:
                content = f.read()
        return content
    except requests.exceptions.RequestException as e:
        # Catch request.get exception
        return 'Cannot get content from {}, raise exception: {}'.format(url, str(e))
    except FileNotFoundError:
        # Catch read log file error
        return 'Cannot get content from {}, because it not exist.'.format(url)
