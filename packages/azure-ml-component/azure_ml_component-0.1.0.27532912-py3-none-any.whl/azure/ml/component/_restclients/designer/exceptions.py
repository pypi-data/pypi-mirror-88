# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from functools import wraps

from .models import ErrorResponseException
from html import unescape


def _is_user_error(http_status_code):
    return 400 <= http_status_code < 500


class ServiceError(Exception):
    """General error when interacting with the http server."""

    def __init__(self, message):
        super().__init__(message)


class ComponentServiceError(ServiceError):
    """General error when interacting with the module service."""

    def __init__(self, error_code=None, message=None, http_status_code=None, http_reason=None):
        super().__init__(message)
        self._error_code = error_code
        self._message = message
        self._http_status_code = http_status_code
        self._http_reason = http_reason

    @classmethod
    def from_response_exception(cls, e: ErrorResponseException):
        res = e.response
        error_code = None
        message = None
        http_status_code = res.status_code
        http_reason = res.reason

        json = res.json()
        if json:
            dct = json.get('error', None)
            if dct is not None:
                error_code = dct.get('code')
                # Server encodes the error message using XML,
                # e.g `\r\n` will be encoded as `&#xD;&#xA;`.
                # We need to unescape them here.
                message = unescape(dct.get('message'))
        else:
            message = res.text

        if not _is_user_error(http_status_code):
            # detailed error message if request id is provided
            text = '{0} {1}: {2}'.format(http_status_code, http_reason, message)
            request_id = e.response.headers.get('x-ms-client-request-id')
            if request_id:
                message = '{text} (RequestId: {request_id})'.format(text=text, request_id=request_id)

        message = '{}: {}'.format(error_code, message)

        # This is for catching conflict error.
        constructor = cls if error_code != 'AzureMLModuleVersionAlreadyExist' else ComponentAlreadyExistsError
        return constructor(
            error_code=error_code,
            message=message,
            http_status_code=http_status_code,
            http_reason=http_reason,
        )

    @property
    def error_code(self):
        return self._error_code

    @property
    def message(self):
        return self._message

    @property
    def http_status_code(self):
        return self._http_status_code

    @property
    def http_reason(self):
        """The reason code returned from http

           e.g. 'Not Found', 'Internal Service Error'.
        """
        return self._http_reason


class ComponentAlreadyExistsError(ComponentServiceError):
    pass


def error_wrapper(exception: ErrorResponseException):
    """Try to wrap ErrorResponseException to ComponentServiceError, return original exception if failed."""
    try:
        return ComponentServiceError.from_response_exception(exception)
    except BaseException:
        return exception


def try_to_find_request_id_from_params(args, kwargs):
    """Try to find request id from positional arguments and key value arguments

    Note: This function only try to find request id from auto-generated service call methods.
    eg: ComponentOperations.get_component( ..., custom_headers=None, ...)
    :param args: positional arguments
    :param kwargs: key value arguments
    :return: Request id or None if request id not found
    """
    request_id_key = 'x-ms-client-request-id'
    # find in positional args
    for arg in args:
        if isinstance(arg, dict):
            if request_id_key in arg.keys():
                return arg.get(request_id_key)
    # find in kwargs, we assume request id can only be found in value of "custom_headers"
    if 'custom_headers' in kwargs.keys():
        return kwargs['custom_headers'].get(request_id_key, None)
    return None


def wrap_exception(exception=ErrorResponseException):
    """Wrap exception to ComponentServiceError for function f."""

    def wrap_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exception as e:
                wrapped = error_wrapper(e)
                raise e if wrapped is e else wrapped
            except BaseException as e:
                error_msg = "Got error {0}: '{1}' while calling {2}".format(e.__class__.__name__, e, f.__name__)
                # add request id if possible
                request_id = try_to_find_request_id_from_params(args, kwargs)
                if request_id:
                    error_msg = '{} (RequestId: {})'.format(error_msg, request_id)
                raise ServiceError(error_msg) from e

        return wrapper

    return wrap_decorator


def wrap_methods_with_decorator(obj, decorator=wrap_exception):
    """Wrap all methods of obj with decorator"""
    for attribute_name in dir(obj):
        if not attribute_name.startswith('__'):
            attr = getattr(obj, attribute_name)
            if callable(attr):
                setattr(obj, attribute_name, decorator()(attr))
