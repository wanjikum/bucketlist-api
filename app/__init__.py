from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from app.api.resources import *


# Control the SQLAlchemy integration for our Flask application
# provide access to all the SQLAlchemy functions and classes
db = SQLAlchemy()

# wraps the creation of a new Flask object


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # initialize app on the SQLAlchemy instance
    db.init_app(app)

    api = Api(app)

    api.add_resource(UserRegisterApi, '/api/v1/auth/register',
                     endpoint='user_registration')
    api.add_resource(UserLoginApi, '/api/v1/auth/login',
                     endpoint='user_login')
    api.add_resource(BucketlistsApi, '/api/v1/bucketlists/',
                     endpoint='bucketlists')
    api.add_resource(BucketlistApi, '/api/v1/bucketlists/<int:id>',
                     endpoint='bucketlist')
    api.add_resource(BucketlistItemsApi, '/api/v1/bucketlists/<int:id>/items/',
                     endpoint='bucketlistitems')
    api.add_resource(BucketlistItemApi,
                     '/api/v1/bucketlists/<id>/items/<item_id>',
                     endpoint='bucketlistitem')
    return app
