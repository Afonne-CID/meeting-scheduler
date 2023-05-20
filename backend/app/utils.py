'''
This module defines utility functions for use in the app.
'''
from functools import wraps
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity


def jwt_required_and_user_loaded(f):
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
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        g.user_id = get_jwt_identity()
        if g.user_id is None:
            return {"msg": "Missing JWT identity"}, 401
        return f(*args, **kwargs)
    return wrapper
