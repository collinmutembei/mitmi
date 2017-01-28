import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.app import app, db
from api.users.models import User
from api.events.models import Event

manager = Manager(app)
migrate = Migrate(app, db)

# db command
manager.add_command('db', MigrateCommand)


# custom script command to run unit tests
@manager.command
def test():
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_suite = test_loader.discover('tests')
    test_runner.run(test_suite)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Event=Event)


if __name__ == "__main__":
    manager.run()
