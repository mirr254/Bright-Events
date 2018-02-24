import unittest
import json
from app import createApp, db
from . import test_user_auth
import base64


class EventsActivitiesTestCases(unittest.TestCase):

    def setUp(self):
        self.app = createApp(conf_name='testing')
        self.client = self.app.test_client

        #url route variable
        self.base_event_url = "/api/v1/events"
        self.base_auth_url = "/api/v1/auth"

        self.event1 = {
            "name" : "Partymad",
            "location" : "Nairobi",
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
            "event" : self.event1,           
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
        return self.client().post(self.base_auth_url+'/register', data=user_details, content_type='application/json')

    def open_with_auth(self, url, method, username, password):
        return self.app.test_client().open(url,
                   method = method,
                   headers = {
                        'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'utf-8')).decode('utf-8') }
    )

    #login the newly created user
    def user_login(self):        
        return self.open_with_auth(self.base_auth_url+'/login', 'GET', 'test', 'hardpass')

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

        res = self.client().post(self.base_event_url,
                      headers = {'x-access-token' : token },
                      data=json.dumps(self.event1), content_type='application/json')

        self.assertEqual(res.status_code, 201)
    
    def test_if_add_event_has_location(self):
        token = self.get_verfication_token()

        res = self.client().post(self.base_event_url,
              headers = {'x-access-token' : token },
              data=json.dumps(self.event2), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_if_add_event_has_name(self):
        token = self.get_verfication_token()

        res = self.client().post(self.base_event_url, 
            headers = {'x-access-token' : token },
            data=json.dumps(self.event3), content_type='application/json')
        self.assertEqual(res.status_code, 403)

    #test api can get all events
    def test_can_get_events(self):
        token = self.get_verfication_token()

        self.test_add_event()  

        res = self.client().get(self.base_event_url,
             headers = {'x-access-token' : token },
             content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Partymad', str(res.data))

    #test filtering events by location
    def test_for_filter_events_by_location(self):
        token = self.get_verfication_token()

        #add event before testing the filtering
        self.test_add_event()

        res = self.client().get(self.base_event_url+'?location=nairobi', 
              headers = {'x-access-token': token},
              content_type='application/json')
        self.assertIn('Nairobi', str(res.data))
        

    #test rsvp
    def test_rsvp_an_event(self):
        token = self.get_verfication_token()
        #make sure before rsvp we have an add event api working
        self.test_add_event()        
        
        res = self.client().post(self.base_event_url+'/1/rsvp',
             headers = {'x-access-token' : token },
             data=json.dumps(self.rsvp_) ,content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('Successfully responded to and event', str(res.data))
        self.assertIn('eventid', str(res.data))

    #test listing users who have responded (rsvp) to an event
    def test_list_rsvp_users(self):
        token = self.get_verfication_token()
        #test create an event
        self.test_add_event()
        
        ### test user can rsvp to that event ###                
        self.test_rsvp_an_event() 

        #test the endpoint for retrieving the users. will retrieve users based on eventid                
        res = self.client().get(self.base_event_url+'/1/guests',
                headers = {'x-access-token' : token },
                content_type='application/json')        
        self.assertEqual(res.status_code, 200)
        self.assertIn('test', str(res.data))


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    
    if __name__ == '__main__':
        unittest.main()      