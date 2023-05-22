'''
This module provides services for creating and deleting a Vote.

Functions:
    create_vote: Creates a new vote.
    delete_vote: Deletes an existing vote.
'''

from flask import current_app
from sqlalchemy.exc import IntegrityError
from ..models.vote import Vote
from ..database import db
from ..exceptions import ResourceCreationError, UnexpectedError


def create_vote(user_id, timeslot_id):
    '''
    Create a new vote.

    Args:
        user_id (int): The ID of the user creating the vote.
        meeting_id (int): The ID of the meeting for which
                        the vote is being cast.
        timeslot_id (int): The ID of the timeslot for which
                        the vote is being cast.

    Returns:
        Vote: The created Vote object.

    Raises:
        Exception: If there is a problem creating the vote.
    '''

    try:
        vote = Vote(timeslot_id=timeslot_id, user_id=user_id)
        db.session.add(vote)
        db.session.commit()
        return vote
    except IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"Vote creation failed: {error}")
        raise ResourceCreationError("Vote creation failed") from error
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(error,
            "Unexpected error occurred in create_vote") from error


def delete_vote(user_id, vote_id):
    '''
    Delete a vote.

    Args:
        vote_id (int): The ID of the vote to be deleted.

    Returns:
        Vote: The deleted Vote object, or None if a vote with
        the provided ID does not exist.

    Raises:
        Exception: If there is a problem deleting the vote.
    '''
    try:
        vote = db.session.get(Vote, vote_id)
        if vote is None:
            return None
        if vote and vote.user_id != user_id:
            return 'Unauthorized'

        db.session.delete(vote)
        db.session.commit()
        return True
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(error,
            "Unexpected error occurred in delete_vote") from error
