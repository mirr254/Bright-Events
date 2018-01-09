#!flask/bin/python
from flask import Flask, jsonify,abort,request,session
from flask import make_response
from app import createApp
from app.common_functions import token_required

from . import models
from . import events
import app.common_functions

""" HANDLE EVENTS ACTIVITIES """
#create a new event
@events.route('/api/v1/events', methods=['POST'])
@token_required
def add_event(logged_in_user):
    if not request.json or not 'name' in request.json: #name must be included
        return jsonify({"Hey":"Name must be included"}),403    
    if not request.json or not 'location' in request.json:
        return jsonify({"Hey":"Location must be included"}),403
    if not request.json or not 'category' in request.json:
        return jsonify({"Hey":"Category must be included"}),403
    
    cost = request.json.get('cost')
    name = request.json.get('name')
    location = request.json.get('location')
    category = request.json.get('category')
    date = request.json.get('date')
    description = request.json.get('description')
    public_userid =logged_in_user.public_id
        
    #check if cost is int
    if cost:
        if isinstance(cost, (int, float)) != True:
            return jsonify({"Error":"Cost must be numbers only"}),403

    event = models.Events(
                        name=name,
                        cost=cost,
                        user_public_id=public_userid,
                        location=location,
                        description=description,
                        date = date, #yyy-mm-dd
                        category=category )

    event.save()
    return jsonify({'Message': "Successfully created an event"}),201

#get a specific event
@events.route('/api/v1/events/<int:eventid>', methods=['GET'])
@token_required
def get_event(logged_in_user, eventid):
    # retrieve a event using its ID
    event = models.Events.query.filter_by(eventid=eventid).first()
    if len(event) == 0:
        return jsonify({'Not found':'Event with that id is not available'}),404
    response = jsonify({
                'id': event.eventid,
                'name': event.name,
                'cost': event.cost,
                'public_userid': event.user_public_id, #fetch user details using this ID
                'location': event.location,
                'description': event.description,
                'date' : event.date,
                'category': event.category,
                'date_created': event.date_created,
                'date_modified': event.date_modified
            })
    response.status_code = 200
    return response

#get all events
@events.route('/api/v1/events')
@token_required
def get_all_events(logged_in_user):
    events = models.Events.get_all()
    results = [] # a list of events
    for event in events:
        
        obj = {
            'id': event.eventid,
            'name': event.name,
            'cost': event.cost,
            'public_userid': event.user_public_id, #fetch user details using this ID
            'location': event.location,
            'description': event.description,
            'date' : event.date,
            'category': event.category,
            'date_created': event.date_created,
            'date_modified': event.date_modified
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response    

#deleting an event
@events.route('/api/v1/events/<int:eventid>', methods=['DELETE'])
@token_required
def delete_event(logged_in_user, eventid):
    # retrieve a event using its ID
    event = models.Events.query.filter_by(eventid=eventid).first()    
    if len(event) == 0:
        return jsonify({'Not found':'Event with that id is not available'}),404

    event.delete()
    return {
            "message": "Event {} deleted successfully".format(event.eventid) 
         }, 200

#edit and event
@events.route('/api/v1/events/<int:eventid>', methods=['PUT'])
def edit_event(eventid):
    event = models.Events.query.filter_by(eventid=eventid).first()
    if len(event) == 0:
        return jsonify({'Not found':'Event with that id is not available'}),404
    if not request.json:
        abort(403)
    
    event.name = request.json.get('name', event.name) #if no changes made let the initial remain
    event.description = request.json.get('description', event.description)
    event.location = request.json.get('location', event.location)
    event.category = request.json.get('category', event.category)
    event.save()

    response = jsonify({
                'id': event.eventid,
                    'name': event.name,
                    'cost': event.cost,
                    'public_userid': event.user_public_id, #fetch user details using this ID
                    'location': event.location,
                    'description': event.description,
                    'date' : event.date,
                    'category': event.category,
                    'date_created': event.date_created,
                    'date_modified': event.date_modified
            })
    response.status_code = 200
    return response

#search by name
@events.route('/api/v1/events/<string:location>', methods=['GET'])
@token_required
def searc_by_location(logged_in_user, location):
    event_searched = models.Events.query.filter_by(location=location)
    if event_searched:
        results = [] # a list of events
        for event in events:

            obj = {
                'id': event.eventid,
                'name': event.name,
                'cost': event.cost,
                'public_userid': event.user_public_id, #fetch user details using this ID
                'location': event.location,
                'description': event.description,
                'date' : event.date,
                'category': event.category,
                'date_created': event.date_created,
                'date_modified': event.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response    
    return jsonify({'Not found':'No event in that location'}),404

#rsvp or respond to an event (attending/not attending/maybe)
@events.route('/api/v1/events/<int:eventid>/rsvp', methods=['POST'])
@token_required
def rsvp_to_an_event(logged_in_user, eventid):
    if not request.json or not 'rsvp' in request.json: #name must be included
        return jsonify({'Error':'Please provide rsvp details'})

    rsvp = request.json['rsvp']
    if rsvp == 'attending' or rsvp =='not attending' or rsvp == 'maybe':
        #return jsonify({'Error':'Rsvp with attending, not attending or maybe'}),403
        event = models.Events.query.filter_by(eventid=eventid).first()
        if event:
            rsvp = models.Rsvp(
                eventid = eventid,
                userid = 2,#change to take of logged in user
                rsvp = request.json['rsvp']
            )
            rsvp.save()
            return jsonify({'Message': "Successfully responded to and event"}),201
        return jsonify({'Event not found':'No event with that id'}),404
    return jsonify({'Error':'rsvp must be either attending/maybe/not attending'}),403
