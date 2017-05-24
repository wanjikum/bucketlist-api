import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from flask import request, g, url_for, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api.schema import (get_user_register_schema,
                            get_user_login_schema,
                            get_bucketlist_schema,
                            get_bucketlist_item_schema,
                            get_bucketlists_schema,
                            get_edit_bucketlist_item_schema)
from app.api.responses import error_response, success_response
from app.models import UserModel, BucketlistModel, BucketListItem

# create an instance of the flask_httpauth.HTTPBasicAuth class named auth
auth = HTTPTokenAuth()


#  declare the verify_user_token that verifies token
# it uses the @auth.verify_token decorator to make this function
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

        # check if both passwords given are similar
        password1 = new_user["password"]
        password2 = new_user["verify_password"]

        # if passwords not equal return an error response
        if password1 != password2:
            return error_response(message='Password mismatch')

        # get data provided by the user
        first_name = new_user["first_name"].title()
        last_name = new_user["last_name"].title()
        email = new_user["email"].lower()
        password = new_user["password"]

        # reject adding a new_user if he registers with an existing email
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

        # if no data provided
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
            return error_response(message='The email provided does not exist'
                                  ', kindly register')

        # check if email provided matches with the password which exists
        if user_by_email.check_password(password):
            token = user_by_email.generate_auth_token()
            print(token)

            return jsonify(status=200,
                           message="Login successful!"
                           " Your token is " + str(token, 'utf-8'))
        else:
            return error_response(message="Either email or password"
                                  " is incorrect")


class BucketlistsApi(AuthRequiredResource):
    """
    A function that creates a new bucket list and lists all the
    created bucket lists
    """

    def get(self):
        """Lists all the created bucket lists"""

        # obtain pagination arguments from the URL's query string
        page = request.args.get('page', 1, type=int)
        max_limit = 100
        request_limit = request.args.get('limit', 20, type=int)
        limit = min(request_limit, max_limit)
        search_term = request.args.get('q', None, type=str)

        # Get the current user
        current_user = g.user.id

        # Query all the bucketlists available
        # Returns an array of bucketlists

        # if there are is no search term
        if not search_term:
            paginated_bucketlists = BucketlistModel.query.filter_by(
                created_by=current_user).paginate(page, limit, error_out=True)
            print(paginated_bucketlists)

        # search bucketlists if search url argument exists
        else:
            paginated_bucketlists = BucketlistModel.query.filter_by(
                created_by=current_user).filter(BucketlistModel.name.ilike(
                    '%' + search_term + '%')).paginate(page, limit,
                                                       error_out=True)
            print(paginated_bucketlists)

        # return 404 if the user doesn't have bucketlists
        if not paginated_bucketlists.items:
            return error_response(error='Not found', status=404,
                                  message='No bucketlists available')

          # obtain prev_url and next_url
        if paginated_bucketlists.has_prev:
            previous_url = url_for(request.endpoint,
                                   q=search_term, limit=limit,
                                   page=paginated_bucketlists.prev_num,
                                   _external=True)

        else:
            previous_url = None

        if paginated_bucketlists.has_next:
            next_url = url_for(request.endpoint,
                               q=search_term, limit=limit,
                               page=paginated_bucketlists.next_num,
                               _external=True)
        else:
            next_url = None

        # obtain first and last urls
        first_url = url_for(request.endpoint, q=search_term, limit=limit,
                            page=1, _external=True)

        last_url = url_for(request.endpoint, q=search_term,
                           limit=limit, page=paginated_bucketlists.pages,
                           _external=True)

        # serialize bucketlist objects
        result = get_bucketlists_schema.dump(paginated_bucketlists.items)

        return jsonify({
            'page': page,
            'limit': limit,
            'pages': paginated_bucketlists.pages,
            'prev_url': previous_url,
            'next_url': next_url,
            'first_url': first_url,
            'last_url': last_url,
            'total': paginated_bucketlists.total,
            'bucketlist(s)': result.data})

    def post(self):
        """A function that creates a new bucketlist"""
        new_bucketlist = request.get_json()

        # Check if there is any data provided by the user
        if not new_bucketlist:
            return error_response(message='No input provided')

        # check for validation errors
        validation_errors = get_bucketlist_schema.validate(new_bucketlist)

        # if there are validation errors
        if validation_errors:
            return error_response(validation_errors=validation_errors)

        # Get the name of the new bucketlist
        name = new_bucketlist["name"]
        current_user = g.user.id

        # Check if the bucketlist exists
        existing_bucketlist = BucketlistModel.query.filter_by(
            name=name, created_by=current_user).first()

        # if it exists throw an error message that it can't be recreated
        if existing_bucketlist:
            return error_response(status=409, error='Conflict',
                                  message='Bucket list {} already '
                                  'exists!'.format(name))

        # Add it to the database
        new_bucket_list = BucketlistModel(name=name, created_by=current_user)
        new_bucket_list.add(new_bucket_list)

        # Return a success message
        return success_response(
            message='Bucket list {} created successfully!'.format(name),
            status=201, added=get_bucketlist_schema.dump(new_bucket_list).data)

    def delete(self):
        """Deletes all the bucket lists available"""
        # Get the current user
        current_user = g.user.id

        # Query all the bucketlists available
        # Returns an array of bucketlists
        bucketlists = BucketlistModel.query.filter_by(
            created_by=current_user).all()

        # if no bucketlists available
        if not bucketlists:
            return success_response(message='There are no bucketlists '
                                    'available. None has been deleted',
                                    status=200)

        # if available delete all bucketlists
        bucketlist = [bucketlist.delete(
            bucketlist) for bucketlist in bucketlists]
        return success_response(message='Bucket lists deleted '
                                'successfully!', status=200)


class BucketlistApi(AuthRequiredResource):
    """
    A class that contains functionalities that gets single bucket list,
    Updates a bucket list and deletes single bucket list
    """

    def get(self, id):
        """A function that gets single bucket list"""

        # Get the current user
        current_user = g.user.id

        # Query the bucket list with the id
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        print(bucketlist)

        # There are no bucketlists available
        if not bucketlist:
            return error_response(status=404,
                                  message="The bucketlist does not exist",
                                  error="Page not found")

        return get_bucketlist_schema.dump(bucketlist).data

    def put(self, id):
        """A function that Updates a bucket list"""

        # Get the current user
        current_user = g.user.id

        # Query the bucket list with the id
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        # There are no bucketlists available
        if not bucketlist:
            return error_response(status=404,
                                  message="The bucketlist does not exist",
                                  error="Page not found")

        # Check the new bucketlist update
        bucketlist_update = request.get_json()

        # If there is no data available
        if not bucketlist_update:
            return error_response(message='No input provided')

        # Check for validation errors
        validation_errors = get_bucketlist_schema.validate(bucketlist_update)

        # If there are validation errors
        if validation_errors:
            return error_response(validation_errors=validation_errors)

        # Update bucketlist, pick the new name
        bucketlist.name = bucketlist_update['name']

        # update it to the db
        bucketlist.update()

        # return a success message
        return success_response(
            status=200, message="Updated successfully!",
            modified=get_bucketlist_schema.dump(bucketlist).data)

    def delete(self, id):
        """A function that deletes single bucket list"""
        # Get the current user
        current_user = g.user.id

        # Query the bucket list with the id
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        # There are no bucketlists available
        if not bucketlist:
            return error_response(status=404,
                                  message="The bucketlist does not exist",
                                  error="Page not found")

        # Delete bucketlist
        bucketlist.delete(bucketlist)
        return success_response(status=200, message="The bucketlist has been"
                                " deleted successfully")


class BucketlistItemsApi(AuthRequiredResource):
    """ A class that creates a new item in bucket list """

    def post(self, id):
        """
        A function that creates a new item in bucket list
        """
        # Get the current user
        current_user = g.user.id

        # Query the bucket list to find the bucketlist owner
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        if not bucketlist:
            return error_response(
                status=404, error="Not found",
                message="The bucketlist with id {} does not exist!".format(id))

        new_bucketlist_item = request.get_json()

        # Check if there is any data provided by the user
        if not new_bucketlist_item:
            return error_response(message='No input provided')

        # check for validation errors
        validation_errors = get_bucketlist_item_schema.validate(
            new_bucketlist_item)

        # if there are validation errors
        if validation_errors:
            return error_response(validation_errors=validation_errors)

        # Get the name of the new bucketlist
        name = new_bucketlist_item["name"]

        # Check if the bucketlist exists
        existing_bucketlist_item = BucketListItem.query.filter_by(
            name=name, bucketlist_id=id).first()

        # if it exists throw an error message that it can't be recreated
        if existing_bucketlist_item:
            return error_response(
                status=409, error='Conflict',
                message='Bucket list {} already exists!'.format(name))

        # Add it to the database
        new_bucketlist_item = BucketListItem(name=name, bucketlist_id=id)
        new_bucketlist_item.add(new_bucketlist_item)

        # Return a success message
        return success_response(
            message='Bucket list item {} created successfully!'.format(name),
            status=201,
            added=get_bucketlist_item_schema.dump(new_bucketlist_item).data)


class BucketlistItemApi(AuthRequiredResource):
    """
    Updates a bucket list item sand deletes an item in a bucket list
    """

    def put(self, id, item_id):
        """Updates a bucket list item"""

        # Get the current user
        current_user = g.user.id

        # Query the bucket list to find the bucketlist owner
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        # if not found
        if not bucketlist:
            return error_response(
                status=404, error="Not found",
                message="The bucketlist with id {} does not exist!".format(id))

        # check if the bucketlist item is in the bucketlist
        existing_bucketlist_item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_id=id).first()

        # if it does not
        if not existing_bucketlist_item:
            return error_response(status=404, error="Not found",
                                  message="The bucketlist item with id {} does "
                                  "not exist!".format(item_id))
        new_bucketlist_item = request.get_json()

        # Check if there is any data provided by the user
        if not new_bucketlist_item:
            return error_response(message='No input provided')

        # check for validation errors
        validation_errors = get_edit_bucketlist_item_schema.validate(
            new_bucketlist_item)

        # if there are validation errors
        if validation_errors:
            return error_response(validation_errors=validation_errors)

        #

        # Get the name of the new bucketlist item
        existing_bucketlist_item.name = new_bucketlist_item["name"]
        existing_bucketlist_item.done = new_bucketlist_item["done"]

        # update it to the db
        existing_bucketlist_item.update()

        # return a success message
        return success_response(
            status=200, message="Updated successfully!",
            modified=get_bucketlist_item_schema.dump(
                existing_bucketlist_item).data)

    def get(self, id, item_id):
        """Updates a bucket list item"""
        # Get the current user
        current_user = g.user.id

        # Query the bucket list to find the bucketlist owner
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        # if not found
        if not bucketlist:
            return error_response(
                status=404, error="Not found",
                message="The bucketlist with id {} does not exist!".format(id))

        # check if the bucketlist item is in the bucketlist
        existing_bucketlist_item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_id=id).first()

        # if it does not
        if not existing_bucketlist_item:
            return error_response(status=404, error="Not found",
                                  message="The bucketlist item with id {} does "
                                  "not exist!".format(item_id))

        return get_bucketlist_item_schema.dump(existing_bucketlist_item).data

    def delete(self, id, item_id):
        """delete a bucket list item"""

        # Get the current user
        current_user = g.user.id

        # Query the bucket list to find the bucketlist owner
        bucketlist = BucketlistModel.query.filter_by(
            id=id, created_by=current_user).first()

        # if not found
        if not bucketlist:
            return error_response(
                status=404, error="Not found",
                message="The bucketlist with id {} does not exist!".format(id))

        # check if the bucketlist item is in the bucketlist
        existing_bucketlist_item = BucketListItem.query.filter_by(
            id=item_id, bucketlist_id=id).first()

        # if it does not
        if not existing_bucketlist_item:
            return error_response(status=404, error="Not found",
                                  message="The bucketlist item with id {} does "
                                  "not exist!".format(item_id))

        existing_bucketlist_item.delete(existing_bucketlist_item)
        return success_response(status=200, message="The bucketlist item {} "
                                "has been deleted successfully".format(item_id))
