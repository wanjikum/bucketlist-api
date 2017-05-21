import unittest
from flask import json
from instance.config import app_config
from app.models import UserModel
from app import create_app, db


class BaseUserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test client our application
        self.client = self.app.test_client()

        # User registration
        self.user = {
            'first_name': 'Millicent',
            'last_name': 'Njuguna',
            'email': 'millicent.njuguna@gmail.com',
            'password': 'password',
            'verify_password': 'password'
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
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
