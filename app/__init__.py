from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config


# Control the SQLAlchemy integration for our Flask application
# provide access to all the SQLAlchemy functions and classes
db = SQLAlchemy()


# wraps the creation of a new Flask object
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # connect to the db
    db.init_app(app)

    return app
