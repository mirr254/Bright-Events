#!flask/bin/python
from flask import Flask
from instance.config import app_config

def createApp(conf_name):

    app = Flask(__name__)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

      #register the blueprints 
    
    from .auth_blueprint import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .events_blueprint import events as events_blueprint
    app.register_blueprint(events_blueprint)

    return app