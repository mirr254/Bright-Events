# from passlib.apps import custom_app_context as pwd_context
import random
import os
from passlib.apps import custom_app_context as passwd_context #based on sha256_crypt algo
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
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
  

    #hash the user password
    def hash_password(self, password):
        self.password_hash = passwd_context.encrypt(password)

    #verify if password supplied is equal to hashed password
    def verify_password(self, password):
        return passwd_context.verify(password, self.password_hash) #true if paswd is correct

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_auth_token(self, expiration = 600):
        s = Serializer("super awesome secret #$%^*(", expires_in = expiration)
        return s.dumps({ 'id': self.id })


