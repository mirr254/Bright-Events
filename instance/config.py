import os

class Config(object):
    #parent configuration class
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    #configuration for development
    DEBUG = True

class ProductionCofig(Config):
    DEBUG = False

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db_brighter_events'
    DEBUG = True

#export the enviroment specified
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionCofig,
    'testing': TestingConfig
}