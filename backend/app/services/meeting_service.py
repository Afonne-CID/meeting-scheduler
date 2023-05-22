'''
This module provides services for creating, updating and deleting a Meeting.

Functions:
    create_meeting: Create a new meeting.
    update_meeting: Update an existing meeting.
    delete_meeting: Delete a meeting.
'''
from flask import current_app
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from . import timeslot_service
from ..models.meeting import Meeting
from ..models.vote import Vote
from ..models.timeslot import TimeSlot
from ..database import db
from ..exceptions import ResourceCreationError, UnexpectedError


def get_meeting(meeting_id):
    '''
    Fetch a meeting with a given ID.

    Args:
        meeting_id (int): The ID of the meeting to fetch.

    Returns:
        The Meeting object or None if the meeting does not exist.
    '''

    try:
        meeting = Meeting.query.options(
            joinedload(Meeting.timeslots),
        ).get(meeting_id)
        return meeting
    except Exception as error:
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in get_meeting") from error


def get_meetings(user_id):
    '''
    Fetch all meetings created by a user, created a timeslot in, or voted on.

    Args:
        user_id (int): The ID of the user.

    Returns:
        A list of Meeting objects.
    '''
    try:
        # Fetch all meetings where the user is the creator
        created_meetings = Meeting.query.options(
            joinedload(Meeting.timeslots),
        ).filter_by(user_id=user_id).order_by(Meeting.created_at.desc()).all()

        # Fetch all meetings where the user has created a timeslot
        timeslots = TimeSlot.query.filter_by(user_id=user_id).all()
        timeslot_created_meetings = []
        for timeslot in timeslots:
            meeting = Meeting.query.options(
                joinedload(Meeting.timeslots),
            ).get(timeslot.meeting_id)
            if meeting not in timeslot_created_meetings:
                timeslot_created_meetings.append(meeting)

        # Fetch all meetings where the user has voted
        votes = Vote.query.filter_by(user_id=user_id).all()
        voted_meetings = []
        for vote in votes:
            timeslot = TimeSlot.query.get(vote.timeslot_id)
            meeting = Meeting.query.options(
                joinedload(Meeting.timeslots),
            ).get(timeslot.meeting_id)
            if meeting not in voted_meetings:
                voted_meetings.append(meeting)

        # Merge the three sets of meetings together
        meetings = list(
            set(created_meetings + voted_meetings + timeslot_created_meetings))

        return meetings
    except Exception as error:
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in get_all_meetings_by_user") from error


def create_meeting(user_id, title, description, time_slots):
    '''
    Create a new meeting with given title, description, user_id and time_slots.

    Args:
        title (str): The title of the meeting.
        description (str): The description of the meeting.
        user_id (int): The ID of the user who creates the meeting.
        time_slots (list): A list of time slots.

    Returns:
        The created Meeting object.

    Raises:
        Exception: If there is a problem creating the meeting.
    '''
    try:
        meeting = Meeting(
            title=title, description=description, user_id=user_id)
        db.session.add(meeting)
        db.session.flush()  # Flush to get the meeting id

        # Loop through time_slots and add each to the database
        for slot in time_slots:
            start_time = isoparse(slot['startTime'])
            end_time = isoparse(slot['endTime'])
            time_slot = TimeSlot(
                user_id=user_id,
                meeting_id=meeting.id,
                start_time=start_time,
                end_time=end_time)

            db.session.add(time_slot)

        db.session.commit()
        return meeting
    except IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"Meeting creation failed: {error}")
        raise ResourceCreationError("Meeting creation failed") from error
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in create_meeting") from error


def update_meeting(user_id, meeting_id, title, description):
    '''
    Update a new meeting with given title and description.

    Args:
        title (str): The title of the meeting.
        description (str): The description of the meeting.
        meeting_id (int): The ID of the meeting to update.
        user_id (int): The ID of the user who updates the meeting.

    Returns:
        The updated Meeting object.

    Raises:
        Exception: If there is a problem updating the meeting.
    '''
    try:
        meeting = db.session.get(Meeting, meeting_id)
        if meeting is None:
            return None
        if meeting and meeting.user_id != user_id:
            return None

        if title is not None:
            meeting.title = title
        if description is not None:
            meeting.description = description

        db.session.commit()
        return meeting
    except Exception as error:
        db.session.rollback()
        raise UnexpectedError("Could not update meeting.") from error


def delete_meeting(user_id, meeting_id):
    '''
    Delete a meeting with a given ID.

    Args:
        meeting_id (int): The ID of the meeting to delete.

    Returns:
        The deleted Meeting object or None if the meeting does not exist.

    Raises:
        Exception: If there is a problem deleting the meeting.
    '''
    try:
        meeting = db.session.get(Meeting, meeting_id)
        if meeting is None:
            return None
        if meeting and meeting.user_id != user_id:
            return None

        db.session.delete(meeting)
        db.session.commit()
        return True
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error: {error}")
        raise UnexpectedError(
            "Unexpected error occurred in delete_meeting") from error
