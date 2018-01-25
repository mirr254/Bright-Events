#!flask/bin/python

from flask import Flask, jsonify,abort,request,session, render_template
from flask import make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import createApp
from app.common_functions import token_required
from . import models
from . import auth
from app import db

import re
import jwt
import datetime
import uuid


#variables
app = createApp('development')

""" HANDLE USER ACTIVITIES"""


#error handlers for custom errors
@auth.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#view api docs in heroku
@auth.route('/')
def index():
	return render_template('documentation.html') 


# register user
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if email is None: #email and password must be included
        return jsonify({"Hey":"Email must be included"}),403
    if username is None: #password must be included
        return jsonify({"Hey":"Username must be included"}),403
    if password is None: #password must be included
        return jsonify({"Hey":"Password must be included"}),403
    if len(password) < 8:
        return jsonify({'Sorry', 'Password lenth must be more than 8 characters'}),403
    #check correct emai
    bad_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)    
    if bad_email == None:
       return jsonify({"Bad Email":"Please provide a valid email"})   

    #check if email already exists
    if models.User.query.filter_by(email = email).first() is not None:
        return jsonify({"Error": "Email already taken"})

    #test username
    if models.User.query.filter_by(username = username).first() is not None:
        return jsonify({"Error": "Username already taken"})

    hashed_pass = generate_password_hash(password, method='pbkdf2:sha256')
    user = models.User(username = username, email=email, public_id=str(uuid.uuid4()), password_hash = hashed_pass)   
    user.save()
    
    return jsonify({'Successful': 'User registered successfully. You can now log in'}),201

#login user
@auth.route('/api/v1/auth/login')
def login():    
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})    
    user = models.User.query.filter_by(username=auth.username).first()
    
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

    #check password
    if check_password_hash(user.password_hash, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, createApp('development').config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')}),200

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
   
#edit and password
@auth.route('/api/v1/auth/reset-password/<string:email>', methods=['PUT'])
def reset_password(email):
    user = models.User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'Not found':'Email not found'}),404
    password = str(request.json.get('password', ''))
    hashed_pass = generate_password_hash(password)
    user.password_hash = hashed_pass
    user.save()
    return jsonify({'Success':'Password reset success'}),201

#logout
@auth.route('/api/v1/auth/logout')
@token_required
def logout(logged_in_user):
    return jsonify({"Logged out ": logged_in_user.public_id})

