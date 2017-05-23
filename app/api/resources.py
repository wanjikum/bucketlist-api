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

            return jsonify(status=200,
                           message="Login successful!" \
                           " Your token is "+str(token, 'utf-8'))
        else:
            return error_response(message="Either email or password"\
                                  " is incorrect")

class BucketlistsApi(AuthRequiredResource):
    """
    A function that creates a new bucket list and lists all the
    created bucket lists
    """

    def get(self):
        """Lists all the created bucket lists"""
        # Get the current user
        current_user = g.user.id
        # print('name is', g.user.first_name, 'id is', g.user.id)

        # Query all the bucketlists available
        # Returns an array of bucketlists
        bucketlists = BucketlistModel.query.filter_by(created_by=current_user).all()
        # print( 'this is my', bucketlists)

        # if no bucketlists available
        if not bucketlists:
            return success_response(message='There are no bucketlists '\
                                    'available')

        # if available
        # serialize obj to JSON formated str
        bucketlists = [get_bucketlist_schema.dump(bucketlist).data \
                       for bucketlist in bucketlists]
        return bucketlists


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

        # Get the name of the new bucketlist item
        name =new_bucketlist["name"]
        current_user = g.user.id

        # Check if the bucketlist item exists
        existing_bucketlist = BucketlistModel.query.filter_by(name=name,
        created_by=current_user).first()

        # if it exists throw an error message that it can't be recreated
        if existing_bucketlist:
            return error_response(status=409, error='Conflict',
                message='Bucket list {} already exists!'.format(name))

        # Add it to the database
        new_bucket_list = BucketlistModel(name=name, created_by=current_user)
        new_bucket_list.add(new_bucket_list)

        # Return a success message
        return success_response(message='Bucket list {} created ' \
                                'successfully!'.format(name), status=201)

    def delete(self):
        """Deletes all the bucket lists available"""
        # Get the current user
        current_user = g.user.id
        print('name is', g.user.first_name, 'id is', g.user.id)

        # Query all the bucketlists available
        # Returns an array of bucketlists
        bucketlists = BucketlistModel.query.filter_by(created_by=current_user).all()
        # print( 'this is my', bucketlists)

        # if no bucketlists available
        if not bucketlists:
            return success_response(message='There are no bucketlists '\
                                    'available. None has been deleted',
                                    status=200)

        # if available delete all bucketlists
        bucketlist = [bucketlist.delete() for bucketlist in bucketlists]
        return success_response(message='Bucketlists deleted '\
                                'successfully!', status=200)


class BucketlistApi(AuthRequiredResource):
    """
    A class that contains functionalities that gets single bucket list,
    Updates a bucket list and deletes single bucket list
    """
    def get(self):
        """A function that gets single bucket list"""
        return "I am get"

    def put(self):
        """A function that Updates a bucket list"""
        return "I am updating"

    def delete(self):
        """A function that deletes single bucket list"""
        return "I am deleting"


class BucketlistItemApi(Resource):
    """Contains bucketlist item functionalities"""
    pass


class BucketlistItemsApi(Resource):
    """Contains bucketlist items functionalities"""
    pass
