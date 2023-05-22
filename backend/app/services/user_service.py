'''
This module provides services for registering and logging in a User.

Functions:
    register_user: Register a new user.
    login_user: Log in a user.
'''

from datetime import timedelta
from flask_jwt_extended import create_access_token
from ..exceptions import UnexpectedError
from ..models.user import User
from ..database import db


def register_user(email, password):
    '''
    Register a new user with given email and password.

    If the user already exists, an error message will be returned.
    Otherwise, the new user is added to the database,
    and an access token is returned for the user.

    Args:
        email (str): The email of the user to register.
        password (str): The password of the user to register.

    Returns:
        dict: A dictionary with the access token for the registered user,
        or an error message.

    Raises:
        Exception: If there is a problem registering the user.
    '''
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return {'error': 'An account with this email already exists'}, 409

        new_user = User(email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(
            identity=new_user.id, expires_delta=timedelta(minutes=30))
        return {'user': new_user.to_dict(), 'token': access_token}, 201

    except Exception as error:
        db.session.rollback()
        raise UnexpectedError(error, 'Registration failed')


def login_user(email, password):
    '''
    Log in a user with given email and password.

    If the credentials are invalid, an error message will be returned.
    Otherwise, an access token is returned for the user.

    Args:
        email (str): The email of the user to log in.
        password (str): The password of the user to log in.

    Returns:
        dict: A dictionary with the access token for the user,
        or an error message.
    '''
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {'error': 'Invalid email or password'}, 401

    access_token = create_access_token(identity=user.id)
    return {'user': user.to_dict(), 'token': access_token}, 200
