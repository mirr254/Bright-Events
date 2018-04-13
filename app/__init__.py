#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from instance.config import app_config
from flask_cors import CORS
from flask_mail import Mail
from flask_heroku import Heroku


db = SQLAlchemy()
mail = Mail()
heroku = Heroku()

def createApp(conf_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[conf_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    mail.init_app(app)
    heroku.init_app(app)
    CORS(app)


      #register the blueprints 
    
    from .auth_blueprint import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .events_blueprint import events as events_blueprint
    app.register_blueprint(events_blueprint)

    return app