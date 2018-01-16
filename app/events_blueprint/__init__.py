from flask import Blueprint

#create a blueprint object and initialize it with a name
events = Blueprint('events', __name__) 

from . import views