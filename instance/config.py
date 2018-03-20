import os

class Config(object):
    #parent configuration class
    DEBUG = False
    CSRF_ENABLED = True
    POSTS_PER_PAGE = 4
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_RESET_SALT = os.getenv('SECURITY_PASSWORD_RESET_SALT')

    # mail settings
    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'sammysteppa90@gmail.com'

class DevelopmentConfig(Config):
    #configuration for development
    DEBUG = True

class ProductionCofig(Config):
    DEBUG = False

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db_brighter_events'
    DEBUG = False

#export the enviroment specified
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionCofig,
    'testing': TestingConfig
}