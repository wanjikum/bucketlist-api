from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


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

    return app
