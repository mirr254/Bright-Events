from functools import wraps
from flask import request, jsonify
from app.auth_blueprint import models
from app import createApp
import jwt

def check_blacklisted_token(token):
    """Helper function to check for blacklisted tokens.

    Args:
        token (str): Token from the x-access-token header.

    Returns:
        bool: True if user logged out (blacklisted token), False otherwise. 


    """
    token = models.TokenBlackList.query.filter_by(token=token).first()
    if token:
        return True
    return False
   
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        if check_blacklisted_token(token):
            return jsonify({'Session expired':'Please login again'}),403

        try: 
            data = jwt.decode(token, createApp('development').config['SECRET_KEY'])
            logged_in_user = models.User.query.filter_by(public_id=data['public_id']).first()
        except Exception:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(logged_in_user, *args, **kwargs)

    return decorated