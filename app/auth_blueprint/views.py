#!flask/bin/python
import re
from flask import Flask, jsonify,abort,request,session, render_template
from flask import make_response, g
from flask_httpauth import HTTPBasicAuth
from . import models
from . import auth
from app import db

""" HANDLE USER ACTIVITIES"""

authenticate = HTTPBasicAuth()

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

    user = models.User(username = username, email =email)
    user.hash_password(password)
    user.save()
    
    return jsonify({'Successful': 'User registered successfully. You can now log in'}),201

@authenticate.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = models.User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user

    import pdb; pdb.set_trace() #debugger
    return True

#login user
@auth.route('/api/v1/auth/login')
@authenticate.login_required
def login():    
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
    #return jsonify({'Welcome':'Login Okay'}),200
   


#edit and password

@auth.route('/api/v1/auth/reset-password/<string:email>', methods=['PUT'])
def resetPassword(email):
    user = models.User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'Not found':'Email not found'}),404
    password = str(request.json.get('password', ''))
    user.hash_password(password)
    user.save()
    return jsonify({'Success':'Password reset success'}),200

#logout
@auth.route('/api/v1/auth/logout')
def logout():    
    return jsonify({"Success":"Log out okay"})

