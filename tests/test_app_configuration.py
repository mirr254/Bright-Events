import unittest
from app import createApp
from . import test_user_auth

class AppConfigTestCases(unittest.TestCase):

    def setUp(self):
        self.app = createApp(conf_name='testing')

    #test for debugging log
    def test_debug_mode(self):
        self.assertEqual(self.app.debug, False)