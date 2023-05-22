'''
This module defines the routes related to the user operations
such as registering and logging in a user.
'''

from flask import Blueprint, jsonify, request
from ..services import user_service
from ..exceptions import ResourceCreationError, UnexpectedError

user_routes = Blueprint('user_routes', __name__, url_prefix='/api')


@user_routes.route('/users', methods=['POST'])
def register_user():
    '''
    Registers a new user with the specified email and password.

    Returns:
        Response from the user service register_user function
        if registration is successful. 400 status code if
        required fields are missing. 500 status code and error message
        if there's an unexpected error.
    '''
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No JSON data in request'}), 400

    # validate incoming data
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        response, status_code = user_service.register_user(
            data['email'], data['password'])
        return jsonify(response), status_code
    except ResourceCreationError:
        return jsonify({'error': 'User creation failed'}), 400
    except UnexpectedError:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@user_routes.route('/users/login', methods=['POST'])
def login_user():
    '''
    Logs in a user with the specified email and password.

    Returns:
        Response from the user service login_user function
        if login is successful. 400 status code
        if required fields are missing.
    '''
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No JSON data in request'}), 400

    # validate incoming data
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    response, status_code = user_service.login_user(
        email=data['email'], password=data['password'])
    return jsonify(response), status_code
