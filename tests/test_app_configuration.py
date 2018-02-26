import unittest
from app import createApp
from . import test_user_auth

class AppConfigTestCases(unittest.TestCase):

    def setup(self):
        self.app = createApp(conf_name='testing')
        self.assertEqual(self.app.debug, False)