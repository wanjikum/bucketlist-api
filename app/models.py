from app import db


class UserModel(db.Model):
    """Defines the user table"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        """user model constructor"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        """returning a printable version for the object"""
        return "<UserModel: {} {}>".format(self.first_name, self.last_name)


class BucketlistModel(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    items = db.relationship("bucketlistitem", backref="bucketlists",
                            cascade='all, delete-orphan', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=False)

    # def __init__(self, name):
    #     """initialize with name."""
    #     self.name = name
    #
    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # @staticmethod
    # def get_all():
    #     return Bucketlist.query.all()
    #
    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #
    # def __repr__(self):
    #     return "<BucketlistModel: {}>".format(self.name)


class BucketListItem(db.Model):
    """Define the bucketlist  items table"""
    __tablename__ = "bucketlistitems"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean(), default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
