'''
This module defines the error handlers.
'''
from flask import jsonify


def handle_bad_request(error):
    '''Handle 400 errors

    Args:
       error (Exception): The exception raised.

    Returns:
        The error message supplied.
    '''
    return jsonify(error=str(error)), 400


def handle_unauthorized(error):
    '''Handle 401 errors

    Args:
       error (Exception): The exception raised.

    Returns:
        The error message supplied.
    '''
    return jsonify(error=str(error)), 401


def handle_forbidden(error):
    '''Handle 403 errors

    Args:
       error (Exception): The exception raised.

    Returns:
        The error message supplied.
    '''
    return jsonify(error=str(error)), 403


def handle_page_not_found(error):
    '''Handle 404 errors

    Args:
       error (Exception): The exception raised.

    Returns:
        The error message supplied.
    '''
    return jsonify(error=str(error)), 404


def handle_internal_server_error(error):
    '''Handle 500 errors

    Args:
       error (Exception): The exception raised.

    Returns:
        The error message supplied.
    '''
    return jsonify(error=str(error)), 500
