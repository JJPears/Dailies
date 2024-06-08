"""
This module provides an error handler for handling common exceptions in a Flask application.
"""

from flask import jsonify
from werkzeug.exceptions import NotFound, BadRequest


def handle_not_found_error(error):
    """
    Handle a not found error.

    :param error: The exception that was raised.
    :return: A JSON object with an error message and a 404 HTTP status code.
    """
    response = jsonify({"error": str(error.description)})
    response.status_code = NotFound.code
    return response


def handle_bad_request_error(error):
    """
    Handle a bad request error.

    :param error: The exception that was raised.
    :return: A JSON object with an error message and a 400 HTTP status code.
    """
    response = jsonify({"error": str(error.description)})
    response.status_code = BadRequest.code
    return response


ERROR_HANDLERS = {
    NotFound: handle_not_found_error,
    BadRequest: handle_bad_request_error,
}
