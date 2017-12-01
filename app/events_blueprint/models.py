import random
class Events(object):

    events_list = [
        {
            "eventid":112,
            "userid" : 11,
            "name" : "Partymad",
            "location" : "Nairobu",
            "description" : "here and 2",
            "date": "10/10/2017",
            "cost" : 2000,
            "category":"indoors"
        }
    ]
    rsvp_list = [
         {
            "rsvp_id":543,
            "eventid":112,
            "userid":"sam@gmail",
            "rsvp":"attending"
        }
    ]

    def get_random_id():
        # generate a random unique integer to be used as ID
        random_id = random.randrange(1, 10000000)
        return random_id