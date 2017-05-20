# JSON is a format that encodes objects in a string.
# Serialization means to convert an object(dump) into that string, and
# deserialization is its inverse operation.
# add url field

from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    """
    Schema to validate, serialize, and deserialize user registration data
    """
    first_name = fields.String(load_only=True,
                               validate=[validate.Length(max=12)],
                               required=True,
                               error_message={'required': 'Enter first name'})

    last_name = fields.String(load_only=True,
                              validate=[validate.Length(max=12)],
                              required=True,
                              error_message={'required': 'Enter Last name'})

    email = fields.String(load_only=True,
                          validate=[validate.Length(max=12)],
                          required=True,
                          error_message={'required': 'Enter email'})
    password = fields.String(load_only=True,
                             validate=[validate.Length(min=5)],
                             required=True,
                             error_message={'required': 'Enter password'})
    verify_password = fields.String(load_only=True,
                                    validate=[validate.Length(min=5)],
                                    required=True,
                                    error_message={'required': 'Enter password again'})


class UserLoginSchema(Schema):
    """
    Schema to validate, serialize, and deserialize user login data
    """
    email = fields.String(load_only=True,
                          validate=[validate.Length(max=12)],
                          required=True,
                          error_message={'required': 'Enter email'})
    password = fields.String(load_only=True,
                             validate=[validate.Length(min=5)],
                             required=True,
                             error_message={'required': 'Enter password'})


class BucketlistSchema(Schema):
    """
    Schema to validate, serialize, and deserialize buckelist data
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,
                         error_messages={
                             'required': 'Enter a bucketlist name'})
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    created_by = fields.Integer(attribute='users.id', dump_only=True)
