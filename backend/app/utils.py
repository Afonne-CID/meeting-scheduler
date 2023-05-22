'''
This module defines utility functions for use in the app.
'''
from functools import wraps
from datetime import datetime
from dateutil.parser import isoparse
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity


def jwt_required_and_user_loaded(function):
    """
    Decorator function to require a JWT and load the user's
    identity from the token.

    The decorator first requires that a valid JWT is present in
    the request (using flask_jwt_extended.jwt_required).
    Then, it loads the user's identity from the JWT and stores it in
    Flask's application context global (g). If no identity is found,
    it returns a 401 response. If an identity is found, it proceeds with
    the execution of the decorated function.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(function)
    @jwt_required()
    def wrapper(*args, **kwargs):
        g.user_id = get_jwt_identity()
        if g.user_id is None:
            return {"msg": "Missing JWT identity"}, 401
        return function(*args, **kwargs)
    return wrapper


def is_valid_time_slot(start_time, end_time):
    """
    Validate a time slot.

    This function checks that the start_time is before the end_time and both are in the future.

    Args:
        start_time (str): The start time of the slot in ISO 8601 format.
        end_time (str): The end time of the slot in ISO 8601 format.

    Returns:
        bool: True if the time slot is valid, False otherwise.
    """

    now = datetime.utcnow()

    # Check if start_time is already a datetime object
    if not isinstance(start_time, datetime):
        start_time = isoparse(start_time)

    # Check if end_time is already a datetime object
    if not isinstance(end_time, datetime):
        end_time = isoparse(end_time)

    print(start_time < end_time and start_time > now and end_time > now)
    return start_time < end_time and start_time > now and end_time > now
