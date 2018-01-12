import unittest
import json
from app import createApp, db

class EventsActivitiesTestCases(unittest.TestCase):

    def setUp(self):
        self.app = createApp(conf_name='testing')
        self.client = self.app.test_client

         self.event1 = {            
            "userid" : 2,
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000,
            "category": "Indoors"
        }
        self.event2 = {
            "userid" : 2,
            "name" : "Partymad",            
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.event3 = {
            "userid" : 2,            
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.event4 = {            
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000
        }
        self.rsvp_ = {            
            "eventid":1,
            "userid":2,
            "rsvp":"attending"
        }

         """Unit tests for events goes here"""    

     # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

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
        
        res = self.client().post('/api/v1/events/1/rsvp',
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
        res = self.client().post('/api/v1/events/1/rsvp',data=json.dumps(self.rsvp_) ,content_type='application/json')
        print(res)
        self.assertEqual(res.status_code, 201)

        #test the endpoint for retrieving the users. will retrieve users based on eventid
        # result_as_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # res = self.client().get('/api/v1/events/'+eventid+'/rsvp',content_type='application/json')
        # #print(json.loads(res.data.decode('utf-8').replace("'", "\"")))
        # self.assertEqual(res.status_code, 200)


     def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    
    if __name__ == '__main__':
        unittest.main()      