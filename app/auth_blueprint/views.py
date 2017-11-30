#!flask/bin/python
from flask import Flask, jsonify,abort,request,session
from flask import make_response, g
from . import models

from . import auth

""" HANDLE USER ACTIVITIES"""

#error handlers for custom errors
@auth.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Resource Already exist '}), 404)

@auth.errorhandler(403)
def forbiden(error):
    return make_response(jsonify({'error': 'Please dont leave some fields blank'}), 404)
# register user
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    if not request.json or not 'email' in request.json: #email and password must be included
        abort(403)
    if not request.json or not 'password' in request.json: #password must be included
        abort(403)
    #check if email exists
    # user = [user for user in models.User.users_list if user['email'] == request.json['email']]
    # if user:
    #     abort(400)
    
    #check if username exists
    # user = [user for user in models.User.users_list if user['username'] == request.json['username']]
    # if user:
    #     abort(400)
    #register user
    user = {
        'id':len(models.User.users_list)+ 1,
        'email': request.json['email'],
        'username':request.json['username'],
        'password':request.json['password']
    }
    models.User.users_list.append(user)
    return jsonify({'user': user}),201

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
        
        return jsonify({'user':user}),200
    abort(404)


#edit and password

@auth.route('/api/v1/auth/reset-password/<string:email>', methods=['PUT'])
def resetPassword(email):
    user = [user for user in models.User.users_list if user['email'] == email]
    if not user:
        abort(404)
    user[0]['password'] = request.json.get('password', user[0]['password'])
    return jsonify({'user':user}),200
