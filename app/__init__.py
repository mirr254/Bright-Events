#!flask/bin/python
from flask import Flask, jsonify,abort,request
from flask import make_response

def createApp():

    app = Flask(__name__)
    app.secret_key = 'jhjghjsdvvhgggjhsdvvvvhgsd'

    users = []
    events = []

    @app.errorhandler(404)
    def not_found(error):
        return make_response( jsonify({'error': 'Resource not found'}), 404)

    @app.errorhandler(403)
    def bad_request(error):
        return make_response( jsonify({'error': 'Not allowed to leave that field blank'}))

    """ HANDLE USER ACTIVITIES"""

    # register user
    @app.route('/api/v1/auth/register', methods=['POST'])
    def register():
        if not request.json or not 'email' in request.json: #email must be included
            abort(403)
        if not request.json or not 'password' in request.json: #password must be included
            abort(403)
        user = {
            'id':len(users)+ 1,
            'email': request.json['email'],
            'username':request.json['username'],
            'password':request.json['password']
        }
        users.append(user)
        return jsonify({'task': user}),201


    """ HANDLE EVENTS ACTIVITIES """

    #create a new event
    @app.route('/api/v1/events', methods=['POST'])
    def addevent():
        if not request.json or not 'name' in request.json: #name must be included
            abort(403)
        if not request.json or not 'cost' in request.json: #cost must be included
            abort(403)
        event = {
            "eventid": len(events) + 1,
            "userid" : request.json['userid'],
            "name" : request.json['name'],
            "location" : request.json.get('location', ''),
            "description" : request.json.get('description', ''),
            "date": request.json.get('date',''),
            "cost" : request.json['cost']
        }
        events.append(event)
        return jsonify({'event': event}),201

    #get a specific event
    @app.route('/api/v1/events/<int:eventid>', methods=['GET'])
    def getEvent(eventid):
        event = [event for event in events if event['eventid'] == eventid]
        if len(event) == 0:
            abort(404)
        return jsonify({'event': event[0]})

    #get all events
    app.route('/api/v1/events')
    def getAllEvents():
        return jsonify({'events': events})



    return app