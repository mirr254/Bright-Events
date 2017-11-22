#!flask/bin/python
from flask import Flask, jsonify,abort,request
from flask import make_response

def createApp():

    app = Flask(__name__)
    app.secret_key = 'jhjghjsdvvhgggjhsdvvvvhgsd'

    users = []

    @app.errorhandler(404)
    def not_found(error):
        return make_response( jsonify({'error': 'Resource not found'}), 404)

    """ HANDLE USER ACTIVITIES"""

    # register user
    @app.route('/api/v1/auth/register', methods=['POST'])
    def register():
        if not request.json or not 'email' in request.json: #email must be included
            abort(404)
        if not request.json or not 'password' in request.json: #password must be included
            abort(404)
        user = {
            'id':len(users)+ 1,
            'email': request.json['email'],
            'username':request.json['username'],
            'password':request.json['password']
        }
        users.append(user)
        return jsonify({'task': user}),201


    """ HANDLE EVENTS ACTIVITIES """

    return app