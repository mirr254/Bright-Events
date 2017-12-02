#!flask/bin/python
from flask import Flask, jsonify,abort,request,session, render_template
from flask import make_response, g
import re
from . import models
from . import auth

""" HANDLE USER ACTIVITIES"""

#error handlers for custom errors
@auth.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Resource Already exist '}), 403)

@auth.errorhandler(403)
def forbiden(error):
    return make_response(jsonify({'error': 'Please dont leave some fields blank'}), 403)

#view api docs in heroku
@auth.route('/')
def index():
	return render_template('documentation.html') 

# register user
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    if not request.json or not 'email' in request.json: #email and password must be included
        return jsonify({"Hey":"Email must be included"}),403
    if not request.json or not 'password' in request.json: #password must be included
        return jsonify({"Hey":"Password must be included"})
    #check correct emai
    bad_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', request.json['email'])    
    if bad_email == None:
       return jsonify({"Bad Email":"Please provide a valid email"})

    #check if email already exists
    user1 = [user for user in models.User.users_list if user['email'] == request.json['email']]
    if user1:
        return jsonify({"Error": "Email already taken"})

    #test username
    user1 = [user for user in models.User.users_list if user['email'] == request.json['username']]
    if user1:
        return jsonify({"Error": "Username already taken"})

    user = {
        'id':models.User.get_random_id(),
        'email': request.json['email'],
        'username':request.json['username'],
        'password':request.json['password']
    }
    models.User.users_list.append(user)
    return jsonify({'Successful': 'User registered successfully'}, user),201

#login user
@auth.route('/api/v1/auth/login', methods=['POST'])
def login():    
    if not request.json or not 'email' in request.json: #no email provided
        abort(403)
    
    email = request.json['email']
    password = request.json['password']
    
    user = [user for user in models.User.users_list if user['email'] == email and user['password'] == password]
    if user:
        session.email = user[0]['email']
        session.userid = user[0]['id']
        
        return jsonify({'Welcome':'Login Okay'}),200
    abort(404)


#edit and password

@auth.route('/api/v1/auth/reset-password/<string:email>', methods=['PUT'])
def resetPassword(email):
    user = [user for user in models.User.users_list if user['email'] == email]
    if not user:
        return jsonify({'Not found':'Email not found'}),404
    user[0]['password'] = request.json.get('password', user[0]['password'])
    return jsonify({'Success':'Password reset success'}),200

#logout
@auth.route('/api/v1/auth/logout')
def logout():
    session['email'] = None
    session['userid'] = None
    return jsonify({"Success":"Log out okay"})

