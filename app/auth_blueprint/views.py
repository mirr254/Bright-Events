#!flask/bin/python

from flask import Flask, jsonify,abort,request,session, render_template
from flask import make_response, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.utils.token import generate_email_confirmation_token, confirm_email_confirmation_token,generate_password_reset_token,confirm_password__reset_token
from app import createApp
from app.utils.common_functions import token_required, UserRegistrationValidations
from app.utils.email import send_email
from . import models
from . import auth
from app import db

import re
import jwt
import datetime
import uuid
import os


#variables
app = createApp( conf_name = os.getenv('APP_SETTINGS') )
_AUTH_BASE_URL = '/api/v1/auth/'

""" HANDLE USER ACTIVITIES"""


#error handlers for custom errors
@auth.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)

#handle 403 not allowed error
@auth.errorhandler(403)
def not_allowed(error):
    return make_response(jsonify({'message': 'You are not allowed to perfom that request'}), 403)

#error handlers for custom errors
@auth.errorhandler(500)
def server_error_found(error):
    return make_response(jsonify({'message': 'Server error. An error occured while processing your request. Please try again later'}), 500)

#view api docs in heroku
@auth.route('/')
def index():
	return render_template('documentation.html') 


# register user
@auth.route(_AUTH_BASE_URL+'register', methods=['POST'])
def register():
    username = request.json.get('username').strip()
    password =str(request.json.get('password')).strip()
    email = request.json.get('email')    

    #validation
    if email != None and username != None and password != '':        

        if len(password) < 8:
            return jsonify({'message': 'Password lenth must be more than 8 characters'}),400
        #check correct emai
        
        bad_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)    
        if bad_email == None:
            return jsonify({"message":"Please provide a valid email"}),400

        #check if email already exists
        if models.User.query.filter_by(email = email).first() is not None:
            return jsonify({"message": "Email already taken"}),400

        #test username
        if models.User.query.filter_by(username = username).first() is not None:
            return jsonify({"message": "Username already taken"}),400

        hashed_pass = generate_password_hash(password, method='pbkdf2:sha256')
        user = models.User(username = username, email=email, public_id=str(uuid.uuid4()), password_hash = hashed_pass)   
        user.save()

        #call mailer helper function
        mailer_helper(user.email, 'confirm_email')        
        return jsonify({'message': 'User registered successfully. Please check your mail to confirm email address'}),201
    return jsonify({'message':'email, username and password are required'}),400

#mailer helper function
def mailer_helper(email, _function):
    if (_function == 'confirm_email'):
        token = generate_email_confirmation_token(email)
        confirm_url = url_for( 'auth.confirm', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        send_email(email, 'Email confirmation', html)
    elif _function == 'reset_passwd':
        token = generate_password_reset_token(email) 
        password_reset_url = url_for('auth.reset_password_with_token',token = token,_external=True) 
        html = render_template(
            'password_reset_template.html',
            password_reset_url=password_reset_url)
 
        send_email(email,'Password Reset Requested', html)
    

#confirm email address
@auth.route(_AUTH_BASE_URL+'confirm/<token>')
def confirm(token):
    try:
        email = confirm_email_confirmation_token(token)
    except:
        return jsonify({'message':'invalid token. Email not confirmed'}),403
    user = models.User.query.filter_by(email=email).first_or_404()
    #check if user is already confirmed
    if user.email_confirmed:
        return jsonify({'message': 'user already confirmed'})
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.datetime.now()
        user.save()
        return jsonify({'message': 'Success. Email confirmed. Now you can login'})
    

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
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, 
                    app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')}),200

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

    #make sure user has confirmed email address before login
    # if user.email_confirmed:
    #     #check password
    #     if check_password_hash(user.password_hash, auth.password):
    #         token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, 
    #                     app.config['SECRET_KEY'])
    #         return jsonify({'token': token.decode('UTF-8')}),200

    #     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
    # return jsonify({'message': 'Please confirm your email before login in'}),401
   
#edit and password
@auth.route(_AUTH_BASE_URL+'reset-password/<string:email>', methods=['POST', 'GET'])
def reset_password(email):
    
    try:
        user = models.User.query.filter_by(email=email).first_or_404()
    except:
        return jsonify({'message':'Invalid Email address'}),400
    if user.email_confirmed:
        mailer_helper(email, 'reset_passwd')
        return jsonify({'message':'Email sent with reset password link'}),200
    else:
        return jsonify({'message':'Email must be confirmed before requesting password reset'}),401
    

#route to reset password with token 
@auth.route(_AUTH_BASE_URL+'reset-password/<token>', methods=['PUT'])
def reset_password_with_token(token):
    email = confirm_password__reset_token(token)
    
    if email != False:
        import pdb; pdb.set_trace()
        user = models.User.query.filter_by(email=email).first_or_404()
        password = str(request.json.get('password', ''))
        hashed_pass = generate_password_hash(password)
        user.password_hash = hashed_pass
        user.save()
        return jsonify({'message':'Password reset success'}),200
    else:
        return jsonify({'message': 'Token is invalid or expired'}),401

#logout
@auth.route('/api/v1/auth/logout')
@token_required
def logout(logged_in_user):
    token = request.headers['x-access-token']    
    blacklisted_tok = models.TokenBlackList(token)
    blacklisted_tok.save()
    return jsonify({'message': 'user '+logged_in_user.public_id+' logged out'}),200

