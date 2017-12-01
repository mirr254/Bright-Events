#!flask/bin/python
from flask import Flask, jsonify,abort,request,session
from flask import make_response
from . import models

from . import events
""" HANDLE EVENTS ACTIVITIES """

#create a new event

@events.route('/api/v1/events', methods=['POST'])
def addevent():
    if not request.json or not 'name' in request.json: #name must be included
        return jsonify({"Hey":"Name must be included"}),403
    if not request.json or not 'cost' in request.json: #cost must be included
        return jsonify({"Hey":"Cost must be included"}),403
    if not request.json or not 'location' in request.json:
        return jsonify({"Hey":"Location must be included"}),403
    if not request.json or not 'category' in request.json:
        return jsonify({"Hey":"Category must be included"}),403
    event = {
        "eventid": models.Events.get_random_id(),
        "userid" : request.json['userid'],
        "name" : request.json.get('name'),
        "location" : request.json['location'],
        "description" : request.json.get('description', ''),
        "date": request.json.get('date',''),
        "cost" : request.json['cost']
    }
    models.Events.events_list.append(event)
    return jsonify({'event': event}),201

#get a specific event
@events.route('/api/v1/events/<int:eventid>', methods=['GET'])
def getEvent(eventid):
    event = [event for event in models.Events.events_list if event['eventid'] == eventid]
    if len(event) == 0:
        return jsonify({'Not found':'Event with that id is not available'}),404
    return jsonify({'event': event[0]})

#get all events
@events.route('/api/v1/events')
def getAllEvents():
    return jsonify({'events': models.Events.events_list})

#deleting an event
@events.route('/api/v1/events/<int:eventid>', methods=['DELETE'])
def deleteEvent(eventid):
    event = [event for event in models.Events.events_list if event['eventid'] == eventid]
    if len(event) == 0:
        return jsonify({'Not found':'Event with that id is not available'}),404
    models.Events.events_list.remove(event[0])
    return jsonify({'event': "Event deletion successful"})

#edit and event
@events.route('/api/v1/events/<int:eventid>', methods=['PUT'])
def editEvent(eventid):
    event = [event for event in models.Events.events_list if event['eventid'] == eventid]
    if len(event) == 0:
        return jsonify({'Not found':'Event with that id is not available'}),404
    if not request.json:
        abort(403)
    
    event[0]['name'] = request.json.get('name', event[0]['name']) #if no changes made let the initial remain
    event[0]['description'] = request.json.get('description', event[0]['description'])
    event[0]['location'] = request.json.get('location', event[0]['location'])
    event[0]['category'] = request.json.get('category', event[0]['category'])
    
    return jsonify({'event':event[0]})

#search by name
@events.route('/api/v1/events/<string:name>', methods=['GET'])
def searchByLocation(location):
    event_searched = [event for event in models.Events.events_list if event['name'] == location]
    if event_searched:
        return jsonify({'events': event_searched}),200
    return jsonify({'Not found':'No event with that id'}),404

#rsvp or respond to an event (attending/not attending/maybe)
@events.route('/api/v1/events/<int:eventid>/rsvp', methods=['POST'])
def rsvpToAnEvent(eventid):
    if not request.json or not 'rsvp' in request.json: #name must be included
        return jsonify({'Error':'Please provide rsvp details'})

    rsvp = request.json['rsvp']
    if rsvp == 'attending' or rsvp =='not attending' or rsvp == 'maybe':
        #return jsonify({'Error':'Rsvp with attending, not attending or maybe'}),403
        event = [event for event in models.Events.events_list if event['eventid'] == eventid]
        if event:
            rsvp_ = {
                "rsvp_id": models.Events.get_random_id(),
                "eventid": eventid,
                "userid": models.Events.get_random_id(), #to be changed after testing. take user id from session
                "rsvp": request.json['rsvp']
            }
            return jsonify({'rsvp status': rsvp_}),201
        return jsonify({'Event not found':'No event with that id'}),404
    return jsonify({'Error':'rsvp must be either attending/maybe/not attending'}),403
