import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models


app = create_app(config_name=os.getenv('APP_SETTINGS'))
with app.app_context():
    from app.models import UserModel, BucketlistModel, BucketListItem
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
# db.create_all()
# db.session.commit()


@manager.command
def create_db():
    """Creates database with tables"""
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Deletes database"""
    try:
        os.remove("app/bucketlist.db")
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    manager.run()
