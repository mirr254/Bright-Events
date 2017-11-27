#!flask/bin/python
from flask import Flask, jsonify,abort,request
from flask import make_response
from . import models

from . import auth

""" HANDLE USER ACTIVITIES"""

# register user
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    if not request.json or not 'email' in request.json: #email and password must be included
        abort(403)
    if not request.json or not 'password' in request.json: #password must be included
        abort(403)
    user = {
        'id':len(models.User.users_list)+ 1,
        'email': request.json['email'],
        'username':request.json['username'],
        'password':request.json['password']
    }
    models.User.users_list.append(user)
    return jsonify({'user': user}),201

#login user
@auth.route('/api/v1/auth/login', methods=['GET'])
def login(email, password):
    user = [user for user in models.User.users_list if user['email'] == email and user['password'] == password]
    if user:
        return jsonify({'task':user}),200
    abort(403)


#edit and event
@auth.route('/api/v1/auth/reset-password', methods=['PUT'])
def editEvent(email):
    user = [user for user in models.User.users_list if user['email'] == email]
    if len(user) == 0  and not request.json:
        abort(404)
    user[0]['email'] = request.json.get('email', user[0]['email'])
