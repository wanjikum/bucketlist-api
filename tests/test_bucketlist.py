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

    def test_reject_create_bucketlist_if_unauthorized(self):
        """Test API rejects creating a bucketlist if unauthorized"""
        pass

    def test_create_bucketlist_item(self):
        """Test API can create a bucketlist using POST request"""
        pass

    def test_reject_create_bucketlist_item_if_unauthorized(self):
        """Test API rejects creating a bucketlist item if unauthorized"""
        pass

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

    def test_api_lists_a_bucketlist_with_all_bucketlist_items(self):
        """Test API can list a bucketlist with all bucketlist items"""
        pass

    def test_api_rejects_listing_bucketlist_contents_if_unauthorized(self):
        """Test API rejects listing bucketlist content if unauthorized"""
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

    def test_reject_deleting_bucketlist(self):
        """
        Test API rejects deleting an existing bucketlist if anauthorized
        """
        pass

    def test_delete_bucketlist_item(self):
        """Test API can delete an existing bucketlist item"""
        pass

    def test_reject_deleting_a_bucketlist_item(self):
        """
        Test API rejects deleting an existing bucketlist item if anauthorized
        """
        pass

    def tearDown(self):
        """teardown all initialized variables."""
        pass
