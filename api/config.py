import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(object):
    """Main configuration class"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET')


class ProductionConfig(Config):
    """configuration for production environment
    """
    DEBUG = False


class DevelopmentConfig(Config):
    """configuration for development environment
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """configuration for when testing"""
    TESTING = True
    # Prioritize SQLALCHEMY_DATABASE_URI if set by the environment,
    # then fall back to TEST_DB_URL (often used for local test setups).
    # If neither is found, it will inherit the value from the base Config class (which looks for DATABASE_URL).
    # Flask-SQLAlchemy will default to sqlite if no URI is ultimately found and issue a warning.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              os.environ.get('TEST_DB_URL')


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
