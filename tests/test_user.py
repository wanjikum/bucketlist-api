import json
import os
import unittest
from flask import json
from instance.config import app_config
from app.models import db
from app import create_app
TEST_PATH = os.path.abspath(os.path.dirname(__file__))

class UserTestCases(unittest.TestCase):
    """A collection of user login and registration testcases"""
    def setUp(self):
        print("Setup")
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client our application
        self.client = self.app.test_client()

        # User registration
        self.user = {
            "first_name":"milly5",
            "last_name":"shiko6",
            "email":"milly0@gmail.com",
            "password":"password",
            "verify_password":"password"
        }

        # register user with no registration details
        self.invalid_user = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
            'verify_password': ''
        }

        # User login
        self.login = {
            'username': 'millicent.njuguna@gmail.com',
            'password': 'password'
        }

        # Login with no username
        self.login_with_no_username = {
            'username': '',
            'password': 'password'
        }

        # Login with no password
        self.login_with_no_password = {
            'username': 'millicent.njuguna@gmail.com',
            'password': ''
        }

        # Login with no username and password
        self.login_no_credentials = {
            'username': '',
            'password': ''
        }
    def tearDown(self):
        print("tearDown")
        # Delete the test database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def headers(self):
        api_headers= {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        return api_headers

    def test_register_user_successfully(self):
        """ Tests API registers a user successfully """

        # register a new user
        response = self.client.post('/api/v1/auth/register',
                                    headers=self.headers(),
                                    data=json.dumps(self.user))
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
        self.client.post('/api/v1/auth/register', headers=self.headers(),
                         data=json.dumps(self.user))

        # register the new user again
        response = self.client.post('/api/v1/auth/register',
                                    headers=self.headers(),
                                    data=json.dumps(self.user))

        self.assertEqual(response.status_code, 409)

    def test_login_user_successfully(self):
        """ Tests API logs in a user successfully """
        # login a new user
        user = {
            "first_name":"milly",
            "last_name":"shiko6",
            "email":"milly1@gmail.com",
            "password":"password",
            "verify_password":"password"
        }

        self.client.post('/api/v1/auth/register', headers=self.headers(),
                                    data=json.dumps(user))
        user_login = {
            "email":"milly1@gmail.com",
            "password":"password"
        }
        response = self.client.post('/api/v1/auth/login', headers=self.headers(),
                                    data=json.dumps(user_login))
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
