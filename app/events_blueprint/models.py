import random
from app import db

class Events(db.Model):

    """This class represents the events table."""

    __tablename__ = 'events'

    eventid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    userid = db.Column(db.Integer)
    description = db.Column(db.String(255))
    category = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Events.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Event: {}>".format(self.name) #object instance of the model whenever it is queried

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


class Rsvp(db.Model):
    """This class represents the rsvp table. Details of users rsvp"""

    __tablename__ = 'rsvps'

    rsvp_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    eventid = db.Column(db.Integer)   
    rsvp = db.Column(db.String(255))   
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, rsvpid):
        """initialize with name."""
        self.rsvpid = rsvpid

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():#get all rsvps in a single query
        return Rsvp.query.all()
    

    def __repr__(self):
        return "<Rsvp: {}>".format(self.rsvpid) #object instance of the model whenever it is queried
