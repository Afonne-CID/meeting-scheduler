'''
This module defines the TimeSlot model for the application.

Classes:
    TimeSlot: Represents a timeslot related to a meeting in the database.

Dependencies:
    db: SQLAlchemy object instance for database operations.
    Meeting: Meeting model to establish a relationship with the TimeSlot model.
'''

from sqlalchemy.sql import func
from ..database import db
from .meeting import Meeting  # pylint: disable=unused-import
from .vote import Vote  # pylint: disable=unused-import


class TimeSlot(db.Model):
    '''
    A class used to represent a TimeSlot in the application's database.

    ...

    Attributes
    ----------
    id : int
        a unique identifier for each timeslot
    start_time : datetime
        the starting time of the timeslot
    end_time : datetime
        the ending time of the timeslot
    meeting_id : int
        the id of the meeting the timeslot is associated with

    Methods
    -------
    __repr__():
        Represents the TimeSlot instance as a string.
    '''

    __tablename__ = 'timeslots'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey(
        'meetings.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    votes = db.relationship('Vote', backref='meeting',
                            lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime(
        # pylint: disable=not-callable
        timezone=True), server_default=func.now())

    def to_dict(self):
        '''Converts TimeSlot object to dictionary
        '''
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time if isinstance(self.start_time, str) else self.start_time.isoformat(),
            'end_time': self.end_time if isinstance(self.end_time, str) else self.end_time.isoformat(),
            'meeting_id': self.meeting_id,
            'votes': [vote.to_dict() for vote in self.votes]
        }

    def __repr__(self):
        '''
        Represents the TimeSlot instance as a string.

        Returns
        -------
        str
            a string representation of the timeslot instance
        '''
        return f'<TimeSlot from {self.start_time} to {self.end_time}>'
