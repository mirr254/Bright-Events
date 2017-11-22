import unittest
import json
from app import createApp


class UserActivitiesTestcase(unittest.TestCase):
    """This class will be used for user test cases"""

    def setUp(self):
        self.app = createApp()
        self.client = self.app.test_client
        self.user = {
            'id': 1,
            'email': 'email',
            'username':'username',
            'password':'password'
        }

    #test if user can register
    def test_auth_register(self):
        res = self.client().post('/api/v1/auth/register', data=json.dumps(self.user),content_type='application/json')
        self.assertEqual(res.status_code, 201)