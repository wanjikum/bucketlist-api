import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app.__init__ import db
secret_key = os.getenv('SECRET')

class AddUpdateDelete():
    """
    A class that declares the following three methods to add, update,
    and delete a resource through SQLAlchemy sessions
    """

    def add(self, resource):
        """
        This method receives the object to be added in the resource argument
        and calls the db.session.add method with the received resource as an
        argument to create the object in the underlying database. Finally,
        the code commits the session.
        """
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        """
        This method just commits the session to persist the changes made
        to the objects in the underlying database.
        """
        return db.session.commit()

    def delete(self, resource):
        """
         This method receives the object to be deleted in the resource argument
         and calls the db.session.delete method with the received resource as
         an argument to remove the object in the underlying database. Finally,
         the code commits the session.
         """
        db.session.delete(resource)
        return db.session.commit()


class UserModel(db.Model, AddUpdateDelete):
    """Defines the user table"""
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        """user model constructor"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def set_password(self, password):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration = 60000):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = UserModel.query.get(data['id'])
        return user

    def __repr__(self):
        """returning a printable version for the object"""
        return "<UserModel: {} {}>".format(self.first_name, self.last_name)


class BucketlistModel(db.Model, AddUpdateDelete):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    items = db.relationship("BucketListItem", backref="bucketlists",
                            cascade='all, delete-orphan', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=False)

    def __init__(self, name, created_by):
        """initialize with name."""
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<BucketlistModel: {}>".format(self.name)


class BucketListItem(db.Model, AddUpdateDelete):
    """Define the bucketlist  items table"""
    __tablename__ = "bucketlistitems"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean(), default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
