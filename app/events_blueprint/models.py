import random
from app import db

class Events(db.Model):

    """This class represents the events table."""

    __tablename__ = 'events'

    eventid = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    name = db.Column(db.String(255))
    user_public_id = db.Column(db.String(50))
    description = db.Column(db.String(255))
    category = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
   

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

    def __init__(self, name, user_public_id, cost,location,date,description,category):        
        self.name = name
        self.user_public_id = user_public_id
        self.cost = cost
        self.location = location
        self.date = date
        self.description = description
        self.category = category




class Rsvp(db.Model):
    """This class represents the rsvp table. Details of users rsvp"""

    __tablename__ = 'rsvps'

    rsvp_id = db.Column(db.Integer, primary_key=True)
    user_public_id = db.Column(db.Integer)
    eventid = db.Column(db.Integer)   
    rsvp = db.Column(db.String(255))   
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, eventid,rsvp,user_public_id):
        """initialize with name."""
        self.eventid = eventid
        self.rsvp = rsvp
        self.user_public_id = user_public_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():#get all rsvps in a single query
        return Rsvp.query.all()
    

    def __repr__(self):
        return "<Rsvp: {}>".format(self.rsvpid) #object instance of the model whenever it is queried
