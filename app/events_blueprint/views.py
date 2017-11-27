#!flask/bin/python
from flask import Flask, jsonify,abort,request
from flask import make_response
from . import models

from . import events
""" HANDLE EVENTS ACTIVITIES """

#create a new event

@events.route('/api/v1/events', methods=['POST'])
def addevent():
    if not request.json or not 'name' in request.json: #name must be included
        abort(403)
    if not request.json or not 'cost' in request.json: #cost must be included
        abort(403)
    if not request.json or not 'location' in request.json:
        abort(403)
    if not request.json or not 'category' in request.json:
        abort(403)
    event = {
        "eventid": models.Events.get_random_id(),
        #"userid" : request.json['userid'],
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
        abort(404)
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
        abort(404)
    models.Events.events_list.remove(event[0])
    return jsonify({'event': True})

#edit and event
@events.route('/api/v1/events/<int:eventid>', methods=['PUT'])
def editEvent(eventid):
    event = [event for event in models.Events.events_list if event['eventid'] == eventid]
    if len(event) == 0:
        abort(404)
    if not request.json:
        abort(403)
    # if 'name' in request.json and type(request.json['name']) != string:
    #     abort(400) #bad request
    # if 'description' in request.json and type(request.json['description']) != Unicode:
    #     abort(400) #bad request
    # if 'location' in request.json and type(request.json['location']) != Unicode:
    #     abort(400) #bad request
    # if 'category' in request.json and type(request.json['category']) != Unicode:
    #     abort(400) #bad request
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
        return jsonify({'events', event_searched})
    abort(404)