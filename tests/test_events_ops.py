import unittest
import json
from app import createApp, db
from . import test_app_tests
import base64

class EventsActivitiesTestCases(unittest.TestCase):

    def setUp(self):
        self.app = createApp(conf_name='testing')
        self.client = self.app.test_client

        self.event1 = {
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "2017-12-24",
            "cost" : 2000,
            "category": "Indoors"
        }
        self.event2 = {            
            "name" : "Partymad",            
            "description" : "here and 2",
            "date": "2018-01-05",
            "cost" : 2000
        }
        self.event3 = {                        
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.event4 = {            
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "2017-10-10",
            "cost" : 2000
        }
        self.rsvp_ = {            
            "eventid":1,            
            "rsvp":"attending"
        }

        self.user = {
            'email': 'test@kungu.com',
            'username':'test',
            'password':'hardpass'
        }
        self.login_details = {
            'username' : 'test',
            'password' : 'hardpass'
        }

        """Unit tests for events goes here"""    

     # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    #register a user
    def register_users(self):
        user_details = json.dumps(self.user)
        return self.client().post('api/v1/auth/register', data=user_details, content_type='application/json')

    def open_with_auth(self, url, method, username, password):
        return self.app.test_client().open(url,
                   method = method,
                   headers = {
                        'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'utf-8')).decode('utf-8') }
    )

    #login the newly created user
    def user_login(self):        
        return self.open_with_auth('/api/v1/auth/login', 'GET', 'test', 'hardpass')

    #get the token from logged in user
    def get_verfication_token(self):
        
        #register user 1st
        self.register_users()

        #login the user
        res = self.user_login()
        #from nose.tools import set_trace; set_trace()
        #get the access token        
        token = json.loads(res.data.decode('utf-8'))['token']        
            
        return token

    def test_add_event(self):
        token = self.get_verfication_token()   

        res = self.client().post('/api/v1/events',
                      headers = {'x-access-token' : token },
                      data=json.dumps(self.event1), content_type='application/json')

        self.assertEqual(res.status_code, 201)
    
    def test_add_event_has_location(self):
        token = self.get_verfication_token()

        res = self.client().post('/api/v1/events',
              headers = {'x-access-token' : token },
              data=json.dumps(self.event2), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_add_event_has_name(self):
        token = self.get_verfication_token()

        res = self.client().post('/api/v1/events', 
            headers = {'x-access-token' : token },
            data=json.dumps(self.event3), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    #test api can get all events
    def test_can_get_events(self):
        token = self.get_verfication_token()

        res = self.client().get('/api/v1/events',
             headers = {'x-access-token' : token },
             content_type='application/json')
        self.assertEqual(res.status_code, 200)

    #test rsvp
    def test_rsvp_an_event(self):
        token = self.get_verfication_token()
        #make sure before rsvp we have an add event api working
        resp = self.client().post('/api/v1/events',
             headers = {'x-access-token' : token },
             data=json.dumps(self.event1), content_type='application/json')
        self.assertEqual(resp.status_code, 201)        
        
        res = self.client().post('/api/v1/events/1/rsvp',
             headers = {'x-access-token' : token },
             data=json.dumps(self.rsvp_) ,content_type='application/json')
        self.assertEqual(res.status_code, 201)

    #test listing users who have responded (rsvp) to an event
    def test_list_rsvp_users(self):
        token = self.get_verfication_token()
        #test create an event
        resp = self.client().post('/api/v1/events',
            headers = {'x-access-token' : token }, 
            data=json.dumps(self.event1), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        ### test user can rsvp to that event ###
        result_in_json = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        #get eventid of newly created event        
        res = self.client().post('/api/v1/events/1/rsvp',
            headers = {'x-access-token' : token },
            data=json.dumps(self.rsvp_) ,content_type='application/json')
        
        self.assertEqual(res.status_code, 201)

        #test the endpoint for retrieving the users. will retrieve users based on eventid
        result_as_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
                
        res = self.client().get('/api/v1/events/1/guests',
                headers = {'x-access-token' : token },
                content_type='application/json')        
        self.assertEqual(res.status_code, 200)



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    
    if __name__ == '__main__':
        unittest.main()      