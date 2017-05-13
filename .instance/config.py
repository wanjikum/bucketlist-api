import os


class Config(object):
    """
    Parent configuration class. It contains the general settings that
    all environments have by default
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development Environment."""
    DEBUG = True


class TestingConfig(Config):
    """
    Configurations for Testing Environment, with a separate test database.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production Environment."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
