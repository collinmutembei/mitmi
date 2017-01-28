import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(object):
    """Main configuration class"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
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
    if os.getenv('TRAVIS_BUILD', None):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
