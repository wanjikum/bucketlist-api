# JSON is a format that encodes objects in a string.
# Serialization means to convert an object(dump) into that string, and
# deserialization is its inverse operation.

from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    """
    Schema to validate, serialize, and deserialize user registration data
    """
    first_name = fields.String(load_only=True,
                               validate=[validate.Length(max=12)],
                               required=True,
                               error_message='First name is required!')

    last_name = fields.String(load_only=True,
                              validate=[validate.Length(max=12)],
                              required=True,
                              error_message='Last name is required!')

    email = fields.String(load_only=True,
                          validate=[validate.Length(max=12)],
                          required=True,
                          error_message='Email is required!')
    password = fields.String(load_only=True,
                             validate=[validate.Length(min=5)],
                             required=True,
                             error_message='Password is required!')
    verify_password = fields.String(load_only=True,
                                    validate=[validate.Length(min=5)],
                                    required=True,
                                    error_message='Password is required!')

    print('heeeey, goodwork!')
