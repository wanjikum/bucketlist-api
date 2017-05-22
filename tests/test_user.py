import json
from tests.user_basetest import BaseUserTest
from app import db


class UserTestCases(BaseUserTest):
    """A collection of user login and registration testcases"""

    def register_new_user(self):
        """Creates a new user"""

        # register a new user
        new_user = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(dict(
            first_name="milly1",
            last_name="shiko",
            email="milly4@gmail.com",
            password="password",
            verify_password="password"
        )),
        content_type='application/json')

        # return the response
        return new_user

    def test_register_user_successfully(self):
        """ Tests API registers a user successfully """

        # register a new user
        response = self.register_new_user()
        self.assertEqual(response.status_code, 200)

    def test_register_user_with_no_details(self):
        """Test API rejects registration of a user who has invalid input"""

        # register a new user using invalid input(bad request)
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(self.invalid_user))
        self.assertEqual(response.status_code, 400)

    def test_register_an_existing_user(self):
        """Test API rejects registering an existing user"""

        # register a new user
        user1_response = self.register_new_user()

        # register the new user again
        user2_response = self.register_new_user()

        self.assertEqual(user2_response.status_code, 409)

    def test_login_user_successfully(self):
        """ Tests API logs in a user successfully """
        # login a new user
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.login))
        self.assertEqual(response.status_code, 200)

    def test_login_user_with_no_username_but_has_password(self):
        """ Tests API  """

        # login a user with no username
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(
                                        self.login_with_no_username))
        self.assertEqual(response.status_code, 400)

    def test_login_user_with_a_username_but_has_no_password(self):
        """ Tests API  """

        # login a user with no password
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(
                                        self.login_with_no_password))
        self.assertEqual(response.status_code, 400)

    def test_login_user_with_no_credentials(self):
        """ Tests API  """

        # login a user with no credentials
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(
                                        self.login_no_credentials))
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """teardown all initialized variables."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
