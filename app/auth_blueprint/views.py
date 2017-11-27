#!flask/bin/python
from flask import Flask, jsonify,abort,request
from flask import make_response, g
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
@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = [user for user in models.User.users_list if user['email'] == email and user['password'] == password]
    if user:
        return jsonify({'task':user}),200
    abort(404)


#edit and password

# @auth.route('/api/v1/auth/reset-password/<string:email>', methods=['PUT'])
# def resetPassword(password):
#     user = [user for user in models.User.users_list if user['email'] == 'him@']
#     if len(user) == 0  and not request.json:
#         abort(404)
#     user[0]['password'] = request.json.get('password', user[0]['password'])
