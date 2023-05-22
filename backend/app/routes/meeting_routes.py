'''
This module defines the routes for handling meetings in the application.

It includes routes for creating, updating and deleting meetings.

Blueprint:
    meeting_routes: Blueprint that handles requests related to meetings.

Dependencies:
    flask: Flask module for request handling and response generation.
    meeting_service: Service module that contains the business logic
                    for handling meetings.
    jwt_required_and_user_loaded: Decorator for routes that
                    require authenticated users.
'''

from flask import Blueprint, jsonify, request, g
from ..services import meeting_service
from ..utils import jwt_required_and_user_loaded
from ..exceptions import (
    ResourceCreationError,
    UnauthorizedError,
    UnexpectedError)


meeting_routes = Blueprint('meeting_routes', __name__, url_prefix='/api')


@meeting_routes.route('/meetings/<int:meeting_id>', methods=['GET'])
@jwt_required_and_user_loaded
def get_meeting(meeting_id):
    '''
    Route for fetching an existing meeting.

    Parameters
    ----------
    meeting_id : int
        The ID of the meeting to fetch.

    Returns
    -------
    json
        The meeting as a JSON object, or an error message.
    '''
    meeting = meeting_service.get_meeting(meeting_id=meeting_id)
    if meeting is None:
        return jsonify(error='Meeting not found'), 404
    return jsonify(meeting.to_dict()), 200


@meeting_routes.route('/meetings', methods=['GET'])
@jwt_required_and_user_loaded
def get_meetings():
    '''
    Route for fetching all meetings created by a user.

    Returns
    -------
    json
        A list of meetings as JSON objects, or an error message.
    '''
    user_id = g.user_id
    meetings = meeting_service.get_meetings(user_id)
    if not meetings:
        return jsonify(error='No meetings found for this user'), 404
    return jsonify([meeting.to_dict() for meeting in meetings]), 200


@meeting_routes.route('/meetings', methods=['POST'])
@jwt_required_and_user_loaded
def create_meeting():
    '''
    Route for creating a new meeting.

    Returns
    -------
    json
        The created meeting as a JSON object, or an error message.
    '''
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No JSON data in request'}), 400

    # validate incoming data
    if not all(key in data for key in ['title', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400

    # validate the content of the fields
    if len(data['title']) > 100:
        return jsonify({'error': 'Title is too long'}), 400

    time_slots = data.get('timeSlots', [])

    # handle potential errors with a try-except block
    try:
        meeting = meeting_service.create_meeting(
            title=data['title'],
            description=data['description'],
            user_id=g.user_id,
            time_slots=time_slots)
        return jsonify(meeting.to_dict()), 201
    except UnauthorizedError:
        return jsonify({
                    'error': 'User is not authorized to create this meeting'}
                    ), 403
    except ResourceCreationError:
        return jsonify({'error': 'Meeting creation failed'}), 400
    except UnexpectedError:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@meeting_routes.route('/meetings/<int:meeting_id>', methods=['PUT', 'PATCH'])
@jwt_required_and_user_loaded
def update_meeting(meeting_id):
    '''
    Route for updating an existing meeting.

    Returns
    -------
    json
        The updated meeting as a JSON object, or an error message.
    '''

    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No JSON data in request'}), 400

    try:
        meeting = meeting_service.update_meeting(
            user_id=g.user_id,
            meeting_id=meeting_id,
            title=data.get('title'),
            description=data.get('description'),
        )
        if meeting is None:
            return jsonify({'error': 'Meeting not found'}), 404

        return jsonify(meeting.to_dict()), 200
    except UnexpectedError as e:
        return jsonify({'error': str(e)}), 500


@meeting_routes.route('/meetings/<int:meeting_id>', methods=['DELETE'])
@jwt_required_and_user_loaded
def delete_meeting(meeting_id):
    '''
    Route for deleting an existing meeting.

    Parameters
    ----------
    meeting_id : int
        The ID of the meeting to delete.

    Returns
    -------
    json
        A success message if the meeting is deleted, or an error message.
    '''
    meeting = meeting_service.delete_meeting(
        user_id=g.user_id, meeting_id=meeting_id)
    if meeting is None:
        return jsonify(error='Meeting not found'), 404
    return jsonify(success=True), 200
