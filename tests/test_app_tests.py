import unittest
import json
from app import createApp
from flask import session, request


class UserActivitiesTestcase(unittest.TestCase):
    """This class will be used for user test cases"""

    def setUp(self):
        self.app = createApp('development')
        self.client = self.app.test_client
        self.user = {
            'id': 1,
            'email': 'email@',
            'username':'samuel',
            'password':'hardpass'
        }
        self.user2 = {
            'id': 1,            
            'username':'samuel',
            'password':'hardpass'
        }
        self.user3 = {
            'id': 1,
            'email': 'emai@gma',
            'username':'samuel'            
        }
        self.event1 = {
            "eventid":1,
            "userid" : 2,
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000,
            "category": "Indoors"
        }
        self.event2 = {
            "eventid":1,
            "userid" : 2,
            "name" : "Partymad",            
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.event3 = {
            "eventid":1,
            "userid" : 2,            
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.event4 = {
            "eventid":1,            
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.rsvp_ = {
            "rsvp_id":1,
            "eventid":20,
            "userid":23456,
            "rsvp":"attending"
        }

        self.user_login_without_email = {
            
            "password":"string1"
        }
        self.new_password = {
                  "password":"1234@"
              }
        self.login_data = {
            "email":"email@",
            "password":"hardpass"
        }


    #test if user can register
    def test_auth_register(self):
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),content_type='application/json')
        self.assertEqual(res.status_code, 201)

    #make sure email is not empty
    def test_auth_register_email_notEmpty(self):
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user2),content_type='application/json')
        self.assertIn("Email must be included", str(res.data))

    #make sure password is set
    def test_auth_register_password_notEmpty(self):
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user3),content_type='application/json')
        self.assertIn("Password must be included", str(res.data))

    #test reset password api 
    def test_auth_reset_password(self):
        #test if user can register before changing password
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        # test if user can now update password
        res = self.client().put('/api/v1/auth/reset-password/email@', 
              data=json.dumps(self.new_password),
              content_type='application/json')
        self.assertEqual(res.status_code, 200)

    #test logout
    def test_logout(self):
        #register first
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        #test login
        res_login = self.client().post('/api/v1/auth/login', data=json.dumps(self.login_data),content_type='application/json')
        result_in_json = json.loads(res_login.data.decode('utf-8').replace("'", "\""))
        print(result_in_json)
        session['email'] = str( result_in_json['user']['email'])
        session['userid'] = str( result_in_json['user']['userid'])
        self.assertEqual(res.status_code, 200)
        #then test logout
        self.assertEqual(session['email'], None)
        self.assertEqual(session['userid'], None)
        



    """Unit tests for events goes here"""    

    def test_add_event(self):
        res = self.client().post('/api/v1/events', data=json.dumps(self.event1), content_type='application/json')
        self.assertEqual(res.status_code, 201)
    
    def test_add_event_has_location(self):
        res = self.client().post('/api/v1/events', data=json.dumps(self.event2), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_add_event_has_name(self):
        res = self.client().post('/api/v1/events', data=json.dumps(self.event3), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_add_event_has_userid(self):
        res = self.client().post('/api/v1/events', data=json.dumps(self.event4), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    #test api can get all events
    def test_can_get_events(self):
        res = self.client().get('/api/v1/events', content_type='application/json')
        self.assertEqual(res.status_code, 200)

    #test rsvp
    def test_rsvp_an_event(self):
        #make sure before rsvp we have an add event api working
        resp = self.client().post('/api/v1/events', data=json.dumps(self.event1), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        result_in_json = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        #get eventid of newly created event
        eventid = str( result_in_json['event']['eventid'])
        res = self.client().post('/api/v1/events/'+eventid+'/rsvp',
             data=json.dumps(self.rsvp_) ,content_type='application/json')
        self.assertEqual(res.status_code, 201)

    #test listing users who have responded (rsvp) to an event
    def test_list_rsvp_users(self):
        #test create an event
        resp = self.client().post('/api/v1/events', data=json.dumps(self.event1), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        ### test user can rsvp to that event ###
        result_in_json = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        #get eventid of newly created event
        eventid = str( result_in_json['event']['eventid'])
        res = self.client().post('/api/v1/events/'+eventid+'/rsvp',data=json.dumps(self.rsvp_) ,content_type='application/json')
        
        self.assertEqual(res.status_code, 201)

        #test the endpoint for retrieving the users. will retrieve users based on eventid
        # result_as_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # res = self.client().get('/api/v1/events/'+eventid+'/rsvp',content_type='application/json')
        # #print(json.loads(res.data.decode('utf-8').replace("'", "\"")))
        # self.assertEqual(res.status_code, 200)
    
    if __name__ == '__main__':
        unittest.main()       
    