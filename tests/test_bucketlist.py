import unittest
from flask import json
from instance.config import app_config
from app.models import UserModel, BucketlistModel, BucketListItem, db
from app import create_app


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        print("setup")
        self.app = create_app("testing")

        # Get the current context we are in, either setup, active or in between
        # Captures things in that context
        self.app_context = self.app.app_context()

        # solves application not registered on db instance and no
        # applicationbound to current context
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # User registration
        user = {
            "first_name": "milly5",
            "last_name": "shiko6",
            "email": "milly0@gmail.com",
            "password": "password",
            "verify_password": "password"
        }

        user_login = {"email": "milly0@gmail.com",
                      "password": "password"}

        # add a bucketlist
        new_bucketlist = {
            "name": "Adventures"
        }

        # add a bucket item
        new_bucketlist_item = {
            "item_name": "Go to rome"
        }
        print(new_bucketlist_item)

        # add a bucketlist update
        new_bucketlist_update = {
            "name": "Explore the world",
        }
        print(new_bucketlist_update)

        # add a bucket item update
        new_bucketlist_item_update = {
            "item_name": "Go to Miami",
            "done": "True"
        }
        print(new_bucketlist_item_update)

        # register a new user
        response1 = self.client.post('/api/v1/auth/register',
                                     headers={"Accept": "application/json",
                                              "Content-Type": "application/json"},
                                     data=json.dumps(user))

        print("RESPONSE 1: " + str(response1.status_code))

        response2 = self.client.post('/api/v1/auth/login', headers={"Accept": "application/json",
                                                                    "Content-Type": "application/json"},
                                     data=json.dumps(user_login))

        print("RESPONSE 2: " + str(response2.status_code))

    def headers(self):
        api_headers = {
            #  what the browser is able to digest
            "Accept": "application/json",
            "Content-Type": "application/json"
            # "Authorization": "Bearer {}".format(UserModel.query.filter_by(email=email).first().generate_auth_token())
        }

        return api_headers

    def test_create_bucketlist(self):
        """
        Test API can create a bucketlist using POST request successfully.
        It should return status code 201 which means bucketlist Created
        successfully.
        """
        print("I am here")
        response = self.client.post("/api/v1/bucketlists/",
                                    data=json.dumps(self.new_bucketlist))
        print(response)
        print("Yes sir")

    #     self.assertEqual(response.status_code, 201)

    def tearDown(self):
        """teardown all initialized variables."""
        print("teardown")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

# use reqparse or marshmallow to validate data, 400
    # def test_get_all_bucketlists_if_no_content(self):
    #     """
    #     Test API can get all bucketlists using GET request if none.
    #
    #     """
    #     pass
