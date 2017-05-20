import unittest
from flask import json
from instance.config import app_config
from app.models import UserModel, BucketlistModel, BucketListItem
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')

        # Get the current context we are in, either setup, active or in between
        # Captures things in that context
        self.app_context = self.app.app_context()

        # solves application not registered on db instance and no
        # applicationbound to current context
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # add a bucketlist
        self.new_bucketlist = {
            'name': 'Adventures'
        }

        # add a bucket item
        self.new_bucketlist_item = {
            'item_name': 'Go to rome'
        }

        # add a bucketlist update
        self.new_bucketlist_update = {
            'name': 'Explore the world'
        }

        # add a bucket item update
        self.new_bucketlist_item_update = {
            'item_name': 'Go to Miami',
            'done': 'True'
        }

    def test_create_bucketlist(self):
        """
        Test API can create a bucketlist using POST request successfully.
        It should return status code 201 which means bucketlist Created
        successfully.
        """
        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))

        self.assertEqual(response.status_code, 201)

    def test_reject_create_bucketlist_duplicate(self):
        """
        Test API rejects bucketlist duplication.
        It should return status code 409 which means Conflict.
        """
        self.client.post('/bucketlists/', data=json.dumps(self.new_bucketlist))
        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))

        self.assertEqual(response.status_code, 409)

    def test_reject_create_bucketlist_if_unauthorized(self):
        """
        Test API rejects creating a bucketlist if unauthorized.
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))

        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist_item(self):
        """
        Test API can create a bucketlist item using POST request.
        It should return status code 201 which means bucketlist item
        Created successfully.
        """
        response = self.client.post('/bucketlists/1/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 201)

    def test_reject_create_bucketlist_item_duplicate(self):
        """
        Test API rejects bucketlist item duplication.
        It should return status code 409 which means Conflict.
        """
        self.client.post('/bucketlists/1/items/',
                         data=json.dumps(self.new_bucketlist_item))
        response = self.client.post('/bucketlists/1/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 409)

    def test_reject_create_bucketlist_item_if_unauthorized(self):
        """
        Test API rejects creating a bucketlist item if unauthorized.
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.post('/bucketlists/1/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist_item_using_non_existing_bucketlist(self):
        """
        Test API rejects creating a bucketlist item if the bucketlist does not
        exist. It should return status code 404 which means page not found.
        """
        response = self.client.post('/bucketlists/19/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 404)

    def test_get_all_bucketlists(self):
        """
        Test API can get all bucketlists using GET request.
        It should return status code 200 which means OK.
        """
        response = self.client.get('/bucketlists/')

        self.assertEqual(response.status_code, 200)

    def test_api_rejects_get_all_bucketlists_if_unathorized(self):
        """
        Test API rejects getting all bucketlists if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.get('/bucketlists/')

        self.assertEqual(response.status_code, 401)

    def test_api_can_get_bucketlist_by_id(self):
        """
        Test API can get a single bucketlist using it's id
        It should return status code 200 which means ok.
        """

        response = self.client.get('/bucketlists/1')

        self.assertEqual(response.status_code, 200)

    def test_api_rejects_getting_bucketlist_by_id_if_unathorized(self):
        """
        Test API rejects getting a bucketlist by id if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.get('/bucketlists/1')

        self.assertEqual(response.status_code, 401)

    def test_api_rejects_getting_bucketlist_if_it_does_not_exist(self):
        """
        Test API rejects getting all bucketlist by id if it does not exist
        It should return status code 404 which means page not found.
        """
        response = self.client.get('/bucketlists/19')

        self.assertEqual(response.status_code, 404)

    def test_api_gets_a_bucketlist_item_by_id_successfully(self):
        """
        Test API can get a bucketlist item by id
        It should return status code 200 which means ok.
        """

        response = self.client.get('/bucketlists/1/items/1')

        self.assertEqual(response.status_code, 200)

    def test_api_rejects_getting_a_bucketlist_item_by_id_if_unauthorized(self):
        """
        Test API rejects getting a bucketlist item if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.get('/bucketlists/1/items/1')

        self.assertEqual(response.status_code, 401)

    def test_api_rejects_getting_bucketlist_item_if_it_does_not_exist(self):
        """
        Test API rejects getting a bucketlist item by id if it does not exist
        It should return status code 404 which means page not found.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.get('/bucketlists/1/items/19')

        self.assertEqual(response.status_code, 404)

    def test_edit_bucketlist_successfully(self):
        """
        Test API can edit an existing bucketlist using PUT request successfully
        It should return status code 200 which means ok.
        """

        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(self.new_bucketlist_update))

        self.assertEqual(response.status_code, 200)

    def test_reject_edit_bucketlist_if_unauthorized(self):
        """
        Test API rejects editing an existing bucketlist if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(self.new_bucketlist_update))

        self.assertEqual(response.status_code, 401)

    def test_reject_edit_bucketlist_if_it_does_not_exist(self):
        """
        Test API rejects editing an existing bucketlist if it does not exist
        It should return status code 404 which means page not found.
        """
        response = self.client.put('/bucketlists/19',
                                   data=json.dumps(self.new_bucketlist_update))

        self.assertEqual(response.status_code, 404)

    def test_edit_bucketlist_item_successfully(self):
        """
        Test API can edit an existing bucketlist item using PUT request
        It should return status code 200 which means ok.
        """
        response = self.client.put('/bucketlists/1/items/1',
                                   data=json.dumps(
                                       self.new_bucketlist_item_update))
        self.assertEqual(response.status_code, 200)

    def test_reject_editing_bucketlist_item_if_unauthorized(self):
        """
        Test API rejects editing an existing bucketlist item if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.put('/bucketlists/1/items/1',
                                   data=json.dumps(
                                       self.new_bucketlist_item_update))
        self.assertEqual(response.status_code, 401)

    def test_reject_editing_bucketlist_item_if_it_does_not_exist(self):
        """
        Test API rejects editing an existing bucketlist item if it does not
        exist. It should return status code 404 which means page not found.
        """
        response = self.client.put('/bucketlists/1/items/19',
                                   data=json.dumps(
                                       self.new_bucketlist_item_update))
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist_item_successfully(self):
        """
        Test API can delete an existing bucketlist item successfully
        It should return status code 200 which means ok.
        """
        response = self.client.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)

    def test_reject_deleting_a_bucketlist_item_if_unauthorized(self):
        """
        Test API rejects deleting an existing bucketlist item if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 401)

    def test_reject_deleting_a_bucketlist_item_if_it_does_not_exist(self):
        """
        Test API rejects deleting a bucketlist item that does not exist
        It should return status code 404 which means page not found.
        """
        response = self.client.delete('/bucketlists/1/items/19')
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist_successfully(self):
        """
        Test API can delete an existing bucketlist successfully
        It should return status code 200 which means ok.
        """
        response = self.client.delete('/bucketlists/1')

        self.assertEqual(response.status_code, 200)

    def test_reject_deleting_bucketlist_if_unauthorized(self):
        """
        Test API rejects deleting an existing bucketlist if unauthorized
        It should return status code 401 which means unauthorized.
        """
        # use an unauthorized user
        # self.client().post('user/logout')
        response = self.client.delete('/bucketlists/1')
        self.assertEqual(response.status_code, 401)

    def test_reject_deleting_bucketlist_if_it_does_not_exist(self):
        """
        Test API rejects deleting a bucketlist if it does not exist
        It should return status code 404 which means page not found.
        """
        response = self.client.delete('/bucketlists/19')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
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
