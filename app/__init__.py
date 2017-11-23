#!flask/bin/python
from flask import Flask

def createApp():

    app = Flask(__name__)
    app.secret_key = 'jhjghjsdvvhgggjhsdvvvvhgsd'

      #register the blueprints 
    
    from .auth_blueprint import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .events_blueprint import events as events_blueprint
    app.register_blueprint(events_blueprint)

    return app