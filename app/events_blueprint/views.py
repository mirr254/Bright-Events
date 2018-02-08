#!flask/bin/python
import os
from flask import Flask, jsonify,abort,request,session
from flask import make_response
from app import createApp
from app.common_scripts.common_functions import token_required
from app.auth_blueprint import models as users_models

from . import models
from . import events

#script global variables
app = createApp(os.getenv('APP_SETTINGS'))

"""Helper function to check for blacklisted tokens"""

def check_blacklisted_token(token):

    token = users_models.TokenBlackList.query.filter_by(token=token).first()
    if token:
        return True
    return False

""" HANDLE EVENTS ACTIVITIES """
#create a new event
@events.route('/api/v1/events', methods=['POST'])
@token_required
def add_event(logged_in_user):    
     #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403

    if not request.json or not 'name' in request.json: #name must be included
        return jsonify({"message":"Name must be included"}),403    
    if not request.json or not 'location' in request.json:
        return jsonify({"message":"Location must be included"}),403
    if not request.json or not 'category' in request.json:
        return jsonify({"message":"Category must be included"}),403
   
    #check if cost is int
    if request.json.get('cost'):
        if isinstance(request.json.get('cost'), (int, float)) != True:
            return jsonify({"message":"Cost must be numbers only"}),403

    event = models.Events(
                        name= request.json.get('name'),
                        cost= request.json.get('cost'),
                        user_public_id= logged_in_user.public_id,
                        location= request.json.get('location'),
                        description= request.json.get('description'),
                        date = request.json.get('date'), #yyy-mm-dd
                        category= request.json.get('category') )

    event.save()
    return jsonify({'message': "Successfully created an event"}),201

#get a specific event
@events.route('/api/v1/events/<int:eventid>', methods=['GET'])
@token_required
def get_event(logged_in_user, eventid):
    # retrieve a event using its ID
    event = models.Events.query.filter_by(eventid=eventid).first()
    if not event:
        return jsonify({'Not found':'Event with that id is not available'}),404
    response = return_response(event)
    response.status_code = 200
    return response


#get all events
@events.route('/api/v1/events')
@token_required
def get_all_events(logged_in_user):
    #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403
    page = request.args.get('page',1,type=int )
    events = models.Events.query.paginate(page, app.config['POSTS_PER_PAGE'], False).items
    results = [] # a list of events
    for event in events:        
        obj = return_obj(event)
        results.append(obj)

    response = jsonify(results)
    response.status_code = 200
    return response    

#deleting an event
@events.route('/api/v1/events/<int:eventid>', methods=['DELETE'])
@token_required
def delete_event(logged_in_user, eventid):
     #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403
    # retrieve a event using its ID
    event = models.Events.query.filter_by(eventid=eventid).first()
    if not event:
        return jsonify({'Not found':'Event with that id is not available'}),404

    if event.user_public_id != logged_in_user.public_id:
        return jsonify({'Authorization error':'You can only delete your own event'}),401

    event.delete()
    return jsonify({"message": "Event {} deleted successfully".format(event.eventid)}), 200

#edit and event
@events.route('/api/v1/events/<int:eventid>', methods=['PUT'])
@token_required
def edit_event(logged_in_user,eventid):
     #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403

    event = models.Events.query.filter_by(eventid=eventid).first()
    if not event:
        return jsonify({'Not found':'Event with that id is not available'}),404
   
    if event.user_public_id != logged_in_user.public_id:
        return jsonify({'Authorization error':'You can only update your own event'}), 401

    event.name = request.json.get('name', event.name) #if no changes made let the initial remain
    event.description = request.json.get('description', event.description)
    event.location = request.json.get('location', event.location)
    event.category = request.json.get('category', event.category)
    event.cost = request.json.get('cost', event.cost)
    event.save()

    response = return_response(event)
    response.status_code = 201
    return response

#search by name
@events.route('/api/v1/events/<string:location>', methods=['GET'])
@token_required
def searc_by_location(logged_in_user, location):
     #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403

    event_searched = models.Events.query.filter_by(location=location)
    if event_searched:
        results = [] # a list of events
        for event in event_searched:

            obj =return_obj(event)

            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response    
    return jsonify({'Not found':'No event in that location'}),404

def return_obj(event):
    obj =  {
                'name': event.name,
                'cost': event.cost,
                'public_userid': event.user_public_id, #fetch user details using this ID
                'location': event.location,
                'description': event.description,
                'date' : event.date,
                'category': event.category,
                'date_created': event.date_created                
            }
    return obj

def return_response(event):
    response = jsonify({                
                'name': event.name,
                'cost': event.cost,                
                'location': event.location,
                'description': event.description,
                'date' : event.date,
                'category': event.category,
                'date_created': event.date_created               
            })
    return response


#rsvp or respond to an event (attending/not attending/maybe)
@events.route('/api/v1/events/<int:eventid>/rsvp', methods=['POST'])
@token_required
def rsvp_to_an_event(logged_in_user, eventid):
     #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403

    if not request.json or not 'rsvp' in request.json: #name must be included
        return jsonify({'Error':'Please provide rsvp details'})

    rsvp = request.json['rsvp']
    if rsvp == 'attending' or rsvp =='not attending' or rsvp == 'maybe':
        #return jsonify({'Error':'Rsvp with attending, not attending or maybe'}),403
        event = models.Events.query.filter_by(eventid=eventid).first()
        if event:
            rsvp = models.Rsvp(
                eventid = eventid,
                rsvp = request.json['rsvp'],
                user_pub_id = logged_in_user.public_id 
            )
            rsvp.save()
            response = jsonify({
                'eventid':eventid,
                'Message': 'Successfully responded to and event'
            })
            return response,201
        return jsonify({'Event not found':'No event with that id'}),404
    return jsonify({'Error':'rsvp must be either attending/maybe/not attending'}),403

@events.route('/api/v1/events/<int:eventid>/guests', methods=['GET'])
@token_required
def list_event_guests(token_required,eventid):
     #check if token is blacklisted
    token = request.headers['x-access-token']
    if check_blacklisted_token(token) == True:
        return jsonify({'Session expired':'Please login again'}),403

    #check if event exists
    event = models.Events.query.filter_by(eventid=eventid).first()
    if event:
        dic_of_users_rsvp = {}
        rsvps = models.Rsvp.query.filter_by(eventid = eventid)
        #if no rsvps
        if not rsvps:
            response = jsonify({'Message':'This event has no guests yet.'})
            response.status_code = 404
            return response
        for resp in rsvps:
            user = users_models.User.query.filter_by( public_id = resp.user_pub_id).first()
            
            dic_of_users_rsvp.update({user.username : resp.rsvp})

        response = jsonify(dic_of_users_rsvp)
        response.status_code = 200

        return response