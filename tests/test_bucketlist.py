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
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # add a bucketlist
        self.new_bucketlist = {
            'id': 1,
            'name': 'Adventures',
            'date_created': '2017-05-15 06:57:23',
            'date_modified': '2017-05-16 05:10:23',
            'created_by': '1'
        }

        # add a bucket item
        self.new_bucketlist_item = {
            'item_id': 1,
            'item_name': 'Go to rome',
            'date_created': '2017-05-15 07:00:23',
            'date_modified': '2017-05-16 08:00:00',
            'done': 'False'
        }

    def test_create_bucketlist(self):
        """Test API can create a bucketlist using POST request"""
        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))

        self.assertEqual(response.status_code, 201)

    def test_reject_create_bucketlist_duplicate(self):
        """Test API rejects bucketlist duplication"""
        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))

        self.assertEqual(response.status_code, 409)

    def test_reject_create_bucketlist_if_unauthorized(self):
        """Test API rejects creating a bucketlist if unauthorized"""
        response = self.client.post('/bucketlists/',
                                    data=json.dumps(self.new_bucketlist))

        self.assertEqual(response.status_code, 403)

    def test_create_bucketlist_item(self):
        """Test API can create a bucketlist using POST request"""
        response = self.client.post('/bucketlists/<id>/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 201)

    def test_reject_create_bucketlistitem_duplicate(self):
        """Test API rejects bucketlist item duplication"""
        response = self.client.post('/bucketlists/<id>/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 409)

    def test_reject_create_bucketlist_item_if_unauthorized(self):
        """Test API rejects creating a bucketlist item if unauthorized"""
        response = self.client.post('/bucketlists/<id>/items/',
                                    data=json.dumps(self.new_bucketlist_item))

        self.assertEqual(response.status_code, 403)

    def test_get_all_bucketlists(self):
        """Test API can get all bucketlists using GET request"""
        pass

    def test_api_rejects_get_all_bucketlists_if_unathorized(self):
        """Test API rejects getting all bucketlists if unauthorized"""
        pass

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist using it's id"""
        pass

    def test_api_rejects_getting_bucketlist_by_id_if_unathorized(self):
        """Test API rejects getting all bucketlist by id if unauthorized"""
        pass

    def test_api_gets_a_bucketlist_item_by_id(self):
        """Test API can get a bucketlist item by id"""
        pass

    def test_api_rejects_getting_a_bucketlist_item_by_id_if_unauthorized(self):
        """Test API rejects getting bucketlist item if unauthorized"""
        pass

    def test_edit_bucketlist(self):
        """Test API can edit an existing bucketlist using PUT request"""
        pass

    def test_reject_edit_bucketlist_if_unauthorized(self):
        """Test API rejects editing an existing bucketlist if anauthorized"""
        pass

    def test_edit_bucketlist_item(self):
        """Test API can edit an existing bucketlist item using PUT request"""
        pass

    def test_reject_editing_bucketlist_item_if_unauthorized(self):
        """
        Test API rejects editing an existing bucketlist item if anauthorized
        """
        pass

    def test_delete_bucketlist(self):
        """Test API can delete an existing bucketlist"""
        pass

    def test_reject_deleting_bucketlist_if_unauthorized(self):
        """
        Test API rejects deleting an existing bucketlist if anauthorized
        """
        pass

    def test_delete_bucketlist_item(self):
        """Test API can delete an existing bucketlist item"""
        pass

    def test_reject_deleting_a_bucketlist_item_if_unauthorized(self):
        """
        Test API rejects deleting an existing bucketlist item if anauthorized
        """
        pass

    def tearDown(self):
        """teardown all initialized variables."""
        pass
