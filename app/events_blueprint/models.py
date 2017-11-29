import random
class Events(object):

    events_list = []
    rsvp_list = []

    def get_random_id():
        # generate a random unique integer to be used as ID
        random_id = random.randrange(1, 10000000)
        return random_id