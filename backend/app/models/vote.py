'''
This module defines the Vote model for the application.

Classes:
    Vote: Represents a vote in the database.

Dependencies:
    db: SQLAlchemy object instance for database operations.
    Meeting: Meeting model.
    User: User model.
'''

from sqlalchemy.sql import func
from ..database import db
from .meeting import Meeting  # pylint: disable=unused-import
from .user import User  # pylint: disable=unused-import


class Vote(db.Model):
    '''
    A class used to represent a Vote in the application's database.

    ...

    Attributes
    ----------
    id : int
        a unique identifier for each vote
    user_id : int
        a foreign key that identifies the user who cast the vote
    meeting_id : int
        a foreign key that identifies the meeting for which the vote was cast
    timeslot_id : int
        a foreign key that identifies the timeslot for which the vote was cast

    Methods
    -------
    __repr__():
        Represents the Vote instance as a string.
    '''

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timeslot_id = db.Column(
        db.Integer,
        db.ForeignKey('timeslots.id', ondelete='CASCADE'),
        nullable=False)
    created_at = db.Column(db.DateTime(
        # pylint: disable=not-callable
        timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timeslot_id': self.timeslot_id,
        }

    def __repr__(self):
        '''
        Represents the Vote instance as a string.

        Returns
        -------
        str
            a string representation of the vote instance
        '''
        return f'<Vote {self.id}>'
