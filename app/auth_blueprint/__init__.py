from flask import Blueprint
#from app.common_functions import token_required
#create a blueprint object and initialize it with a name
auth = Blueprint('auth', __name__)

from . import views
