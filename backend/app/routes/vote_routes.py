'''
This module defines the routes related to the vote operations
such as creating and deleting a vote.
'''

from flask import Blueprint, jsonify, request, g
from ..services import vote_service
from ..utils import jwt_required_and_user_loaded
from ..exceptions import (
    ResourceCreationError,
    UnauthorizedError,
    UnexpectedError)

vote_routes = Blueprint('vote_routes', __name__, url_prefix='/api')


@vote_routes.route('/votes', methods=['POST'])
@jwt_required_and_user_loaded
def create_vote():
    '''
    Creates a new vote for a given meeting timeslot by a user.

    Returns:
        The created vote as JSON, along with a 201 status code
        if the vote is created successfully. 400 status code
        if required fields are missing. 500 status code and
        error message if there's an unexpected error.
    '''
    data = request.get_json()

    # validate incoming data
    if not all(key in data for key in ['timeslot_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        vote = vote_service.create_vote(
            user_id=g.user_id, timeslot_id=data['timeslot_id'])
        return jsonify(vote.to_dict()), 201
    except UnauthorizedError:
        return jsonify({
                    'error': 'User is not authorized to create this vote'}
                    ), 403
    except ResourceCreationError:
        return jsonify({'error': 'Vote creation failed'}), 400
    except UnexpectedError:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@vote_routes.route('/votes/<int:vote_id>', methods=['DELETE'])
@jwt_required_and_user_loaded
def delete_vote(vote_id):
    '''
    Deletes a vote given its ID.

    Returns:
        A success message as JSON and a 200 status code
        if the vote is deleted successfully. 404 status code and
        error message if the vote is not found.
    '''
    vote = vote_service.delete_vote(user_id=g.user_id, vote_id=vote_id)
    if vote is None:
        return jsonify(error='Vote not found'), 404
    return jsonify(success=True), 200
