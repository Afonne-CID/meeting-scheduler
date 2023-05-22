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
        user_id (int): The ID of the user creating the timeslot.
        meeting_id (int): The ID of the meeting for which
                        the timeslot is created.
        start_time (datetime or str): The start time of the timeslot in ISO 8601 format or as a datetime object.
        end_time (datetime or str): The end time of the timeslot in ISO 8601 format or as a datetime object.

    Returns:
        The created TimeSlot object.

    Raises:
        ValueError: If the timeslot is invalid.
        ResourceCreationError: If there is a problem creating the timeslot.
        UnexpectedError: If an unexpected error occurs during timeslot creation.
    '''
    try:
        if not is_valid_time_slot(start_time, end_time):
            raise ValueError('Invalid time slot')

        timeslot = TimeSlot(
            user_id=user_id,
            meeting_id=meeting_id,
            start_time=start_time,
            end_time=end_time)
        db.session.add(timeslot)
        db.session.commit()
        return timeslot
    except IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"TimeSlot creation failed: {error}")
        raise ResourceCreationError("TimeSlot creation failed") from error
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"Invalid time slot: {error}")
        raise ResourceCreationError("Invalid time slot") from error
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(error, "Unexpected error occurred in create_timeslot") from error

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
            return 'Unauthorized'
        if timeslot and meeting_id != timeslot.meeting_id:
            return 'Invalid request'

        if start_time is not None:
            new_start_time = isoparse(start_time)
        else:
            new_start_time = timeslot.start_time

        if end_time is not None:
            new_end_time = isoparse(end_time)
        else:
            new_end_time = timeslot.end_time

        if not is_valid_time_slot(start_time, end_time):
            raise ValueError('Invalid time slot')

        timeslot.start_time = new_start_time
        timeslot.end_time = new_end_time

        db.session.commit()
        return timeslot
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(error,
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
            return 'Unauthorized'

        db.session.delete(timeslot)
        db.session.commit()
        return True
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(error,
            "Unexpected error occurred in delete_timeslot") from error
