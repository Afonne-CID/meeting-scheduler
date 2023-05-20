'''
This module defines the routes related to the timeslot operations
such as creating, updating, and deleting timeslots.
'''

from flask import Blueprint, jsonify, request, g
from ..services import timeslot_service
from ..utils import jwt_required_and_user_loaded
from ..exceptions import (
    ResourceCreationError,
    UnauthorizedError,
    UnexpectedError)


timeslot_routes = Blueprint(
                            'timeslot_routes', __name__,
                            url_prefix='/api')


@timeslot_routes.route('/timeslots', methods=['POST'])
@jwt_required_and_user_loaded
def create_timeslot():
    '''
    Creates a timeslot with the specified meeting_id, start_time,
    and end_time. The timeslot is created in the context of the current user.

    Returns:
        201 status code and json representation of the timeslot
        if creation is successful. 400 status code
        if required fields are missing. 500 status code and error message
        if there's an unexpected error.
    '''
    data = request.get_json()

    # validate incoming data
    if not all(key in data for key in ['meeting_id',
                                       'start_time',
                                       'end_time']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        timeslot = timeslot_service.create_timeslot(
            user_id=g.user_id,
            meeting_id=data['meeting_id'],
            start_time=data['start_time'],
            end_time=data['end_time'])
        return jsonify(timeslot.to_dict()), 201
    except UnauthorizedError:
        return jsonify({
                    'error': 'User is not authorized to create this timeslot'}
                    ), 403
    except ResourceCreationError:
        return jsonify({'error': 'TimeSlot creation failed'}), 400
    except UnexpectedError:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@timeslot_routes.route('/timeslots/<int:timeslot_id>', methods=['PUT', 'PATCH'])
@jwt_required_and_user_loaded
def update_timeslot(timeslot_id):
    '''
    Updates the timeslot with the specified timeslot_id.

    Returns:
        200 status code and json representation of the timeslot
        if update is successful. 404 status code if timeslot is not found.
    '''
    data = request.get_json()
    timeslot = timeslot_service.update_timeslot(
        user_id=g.user_id,
        timeslot_id=timeslot_id,
        meeting_id=data.get('meeting_id'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'))
    if timeslot is None:
        return jsonify(error='Timeslot not found'), 404
    return jsonify(timeslot.to_dict()), 200


@timeslot_routes.route('/timeslots/<int:timeslot_id>', methods=['DELETE'])
@jwt_required_and_user_loaded
def delete_timeslot(timeslot_id):
    '''
    Deletes the timeslot with the specified timeslot_id.

    Returns:
        200 status code and success message if deletion is successful.
        404 status code if timeslot is not found.
    '''
    timeslot = timeslot_service.delete_timeslot(
        user_id=g.user_id,
        timeslot_id=timeslot_id)
    if timeslot is None:
        return jsonify(error='Timeslot not found'), 404
    return jsonify(success=True), 200
