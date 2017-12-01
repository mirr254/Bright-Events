# from passlib.apps import custom_app_context as pwd_context
import random

class User(object):

    #store user details in a list of dic
    users_list = [
        {
            'id': 11,
            'email': 'email@gmail.com',
            'username':'samuel',
            'password':'hardpass'
        }
    ]
    def get_random_id():
        # generate a random unique integer to be used as ID
        random_id = random.randrange(1, 10000000)
        return random_id

    #hash the user password
    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)

    # #verify if password supplied is equal to hashed password
    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash) #true if paswd is correct

