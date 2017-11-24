#!flask/bin/python
from flask import Flask, jsonify,abort,request
from flask import make_response

from . import auth

""" HANDLE USER ACTIVITIES"""

users_list = []

# register user
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    if not request.json or not 'email' in request.json: #email and password must be included
        abort(403)
    if not request.json or not 'password' in request.json: #password must be included
        abort(403)
    user = {
        'id':len(users_list)+ 1,
        'email': request.json['email'],
        'username':request.json['username'],
        'password':request.json['password']
    }
    users_list.append(user)
    return jsonify({'task': user}),201

#edit and event
@auth.route('/api/v1/auth/reset-password', methods=['PUT'])
def editEvent(email):
    user = [event for event in users_list if event['email'] == email]
    if len(user) == 0  and not request.json:
        abort(404)
    user[0]['email'] = request.json.get('email', user[0]['email'])
