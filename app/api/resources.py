import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import request, g, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api.schema import (get_user_register_schema,
                            get_user_login_schema,
                            get_bucketlist_schema)
from app.api.responses import error_response, success_response
from app.models import UserModel, BucketlistModel, BucketListItem

# create an instance of the flask_httpauth.HTTPBasicAuth class named auth
auth = HTTPTokenAuth()


#  declare the verify_user_password function that receives a name
# and a password as arguments
# function uses the @auth.verify_password decorator to make this function
# become the callback that Flask-HTTPAuth will use to verify the password
# for a specific user
@auth.verify_token
def verify_user_token(token):

    # verify token for the current user
    current_user = UserModel.verify_auth_token(token)
    if type(current_user) is not UserModel:
        return False

    else:
        g.user = current_user
        return True

class AuthRequiredResource(Resource):
    method_decorators = [auth.login_required]



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
        user.set_password(password)
        user.add(user)

        message = 'Congratulations {}!!!.'\
            'Your account has been successfully created.'\
            'Login to get started!'.format(first_name)
        return success_response(message=message)


class UserLoginApi(Resource):
    """Contains the user login and functionalities"""
    def post(self):

        # get the login information
        user = request.get_json()

        #if no data provided
        if not user:
            return error_response(message='No input provided')

        # check if the input has validation errors
        validation_errors = get_user_login_schema.validate(user)

        # Return validation errors if available
        if validation_errors:
            return error_response(validation_errors=validation_errors)

        # Get data provided by the user
        email = user["email"].lower()
        password = user["password"]

        # Check if the email provided exists
        user_by_email = UserModel.query.filter_by(email=email).first()

        # Check if user email exists
        if not user_by_email:
            return error_response(message='The email provided does not exist' \
            ', kindly register')

        # check if email provided matches with the password which exists
        if user_by_email.check_password(password):
            token = user_by_email.generate_auth_token()
            print(token)

            return jsonify(status=200, message="Login successful! Your token is "+str(token, 'utf-8'))
        else:
            return error_response(message="Either email or password"\
                                  " is incorrect")

class BucketlistsApi(AuthRequiredResource):
    """
    A function that creates a new bucket list and lists all the
    created bucket lists
    """
    def post(self):
        """A function that creates a new bucketlist"""
        new_bucketlist = request.get_json()

        # Check if there is any data provided by the user
        if not new_bucketlist:
            return error_response(message='No input provided')

        # check for validation errors
        validation_errors = get_bucketlist_schema.validate(new_bucketlist)

        #if there are validation errors
        if validation_errors:
            return error_response(validation_errors=validation_errors)



class BucketlistApi(Resource):
    """Contains all bucketlists functionalities"""
    pass


class BucketlistItemApi(Resource):
    """Contains bucketlist item functionalities"""
    pass


class BucketlistItemsApi(Resource):
    """Contains bucketlist items functionalities"""
    pass
