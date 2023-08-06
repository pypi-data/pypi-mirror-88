# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from threading import Thread, Lock
from http.server import BaseHTTPRequestHandler, HTTPServer

from ._validation import _get_url_content

FORWARD_ROUTE = '/forward'


class BaseVisualizeRequestHandler(BaseHTTPRequestHandler):
    """Handle the requests that arrive at the server."""

    def end_headers(self):
        # To handle CORS issue
        self.send_header('Access-Control-Allow-Credentials', True)
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def _set_response(self):
        self.send_response(200)
        self.end_headers()


class ForwardRequestHandler(BaseVisualizeRequestHandler):
    """Handle the forward requests that arrive at the server."""

    def do_POST(self):
        """
        Handle POST request.
        If url in request content is a web link, will response content of url request.
        If url is a local file path, will response file content.
        """
        if self.path == FORWARD_ROUTE:
            # Get forward url from request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                request_json = json.loads(post_data.decode('utf-8'))
            except json.decoder.JSONDecodeError:
                self.send_error(400, 'Request content is not json format')
                return
            if 'url' not in request_json:
                self.send_error(400, 'Can not get url from request content')
                return

            # Get forward request content
            content = _get_url_content(request_json['url'])
            self._set_response()
            content = json.dumps({'result': content})
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, '{} not found!'.format(self.path))

    def do_OPTIONS(self):
        """
        Handle OPTIONS request
        Handling cross-domain requests and set Access-Control-Allow in response header.
        """
        # In CORS, a preflight request is sent with the OPTIONS method so that the server can respond
        # if it is acceptable to send the request. It sets some Access-Control-Allow headers in response
        # and no need to write content in response.
        self._set_response()

    def log_message(self, format, *args):
        # Overwrite BaseHTTPRequestHandler.log_message to avoid logging handler info.
        pass


class VisualizeServer:
    """Handle requests in a separate thread."""

    _instance_lock = Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton creation visualize server
        """
        # VisualizeServer is used to handle CORS when getting run logs in jupyter. To handle requests from all
        # visualizer in process, life cycle of VisualizeServer is the entire process. And creating VisualizeServer
        # with singleton to avoid creating services repeatedly.
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, request_handler):
        """
        Init and start visualize server in thread

        :param request_handler: RequestHandlerClass
        :type request_handler: http.server.BaseHTTPRequestHandler
        """
        # For first initialization, VisualizeServer._instance doesn't has attribute server.
        # To avoid create multi servers, will check attribute server exist.
        if not hasattr(self, 'server'):
            # OS will pick up an availabe port if not bind to specific port or port 0.
            self.server = HTTPServer(('localhost', 0), request_handler)
            # Start server in thread.
            self.server_thread = Thread(target=self.server.serve_forever)
            self.server_thread.setDaemon(True)
            self.server_thread.start()

    def get_server_address(self):
        if hasattr(self, 'server'):
            address = self.server.server_address
            return 'http://{}:{}'.format(address[0], address[1])

    def server_avaliable(self):
        # Check server is avaliable.
        return self.server_thread.isAlive()
