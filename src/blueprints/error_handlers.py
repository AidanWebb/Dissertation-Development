from flask import Blueprint, jsonify
from classes.errors import OKException, HTTPException

error_handlers = Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(OKException)
def OKExceptionHandler(e):
    """
    Catches OKExceptions and returns a response with the correct status code.
    :param e: OKException
    :return: HTTP response containing status code of exception.
    """
    return jsonify({
        "status" : e.status
    })


@error_handlers.app_errorhandler(HTTPException)
def http_exception_handler(e):
    """
    Catches HTTP Exceptions and deals with the error_handlers appropriately.
    :param e: HTTP Exception
    :return: HTTP response describing nature of exception.
    """
    error_dict = {"error": e.error}
    if e.description is not None:
        error_dict["error_description"]= e.description
    response = jsonify(error_dict)
    response.status_code = e.http_status
    return response