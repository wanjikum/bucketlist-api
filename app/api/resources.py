import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import request
from flask_restful import Resource, abort
from app.api.schema import get_user_register_schema
from app.api.responses import error_response, success_response
from app.models import UserModel


class UserRegisterApi(Resource):
    """Contains the user register functionalities"""

    def post(self):

        # gets json data from the url
        new_user = request.get_json()

        # if no json data available
        if not new_user:
            return error_response(message='No input provided')

        # check for validation errors
        validation_errors = get_user_register_schema.validate(new_user)

        # Return validation errors if available
        if validation_errors:
            return error_response(validation_errors=validation_errors)

        # check if both passwords given are equal
        password1 = new_user["password"]
        password2 = new_user["verify_password"]

        # if they are not equal
        if password1 != password2:
            return error_response(message='Password mismatch')

        # get data provided by the user
        first_name = new_user["first_name"].title()
        last_name = new_user["last_name"].title()
        email = new_user["email"].lower()
        password = new_user["password"]

        # reject adding a
        user_by_email = UserModel.query.filter_by(email=email).first()
        if user_by_email:
            return error_response(status=409,
                                  error='Conflict',
                                  message='The email provided already exists!')
        user = UserModel(first_name=first_name,
                         last_name=last_name,
                         email=email,
                         password=password)

        # add user to the database
        user.add(user)
        message = 'Congratulations {}!!!.'\
            'Your account has been successfully created.'\
            'Login to get started!'.format(first_name)
        return success_response(message=message)


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
