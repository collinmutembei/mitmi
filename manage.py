import unittest

from flask_script import Manager

from api.app import app

manager = Manager(app)


# custom script command to run unit tests
@manager.command
def test():
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_suite = test_loader.discover('tests')
    test_runner.run(test_suite)


if __name__ == "__main__":
    manager.run()
