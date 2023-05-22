'''
This module provides services for creating, updating and deleting
a TimeSlot.

Functions:
    create_timeslot: Create a new timeslot.
    update_timeslot: Update an existing timeslot.
    delete_timeslot: Delete a timeslot.
'''

from flask import current_app
from sqlalchemy.exc import IntegrityError
from dateutil.parser import isoparse
from ..utils import is_valid_time_slot
from ..models.timeslot import TimeSlot
from ..database import db
from ..exceptions import ResourceCreationError, UnexpectedError



def create_timeslot(user_id, meeting_id, start_time, end_time):
    '''
    Create a new timeslot for a specific meeting with given
    start_time and end_time.

    Args:
        meeting_id (int): The ID of the meeting for which
                        the timeslot is created.
        start_time (datetime): The start time of the timeslot.
        end_time (datetime): The end time of the timeslot.

    Returns:
        The created TimeSlot object.

    Raises:
        Exception: If there is a problem creating the timeslot.
    '''
    try:
        timeslot = TimeSlot(
            user_id=user_id,
            meeting_id=meeting_id,
            start_time=isoparse(start_time),
            end_time=isoparse(end_time))
        db.session.add(timeslot)
        db.session.commit()
        return timeslot
    except IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"TimeSlot creation failed: {error}")
        raise ResourceCreationError("TimeSlot creation failed") from error
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in create_timeslot") from error


def update_timeslot(user_id, timeslot_id, meeting_id=None, start_time=None, end_time=None):
    '''
    Update an existing timeslot with given meeting_id and/or start_time
    and/or end_time.

    Args:
        timeslot_id (int): The ID of the timeslot to update.
        meeting_id (int, optional): The new ID of the meeting for which
                                the timeslot is created. Defaults to None.
        start_time (datetime, optional): The new start time of the timeslot.
                                        Defaults to None.
        end_time (datetime, optional): The new end time of the timeslot.
                                        Defaults to None.

    Returns:
        The updated TimeSlot object or None if the timeslot does not exist.

    Raises:
        Exception: If there is a problem updating the timeslot.
    '''
    try:
        timeslot = db.session.get(TimeSlot, timeslot_id)
        if timeslot is None:
            return None
        if timeslot and timeslot.user_id != user_id:
            return None

        if meeting_id is not None:
            timeslot.meeting_id = meeting_id
        if start_time is not None:
            timeslot.start_time = start_time
        if end_time is not None:
            timeslot.end_time = end_time

        db.session.commit()
        return timeslot
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in update_timeslot") from error


def delete_timeslot(user_id, timeslot_id):
    '''
    Delete a timeslot with a given ID.

    Args:
        timeslot_id (int): The ID of the timeslot to delete.

    Returns:
        The deleted TimeSlot object or None if the timeslot does not exist.

    Raises:
        Exception: If there is a problem deleting the timeslot.
    '''
    try:
        timeslot = db.session.get(TimeSlot, timeslot_id)
        if timeslot is None:
            return None
        if timeslot and timeslot.user_id != user_id:
            return None

        db.session.delete(timeslot)
        db.session.commit()
        return timeslot
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in delete_timeslot") from error
