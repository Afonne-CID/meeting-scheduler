'''This module defines the Meeting model for the application.

Classes:
    Meeting: Represents a meeting in the database.

Dependencies:
    db: SQLAlchemy object instance for database operations.
    User: User model to establish a relationship with the Meeting model.
'''

from sqlalchemy.sql import func
from ..database import db
from .user import User  # pylint: disable=unused-import


class Meeting(db.Model):
    '''
    Meeting Model

    Represents a meeting in the database with its associated information.

    Attributes:
        id (int): The unique identifier of the meeting.
        title (str): The title of the meeting.
        description (str): An optional description of the meeting.
        user_id (int): The identifier of the user who created the meeting.
        timeslots (relationship): The timeslots proposed for the meeting.
        votes (relationship): The votes cast on the meeting's timeslots.
    '''

    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    timeslots = db.relationship(
        'TimeSlot', backref='meeting', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime(
        # pylint: disable=not-callable
        timezone=True), server_default=func.now())

    def to_dict(self):
        '''Convert Meeting object to dictionionary
        '''
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'timeslots': [timeslot.to_dict() for timeslot in self.timeslots]
        }

    def __repr__(self):
        '''
        Returns the string representation of the meeting.

        Returns:
            str: A string in the format <Meeting {title}>.
        '''
        return f'<Meeting {self.title}>'
