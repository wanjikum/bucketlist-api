import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import models


app = create_app(config_name='development')
with app.app_context():
    from app.models import db, UserModel, BucketlistModel, BucketListItem
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates database with tables"""
    os.system('createdb bucketlist_db')
    os.system('createdb test_bucketlist_db')
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Deletes database"""
    os.system('dropdb bucketlist_db')
    os.system('dropdb test_bucketlist_db')

if __name__ == '__main__':
    manager.run()
