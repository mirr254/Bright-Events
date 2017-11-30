import os

class Config(object):
    #parent configuration class
    DEBUG = False
    #CSRF_ENABLED = True
    SECRET = os.getenv('SECRETKEY')

class DevelopmentConfig(Config):
    #configuration for development
    DEBUG = True

class ProductionCofig(Config):
    DEBUG = False

#export the enviroment specified
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionCofig,
}