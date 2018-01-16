from functools import wraps
from flask import request, jsonify
from app.auth_blueprint import models
from app import createApp

import jwt

#variables
   

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, createApp('development').config['SECRET_KEY'])
            logged_in_user = models.User.query.filter_by(public_id=data['public_id']).first()
        except Exception:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(logged_in_user, *args, **kwargs)

    return decorated