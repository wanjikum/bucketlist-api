import unittest
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        pass

    def test_create_bucketlist(self):
        """Test API can create a bucketlist using POST request"""
        pass

    def test_create_bucketlist_item(self):
        """Test API can create a bucketlist using POST request"""
        pass

    def test_get_all_bucketlists(self):
        """Test API can get all bucketlists using GET request"""
        pass

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist using it's id"""
        pass

    def test_list_a_bucketlist_with_all_bucketlist_items(self):
        """Test API can list a bucketlist with all bucketlist items"""
        pass

    def test_edit_bucketlist(self):
        """Test API can edit an existing bucketlist using PUT request"""
        pass

    def test_edit_bucketlist_item(self):
        """Test API can edit an existing bucketlist item using PUT request"""
        pass

    def test_delete_bucketlist(self):
        """Test API can delete an existing bucketlist"""
        pass

    def test_delete_bucketlist_item(self):
        """Test API can delete an existing bucketlist item"""
        pass

    def tearDown(self):
        """teardown all initialized variables."""
        pass
