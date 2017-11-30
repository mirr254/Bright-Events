import random
class Events(object):

    events_list = [
        {
            "eventid":1,
            "userid" : 2,
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
            "rsvp_id":1,
            "eventid":20,
            "userid":"sam@gmail",
            "rsvp":"attending"
        }
    ]

    def get_random_id():
        # generate a random unique integer to be used as ID
        random_id = random.randrange(1, 10000000)
        return random_id