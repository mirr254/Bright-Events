#!flask/bin/python
import os
from datetime import datetime
from flask import Flask, jsonify,abort,request,session
from flask import make_response
from app import createApp
from app.utils.common_functions import token_required
from app.auth_blueprint import models as users_models
from sqlalchemy import or_

from . import models
from . import events

#script global variables
app = createApp(os.getenv('APP_SETTINGS'))


#error handlers for custom errors
@events.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Page not found'}), 404)

#error handlers for custom errors
@events.errorhandler(500)
def server_error_found(error):
    return make_response(jsonify({'message': 'Server error. Its not you ,but us...'}), 500)



""" HANDLE EVENTS ACTIVITIES """
#create a new event
@events.route('/api/v1/events', methods=['POST'])
@token_required
def add_event(logged_in_user): 

    if not request.json or not 'name' in request.json or (request.json.get('name').strip() == ''): #name must be included
        return jsonify({"message":"Name must be included"}),403    
    if not request.json or not 'location' in request.json or (request.json.get('location').strip() == ''):
        return jsonify({"message":"Location must be included"}),403
    if not request.json or not 'category' in request.json or (request.json.get('category').strip() == ''):
        return jsonify({"message":"Category must be included"}),403
    if not request.json or not 'date' in request.json or (request.json.get('date').strip() == ''):
        return jsonify({"message":"Date must be included"}),403
   
    #check if cost is int
    if request.json.get('cost'):
        if isinstance(request.json.get('cost'), (int, float)) != True:
            return jsonify({"message":"Cost must be numbers only"}),403
    #check for dates
    user_input_date = datetime.strptime( request.json.get('date'), '%Y-%m-%d %H:%M')
    if user_input_date < datetime.now():
        return jsonify({'message': 'Event date cannnot be past'}),403

    #check for another event with same event name
    event = models.Events.query.filter( models.Events.name.ilike( request.json.get('name').strip()) ).first()   
    if event:
        user_input_date = datetime.strptime( request.json.get('date'), '%Y-%m-%d %H:%M')
        event_stored_date = datetime.strptime(event.date, '%Y-%m-%d %H:%M')           
        if ( event_stored_date.strftime('%Y-%m-%d %H:%M') == user_input_date.strftime('%Y-%m-%d %H:%M') ):                 
            return jsonify({'message': 'Events with same name should have different dates'}),403    

    event = models.Events(
                        name= request.json.get('name'),
                        cost= request.json.get('cost'),
                        user_public_id= logged_in_user.public_id,
                        location= request.json.get('location'),
                        description= request.json.get('description'),
                        date = request.json.get('date'), #"2016/11/06 16:30"
                        category= request.json.get('category') )

    event.save()
    return jsonify({'message': "Successfully created an event"}),201       
            
#get a specific event
@events.route('/api/v1/events/<int:eventid>', methods=['GET'])
@token_required
def get_event(logged_in_user, eventid):
    # retrieve a event using its ID
    event = models.Events.query.filter_by(eventid=eventid).first_or_404()
    if not event:
        return jsonify({'message':'Event with that id is not available'}),404
    response = return_response(event)
    response.status_code = 200
    return response

#get all events from a particular user
@events.route('/api/v1/events/user/<string:public_user_id>', methods=['GET'])
@token_required
def get_all_user_events(logged_in_user, public_user_id):
    #handle pagination 
    page = request.args.get('page',1,type=int )
    limit = request.args.get('limit',6,type=int) #defaults to 3 if user doesn't specify to limit
    #retrieve all events using public_user_id
    events = models.Events.query.filter_by(user_public_id=public_user_id).paginate(page, limit, True).items
    if not events:
        return jsonify({'message': 'You have not created any event. Once you do, it will appear here'})
    return return_event_results(events)


#get all events
@events.route('/api/v1/events')
def get_all_events():
#retrieve all the events any user can do this
    page = request.args.get('page',1,type=int )
    limit = request.args.get('limit',6,type=int) #defaults to 3 if user doesn't specify to limit
    location_filter = request.args.get('location', type=str)
    
    if location_filter:
        events = models.Events.query.filter(models.Events.location.ilike('%{}%'.format(location_filter)))
        return return_event_results(events)
    
    events = models.Events.query.paginate(page, limit, False).items
    return return_event_results(events)
  
def return_event_results(events):
    """helper function to return necessary events based on request args

    Args:
    events: event items from the query

    Returns:
        response: response with data 

    """ 
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
    # retrieve a event using its ID
    event = models.Events.query.filter_by(eventid=eventid).first_or_404()
    if not event:
        return jsonify({'Not found':'Event with that id is not available'}),404

    if event.user_public_id != logged_in_user.public_id:
        return jsonify({'Authorization error':'You can only delete your own event'}),403

    event.delete()
    return jsonify({"message": "Event {} deleted successfully".format(event.eventid)}), 200

#edit and event
@events.route('/api/v1/events/<int:eventid>', methods=['PUT'])
@token_required
def edit_event(logged_in_user,eventid):
    event = models.Events.query.filter_by(eventid=eventid).first_or_404()    
   
    if event.user_public_id != logged_in_user.public_id:
        return jsonify({'Authorization error':'You can only update your own event'}), 403

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
@events.route('/api/v1/events/search/', methods=['GET'])
def searc_by_location():
    name = request.args.get('q')
    #search by location, name or category
    #filter(or_(models.Events.name.ilike('%'+name+'%'), models.Events.location.ilike('%'+name+'%'), models.Events.category.ilike('%'+name+'%') ) )
    event_searched = models.Events.query.filter(or_(models.Events.name.ilike('%'+name+'%'), models.Events.location.ilike('%'+name+'%'), models.Events.category.ilike('%'+name+'%') ) )    
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
                'id': event.eventid,
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
                'public_userid': event.user_public_id,
                'date' : event.date,
                'category': event.category,
                'date_created': event.date_created,
                'event_id': event.eventid             
            })
    return response


#rsvp or respond to an event (attending/not attending)
@events.route('/api/v1/events/<int:eventid>/rsvp', methods=['POST'])
@token_required
def rsvp_to_an_event(logged_in_user, eventid):

    if not request.json or not 'rsvp' in request.json: #name must be included
        return jsonify({'message':'Please provide rsvp details'})

    rsvp = request.json['rsvp']
    if rsvp == 'attending' or rsvp =='not attending':
        event = models.Events.query.filter_by(eventid=eventid).first_or_404()
        if event:
            rsvp = models.Rsvp(
                event = event,
                rsvp = request.json['rsvp'],
                user_pub_id = logged_in_user.public_id 
            )
            rsvp.save()
            response = jsonify({
                'eventid':eventid,
                'rsvpid': rsvp.rsvp_id,
                'message': 'Successfully responded to and event'
            })
            return response,201
        return jsonify({'message':'No event with that id'}),404
    return jsonify({'message':'rsvp must be either attending or not attending'}),403

#get events attending
@events.route('/api/v1/events/rsvp/<string:public_user_id>', methods=['GET'])
@token_required
def get_events_attending(logged_in_user, public_user_id):
    #allow pagination of events attending
    page = request.args.get('page',1,type=int )
    limit = request.args.get('limit',3,type=int) #defaults to 3 if user doesn't specify to limit

    events_attending = models.Rsvp.query.filter_by(user_pub_id=public_user_id).filter_by(rsvp ='attending').paginate(page, limit, False).items
    
    if not events_attending:
        return jsonify({'message':'You Have not rsvp to any event'})
    #events exists
    events = return_rsvpd_events(events_attending)
    response = jsonify(events)
    response.status_code = 200
    return response

#check if user has rsvpd to a single event
@events.route('/api/v1/events/rsvp/<int:event_id>/<string:public_user_id>', methods=['GET'])
@token_required
def check_user_rsvp_for_event(logged_in_user,event_id, public_user_id):
    #allow pagination of events attending
    page = request.args.get('page',1,type=int )
    limit = request.args.get('limit',6,type=int) #defaults to 3 if user doesn't specify to limit

    rsvp_status = models.Rsvp.query.filter_by(user_pub_id=public_user_id).filter_by(eventid =event_id).paginate(page, limit, False).items

    if not rsvp_status:
        response = jsonify('no rsvp to this event')
        response.status_code = 404
        return response
    #user has rsvp to an event
    rsvp = {
        'rsvp_id':rsvp_status[0].rsvp_id,
        'event_id': rsvp_status[0].eventid,
        'rsvp': rsvp_status[0].rsvp
    }

    response = jsonify(rsvp)
    response.status_code = 200
    return response


    
def return_rsvpd_events(event_id_list):
    #A function to get the list of events a user has rsvp to
    events = []
    for event in event_id_list:
        event_id = event.eventid
        
        one_event = models.Events.query.filter_by(eventid=event_id).first()
        event_obj = return_obj(one_event)
        events.append(event_obj)
    return events



#User should be able to edit an rsvp
@events.route('/api/v1/events/<int:eventid>/rsvp/<int:rsvpid>', methods=['PUT'])
@token_required
def edit_rsvp(logged_in_user, eventid, rsvpid):
    #check if that event has rsvp 
    if not request.json or not 'rsvp' in request.json: #name must be included
        return jsonify({'message':'Please provide rsvp details'})

    rsvp = request.json['rsvp']
    if rsvp == 'attending' or rsvp =='not attending':
        event_rsvp = models.Rsvp.query.filter_by(eventid=eventid).first_or_404()
        if not event_rsvp:
            return jsonify({'message': 'That event doesnt have rsvp'}), 404
        #check if the user has rsvp to that event
        rsvp_ = models.Rsvp.query.filter_by(rsvp_id=rsvpid).first_or_404()
        if rsvp_.user_pub_id != logged_in_user.public_id:
            return jsonify({'message': 'Sorry! You can only edit your rsvp'})
        rsvp_.rsvp = request.json.get('rsvp', rsvp_.rsvp)
        rsvp_.save()
        return jsonify({'message': 'You have successfully changed your response'})
    return jsonify({'message':'rsvp must be either attending or not attending'}),403


@events.route('/api/v1/events/<int:eventid>/guests', methods=['GET'])
def list_event_guests(eventid):

    #check if event exists
    event = models.Events.query.filter_by(eventid=eventid).first_or_404()
    if event:
        dic_of_users_rsvp = {}
        results = []
        rsvps = models.Rsvp.query.filter_by(eventid = eventid)
        #if no rsvps
        if not rsvps:
            response = jsonify({'message':'This event has no guests yet.'})
            response.status_code = 404
            return response
        for resp in rsvps:
            user = users_models.User.query.filter_by( public_id = resp.user_pub_id).first()
            user_obj = return_user_object(user.username, resp.rsvp)
            
            results.append(user_obj)

        response = jsonify(results)
        response.status_code = 200

        return response

def return_user_object(username, rsvp):
    user_obj = {
        'username': username,
        'rsvp': rsvp
    }
    return user_obj