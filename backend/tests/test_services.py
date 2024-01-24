'''
This module contains unit tests for the service layer of the application.
'''

from datetime import datetime, timedelta
import unittest

# pylint: disable=unused-import,import-error
from app import create_app
from app.models.user import User
from app.models.meeting import Meeting
from app.models.timeslot import TimeSlot
from app.models.vote import Vote
from app.database import db
from app.services import (
    user_service,
    meeting_service,
    timeslot_service,
    vote_service)
from app.exceptions import ResourceCreationError


# Remove milliseconds from formatted strings
FUTURE_START_TIME = (datetime.utcnow() + timedelta(days=1)
                     ).replace(microsecond=0).isoformat()
FUTURE_END_TIME = (datetime.utcnow() + timedelta(days=1, hours=2)
                   ).replace(microsecond=0).isoformat()
PAST_START_TIME = (datetime.utcnow() - timedelta(hours=1)).isoformat()
PAST_END_TIME = (datetime.utcnow() - timedelta(hours=1)).isoformat()

class TestServices(unittest.TestCase):
    '''
    This class represents the test case for the service layer of
    the application, and inherits from the unittest.TestCase class.
    It contains setup and teardown methods,
    as well as individual test methods for each service function.
    '''
    def setUp(self):
        '''
        This method sets up the testing environment before each test.
        It creates a new application for testing, a new test client,
        a new application context,
        and a new database.
        '''
        self.app = create_app('testing')
        self.app.config.from_object('config.DevelopmentConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.test_user, _ = user_service.register_user('test@example.com', 'password123')
        self.test_meeting = meeting_service.create_meeting(self.test_user['user']['id'],
                                                      'Test Meeting',
                                                      'This is a test meeting', [])
        self.test_timeslot = timeslot_service.create_timeslot(self.test_user['user']['id'],
                                                         self.test_meeting.id,
                                                         FUTURE_START_TIME,
                                                         FUTURE_END_TIME)
        self.test_vote = vote_service.create_vote(self.test_user['user']['id'],
                                        self.test_timeslot.id)

    def tearDown(self):
        '''
        This method tears down the testing environment after each test.
        It removes the current database session, drops the database,
        and pops the application context.
        '''
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test Successes
    def test_success_register_user(self):
        '''
        This method tests the user_service.register_user function.
        It asserts that the returned user's email matches the input email,
        and that the returned user's password does not match the input password
        (because it should be hashed).
        '''
        self.assertEqual(self.test_user['user']['email'], 'test@example.com')

    def test_success_login_user(self):
        '''
        This method tests the user_service.login_user function.
        It asserts that the returned user's email matches the input email,
        and that the login service logs in a user with valid credentials.
        '''
        response, _ = user_service.login_user('test@example.com', 'password123')
        self.assertEqual(response['user']['email'], 'test@example.com')

    def test_success_create_meeting(self):
        '''
        This method tests the meeting_service.create_meeting function.
        It asserts that the returned meeting title matches the input title.
        '''
        self.assertEqual(self.test_meeting.title, 'Test Meeting')

    def test_success_create_timeslot(self):
        '''
        This method tests the timeslot_service.create_timeslot function.
        It asserts that the returned timeslot start_time and
        end_time matche the inputs.
        '''
        self.assertEqual(self.test_timeslot.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                         FUTURE_START_TIME)
        self.assertEqual(self.test_timeslot.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                         FUTURE_END_TIME)

    def test_success_create_timeslot_past_start_time(self):
        """
        Test that create_timeslot fails if the start_time is in the past.
        """
        with self.assertRaises(ResourceCreationError):
            timeslot_service.create_timeslot(self.test_user['user']['id'],
                                             self.test_meeting.id,
                                             PAST_START_TIME,
                                             FUTURE_END_TIME)

    def test_success_create_vote(self):
        '''
        This method tests the vote_service.create_vote function.
        It asserts that a vote's user_id matches the right user that owns the vote.
        '''
        self.assertEqual(self.test_vote.user_id, self.test_user['user']['id'])

    def test_success_update_meeting(self):
        '''
        This method tests the meeting_service.update_meeting function.
        It creates a user, a meeting, and then updates that meeting.
        It asserts that the returned meeting's title matches the new title.
        '''
        updated_meeting = meeting_service.update_meeting(
            self.test_user['user']['id'],
            self.test_meeting.id,
            'Updated Meeting',
            'This is an updated meeting')

        self.assertEqual(updated_meeting.title, 'Updated Meeting')

    def test_success_delete_meeting(self):
        '''
        This method tests the meeting_service.delete_meeting function.
        It creates a user and a meeting, and then deletes that meeting.
        It asserts that the deletion was successful.
        '''
        deleted = meeting_service.delete_meeting(self.test_user['user']['id'],
                                                 self.test_meeting.id)
        self.assertTrue(deleted)

    def test_success_update_timeslot(self):
        '''
        This method tests the timeslot_service.update_timeslot function.
        It creates a user, a meeting, a timeslot, and then updates that timeslot.
        It asserts that the returned timeslot's start_time matches the new start_time.
        '''
        updated_timeslot = timeslot_service.update_timeslot(
            self.test_user['user']['id'],
            self.test_timeslot.id, self.test_meeting.id,
            FUTURE_START_TIME,
            FUTURE_END_TIME)
        self.assertEqual(updated_timeslot.start_time.strftime(
            '%Y-%m-%dT%H:%M:%S'),
            FUTURE_START_TIME)

    def test_success_delete_timeslot(self):
        '''
        This method tests the timeslot_service.delete_timeslot function.
        It creates a user, a meeting, a timeslot, and then deletes that
        timeslot. It asserts that the returned timeslot's id matches
        the deleted timeslot's id.
        '''
        deleted_timeslot = timeslot_service.delete_timeslot(
            self.test_user['user']['id'],
            self.test_timeslot.id)
        self.assertEqual(deleted_timeslot, True)

    def test_success_delete_vote(self):
        '''
        This method tests the vote_service.delete_vote function.
        It creates a user, a meeting, a timeslot, a vote, and then
        deletes that vote. It asserts that the returned vote's id
        matches the deleted vote's id.
        '''
        deleted_vote = vote_service.delete_vote(self.test_user['user']['id'], self.test_vote.id)
        self.assertEqual(deleted_vote, True)

    def test_fail_create_timeslot_past_end_time(self):
        """
        Test that create_timeslot fails if the end_time is in the past.
        """
        with self.assertRaises(ResourceCreationError):
            timeslot_service.create_timeslot(self.test_user['user']['id'],
                                             self.test_meeting.id,
                                             FUTURE_START_TIME,
                                             PAST_END_TIME)

    def test_fail_create_timeslot_end_time_before_start_time(self):
        """
        Test that create_timeslot fails if the end_time is before the
        start_time.
        """
        with self.assertRaises(ResourceCreationError):
            timeslot_service.create_timeslot(self.test_user['user']['id'],
                                             self.test_meeting.id,
                                             FUTURE_END_TIME,
                                             FUTURE_START_TIME)

    # Test Fails
    def test_fail_register_user_with_existing_email(self):
        """
        Test that registering a user with an existing email fails and
        returns status code 409.

        This function:
        - Registers a user with a given email and password
        - Tries to register another user with the same email
        - Asserts that the status code of the second registration
        attempt is 409 (Conflict)
        """
        _, status_code = user_service.register_user('test@example.com', 'password123')
        self.assertEqual(status_code, 409)

    def test_fail_login_with_wrong_password(self):
        """
        Test that a user login attempt with a wrong password fails and
        returns status code 401.

        This function:
        - Registers a user with a given email and password
        - Tries to log in the user with a wrong password
        - Asserts that the status code of the login attempt is 401 (Unauthorized)
        """
        _, status_code = user_service.login_user('test@example.com', 'wrongpassword')
        self.assertEqual(status_code, 401)

    def test_fail_update_meeting_with_wrong_user_id(self):
        """
        Test that updating a meeting with a wrong user ID fails and returns None.

        This function:
        - Registers a user and creates a meeting associated with that user
        - Tries to update the meeting using a wrong user ID
        - Asserts that the updated meeting is None
        """
        updated_meeting = meeting_service.update_meeting('wrong_user_id',
                                                         self.test_meeting.id,
                                                         'Updated Meeting Title',
                                                         'Updated Description')
        self.assertEqual(updated_meeting, 'Unauthorized')

    def test_fail_delete_meeting_with_wrong_user_id(self):
        """
        Test that deleting a meeting with a wrong user ID fails and returns None.

        This function:
        - Registers a user and creates a meeting associated with that user
        - Tries to delete the meeting using a wrong user ID
        - Asserts that the deletion status is None
        """
        is_deleted = meeting_service.delete_meeting('wrong_user_id', self.test_meeting.id)
        self.assertIsNone(is_deleted)

    def test_fail_update_timeslot_with_wrong_user_id(self):
        """
        Test that updating a timeslot with a wrong user ID fails and returns None.

        This function:
        - Registers a user and creates a meeting and a timeslot associated with that user
        - Tries to update the timeslot using a wrong user ID
        - Asserts that the updated timeslot is None
        """
        updated_timeslot = timeslot_service.update_timeslot('wrong_user_id',
                                                            self.test_timeslot.id,
                                                            self.test_meeting.id,
                                                            FUTURE_START_TIME,
                                                            FUTURE_END_TIME)
        self.assertEqual(updated_timeslot, 'Unauthorized')

    def test_fail_delete_timeslot_with_wrong_user_id(self):
        """
        Test that deleting a timeslot with a wrong user ID fails and returns None.

        This function:
        - Registers a user and creates a meeting and a timeslot associated with that user
        - Tries to delete the timeslot using a wrong user ID
        - Asserts that the deletion status is None
        """
        deleted_timeslot = timeslot_service.delete_timeslot('wrong_user_id',
                                                            self.test_timeslot.id)
        self.assertEqual(deleted_timeslot, 'Unauthorized')

    def test_fail_delete_vote_with_wrong_user_id(self):
        """
        Test that deleting a vote with a wrong user ID fails and returns None.

        This function:
        - Registers a user and creates a meeting, a timeslot, and a vote
        associated with that user
        - Tries to delete the vote using a wrong user ID
        - Asserts that the deletion status is None
        """
        deleted_vote = vote_service.delete_vote('wrong_user_id', self.test_vote.id)
        self.assertEqual(deleted_vote, 'Unauthorized')


if __name__ == '__main__':
    unittest.main()
