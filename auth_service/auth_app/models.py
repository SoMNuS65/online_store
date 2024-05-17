from auth_app import db, login
from datetime import datetime, timedelta
from flask_jwt_extended import decode_token
from flask_login import UserMixin
import uuid

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)

    def __repr__(self) -> str:
        return f'<User : {self.email}>'
    
class Validation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    otp = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        expiration_time = timedelta(seconds=180)
        return (datetime.utcnow() - self.created_at) > expiration_time
    
    def __repr__(self) -> str:
        return f'Validation code : {self.otp}, of email : {self.email}'
    
