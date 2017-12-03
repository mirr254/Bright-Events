#!flask/bin/python
from flask import Flask
from instance.config import app_config
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def createApp(conf_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)   

      #register the blueprints 
    
    from .auth_blueprint import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .events_blueprint import events as events_blueprint
    app.register_blueprint(events_blueprint)

    return app