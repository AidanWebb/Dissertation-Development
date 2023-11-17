from flask import request

from classes.errors import BadRequest

api_version = '0.1'


def before_request():
    """
    Invoke all functions here that MUST be called prior to route invocation.
    """
    _check_json_content_type()


def _check_json_content_type():
    """
    If the request is a POST request,
    the Content-Type header must be 'application/json'.
    """
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type') or None
        if content_type and ('application/json' not in [x.strip() for x in content_type.split(';')]):
            raise BadRequest("Content-Type of 'application/json' is required for POST requests.")


def apply_content_version(response):
    """
    Applies a header of Content-Version: 1.0
    No API versions have been formally defined yet.
    """
    response.headers['Content-Version'] = request_version()
    return response


def request_version():
    """
    Gets the version of the incoming request.
    :return: Request version.
    """
    version = request.headers.get('Accept-Version')
    if version in ['0.1']:
        return version
    else:
        return api_version