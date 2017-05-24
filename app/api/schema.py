# JSON is a format that encodes objects in a string.
# Serialization means to convert an object(dump) into that string, and
# deserialization is its inverse operation.
# add url field, bucketlistItem edit, get_many_bucketlists

from marshmallow import Schema, fields, validate
from flask import url_for


class UserRegisterSchema(Schema):
    """
    Schema to validate, serialize, and deserialize user registration data
    """
    first_name = fields.String(validate=[validate.Length(min=2, max=12)],
                               required=True,
                               error_messages={'required': 'Enter first name'})

    last_name = fields.String(validate=[validate.Length(min=2, max=12)],
                              required=True,
                              error_messages={'required': 'Enter Last name'})

    email = fields.Email(validate=[validate.Length(min=5, max=50)],
                         required=True,
                         error_messages={'required': 'Enter email'})
    password = fields.String(validate=[validate.Length(min=5)],
                             required=True,
                             error_messages={'required': 'Enter password'})
    verify_password = fields.String(
                                    validate=[validate.Length(min=5)],
                                    required=True,
                                    error_messages={'required': 'Enter password again'})


class UserLoginSchema(Schema):
    """
    Schema to validate, serialize, and deserialize user login data
    """
    email = fields.Email(validate=[validate.Length(max=50)],
                          required=True,
                          error_messages={'required': 'Enter email'})
    password = fields.String(validate=[validate.Length(min=5)],
                             required=True,
                             error_messages={'required': 'Enter password'})


class BucketListItemSchema(Schema):
    """
    Schema to validate, serialize, and deserialize buckelist data
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(min=2)],
                error_messages={'required': 'Enter a bucketlist item name'})
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    done = fields.Boolean()


class BucketlistSchema(Schema):
    """
    Schema to validate, serialize, and deserialize buckelist data
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(min=2)],
                         error_messages={
                             'required': 'Enter a bucketlist name'})
    items = fields.Nested(BucketListItemSchema, dump_only=True,
                          many=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    created_by = fields.Integer(attribute='users.id')
    url = fields.Method('get_url')

    @staticmethod
    def get_url(obj):
        return url_for('bucketlist', id=obj.id, _external=True)




get_user_register_schema = UserRegisterSchema()
get_user_login_schema = UserLoginSchema()
get_bucketlist_item_schema = BucketListItemSchema()
get_bucketlist_schema = BucketlistSchema(many=True)
