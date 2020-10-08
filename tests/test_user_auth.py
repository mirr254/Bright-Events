from app import createApp,db
from flask import request, jsonify
from functools import wraps
from app.auth_blueprint import models
import jwt
import re
import unittest
import json
import base64

class UserActivitiesTestcase(unittest.TestCase):
    """This class will be used for user test cases"""

    def setUp(self):
        self.app = createApp(conf_name='testing')
        self.client = self.app.test_client
        self.AUTH_URL_BASE_ROUTE = '/api/v1/auth/'

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        self.user = {
            'email': 'kungus@ymail.com',
            'username':'test',
            'password':'hardpass123'
        }
        self.user5 = {
            'email': 'kungus@ymail.com',
            'username':'test1',
            'password':'hardpass123'
        }
        self.user6 = {
            'email': 'kungusamuel90@gmail.com',
            'username':'test1',
            'password':'hardpass123'
        }
        self.user1 = {
            'email' : 'kungus@ymail.com',
            'username' : 'test1',
            'password' :  '        '
        }
        self.login_details = {
            'username' : 'kungus@ymail.com',
            'password' : 'hardpass'
        }
        self.user2 = {                        
            'username':'samuel',
            'password':'hardpass'
        }
        self.user3 = {            
            'email': 'kungus@ymail.com',
            'username':'samuel'            
        }
        self.user4 = {            
            'email': 'kungus@ymail.com',
            'username':'samuel',
            'password':'easypass'          
        }
        self.user_with_bad_chars = {
            'email': 'kungusa@ymail.com',
            'username':'#$5234#@!$$',
            'password':'easypass32324'
        }
        self.user_with_only_numbers = {
            'email': 'kunguas@ymail.com',
            'username':'12345667',
            'password':'easypass22323'
        }
        self.user_with_wrong_json_type ={
            'email': 'kunguas@ymail.com',
            'username': 12345667,
            'password':'easypass22323'
        }

        self.user_login_without_email = {
            
            "password":"string1"
        }
        self.new_password = {
                  "password":"123456@"
              }

    
    #helper methods to login and register
    #login
    def auth_login(self):
        return self.open_with_auth( self.AUTH_URL_BASE_ROUTE+'login', 'GET', 'test', 'hardpass123')

    #register a user
    def register_users(self):
        return self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user), content_type='application/json')

     #get the token from logged in user
    def get_verfication_token(self):
        
        #register user 1st
        self.register_users()

        #login the user
        res = self.auth_login()
        #from nose.tools import set_trace; set_trace()
        #get the access token        
        token = json.loads(res.data.decode('utf-8'))['token']        
            
        return token

    
    def open_with_auth(self, url, method, username, password):
        return self.app.test_client().open(url,
                   method = method,
                   headers = {
                        'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii') }
    )
       
    #test if user can register
    def test_auth_register(self):
        res = self.register_users() 
        self.assertEqual(res.status_code, 201)

    #test if username has only digits
    def test_username_has_digits_only(self):
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user_with_only_numbers),content_type='application/json')
        self.assertIn('That is not a valid username', str(res.data))

    #test if username contains special characters
    def test_username_contains_special_chars(self):
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user_with_bad_chars),content_type='application/json')
        self.assertIn('That is not a valid username', str(res.data))

    #test if username contains special characters
    def test_username_with_wrong_json_type(self):
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user_with_wrong_json_type),content_type='application/json')
        self.assertIn('wrong json type. Please try again', str(res.data))

    #test for duplicate email registration
    def test_auth_duplicate_email_registration(self):
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user), content_type='application/json')
        res2 = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user5), content_type='application/json')
        self.assertIn('Email already taken', str(res2.data))

    #test for duplicate username
    def test_auth_duplicate_username_registration(self):
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user5), content_type='application/json')
        res2 = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user6), content_type='application/json')
        self.assertIn('Username already taken', str(res2.data))


    #test password length
    def test_auth_password_length_on_registration(self):        
        passwrd = self.user['password']
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user), content_type='application/json')             
        self.assertGreaterEqual( len(passwrd), 7)
    
    #test if user login
    def test_auth_login(self):

        self.test_auth_register()
        res = self.auth_login()
        self.assertEqual(res.status_code, 200)

    #test for logout endpoint
    def test_auth_logout(self):
        #register user
        res = self.register_users()       
        #log in user 1st
        res = self.auth_login()
        #log out user
        token = self.get_verfication_token()

        res = self.client().get(self.AUTH_URL_BASE_ROUTE+'logout',
                    headers = {'x-access-token' : token },
                    content_type='application/json')
        self.assertEqual(res.status_code, 200)


    #make sure email is not empty
    def test_auth_register_has_email(self):
        res = self.client().post(self.AUTH_URL_BASE_ROUTE+'register', data=json.dumps(self.user2),content_type='application/json')
        self.assertIn("email, username and password are required", str(res.data))

    #test reset password api 
    def test_auth_reset_password_with_unconfirmed_email(self):
        #test if user can register before changing password
        res = self.register_users()
       
        # test if user can now update password
        res = self.client().put(self.AUTH_URL_BASE_ROUTE+'reset-password/kungus@ymail.com',data=json.dumps(self.new_password),
                  content_type='application/json')        
        self.assertEqual(res.status_code, 401) 
        self.assertIn('Token is invalid or expired', str(res.data))


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    
    if __name__ == '__main__':
        unittest.main()