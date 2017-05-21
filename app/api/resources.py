import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import request, jsonify
from flask_restful import Resource, abort
from models import *
from schema import get_user_register_schema


class UserRegisterApi(Resource):
    """Contains the user register functionalities"""

    def post(self):

        # gets json data from the url
        new_user = request.get_json()

        # if no json data available
        if not new_user:
            return {'error': 'No input provided'}, 400

        # check for validation errors
        validation_errors = get_user_register_schema.validate(new_user)

        # Return validation errors if available
        if validation_errors:
            return validation_errors, 400

        # check if both passwords given are equal
        password1 = new_user["password"]
        password2 = new_user["verify_password"]

        # if they are not equal
        if password1 != password2:
            return 'The passwords provided do not match'

        # get data provided by the user
        first_name = new_user["first_name"]
        last_name = new_user["last_name"]
        email = new_user["email"]
        password = new_user["password"]
        return first_name, last_name, email, password


class UserLoginApi(Resource):
    """Contains the user login and register functionalities"""
    pass


class BucketlistApi(Resource):
    """Contains all bucketlist functionalities"""
    pass


class BucketlistsApi(Resource):
    """Contains all bucketlists functionalities"""
    pass


class BucketlistItemApi(Resource):
    """Contains bucketlist item functionalities"""
    pass


class BucketlistItemsApi(Resource):
    """Contains bucketlist items functionalities"""
    pass
