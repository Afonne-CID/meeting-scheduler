'''
This module defines the User model for the application.

Classes:
    User: Represents a user in the database.

Dependencies:
    db: SQLAlchemy object instance for database operations.
'''

from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db


class User(db.Model):
    '''
    A class used to represent a User in the application's database.

    ...

    Attributes
    ----------
    id : int
        a unique identifier for each user
    email : str
        the email of the user, unique for each user
    password : str
        the hashed password of the user
    meetings : list
        a list of Meeting objects related to the user

    Methods
    -------
    __repr__():
        Represents the User instance as a string.
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    meetings = db.relationship('Meeting', backref='user', lazy=True)
    created_at = db.Column(db.DateTime(
        # pylint: disable=not-callable
        timezone=True), server_default=func.now())

    def set_password(self, password):
        '''Generate a hash for plain input password
        '''
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        '''Check if password is valid
        '''
        return check_password_hash(self.password, password)

    def to_dict(self):
        '''Convert User object to dictionionary
        '''
        return {
            'id': self.id,
            'email': self.email,
            'meetings': [meeting.to_dict() for meeting in self.meetings]
        }

    def __repr__(self):
        '''
        Represents the User instance as a string.

        Returns
        -------
        str
            a string representation of the user instance
        '''
        return f'<User {self.email}>'
