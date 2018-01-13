# from passlib.apps import custom_app_context as pwd_context
import random
from app import db, createApp

class User(db.Model):
    """This class represents the users table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), index=True)
    email = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, username, password_hash, public_id, email):
        self.username = username
        self.password_hash = password_hash
        self.public_id = public_id
        self.email = email

  

    def save(self):
        db.session.add(self)
        db.session.commit()



