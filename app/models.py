from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
import os

Base = declarative_base()


class UserModel(Base):
    """Defines the user table"""
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=False, nullable=False)
    password = Column(String(30), nullable=False)


class BucketListModel(Base):
    """Defines the bucketlist table"""
    __tablename__ = "bucketlist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    items = relationship("bucketlistitem", backref="bucketlist")
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)


class BucketListItem(Base):
    """Define the bucketlist items table"""
    __tablename__ = "bucketlistitems"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    status = Column(Boolean(), default=False)

engine = create_engine('sqlite:///trial-bucketlist.db')
Base.metadata.create_all(engine)
