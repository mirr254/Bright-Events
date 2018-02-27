import unittest
from app import createApp
from app.auth_blueprint.views import generate_email_confirmation_token, confirm_email_confirmation_token
#from app.utils.token import generate_email_confirmation_token,generate_password_reset_token,confirm_email_confirmation_token,confirm_password__reset_token
 

class AppConfigTestCases(unittest.TestCase):

    def setUp(self):
        self.app = createApp(conf_name='testing')

    #test for debugging log
    def test_debug_mode(self):
        self.assertEqual(self.app.debug, False)

class AppCommonFunctionsTestCases(unittest.TestCase):
    def setUp(self):
        self.app = createApp(conf_name='testing')
        self.email = 'kungus@ymail.com'
        self.email_confirmation_token = generate_email_confirmation_token(self.email)

    #test for valid email confirmation token
    def test_valid_email_conf_token(self):
        email = confirm_email_confirmation_token(self.email_confirmation_token,3600)
        self.assertEqual(email, self.email)
    