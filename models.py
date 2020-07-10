from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
import jwt
from config import app
class Region(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False,unique=True)

    def __repr__(self):
        return "<Region {}>".format(self.name)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,nullable=False,unique=True)
    phone = db.Column(db.String,nullable=False,unique=True)
    firstname = db.Column(db.String,nullable=True)
    lastname = db.Column(db.String,nullable=True)
    region = db.Column(db.Integer,db.ForeignKey('region.id'))
    service_provider = db.Column(db.Boolean,default=False)
    admin = db.Column(db.Boolean,default=False)
    date_joined = db.Column(db.Date,nullable=False)
    recommender = db.Column(db.Boolean,default=True)
    passwordhash = db.Column(db.String,nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is write only")

    def set_password(self,password):
        self.passwordhash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.passwordhash,password)

    def encode_auth_token(self,user_id):
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=0, seconds=300),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }

            return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired, please log in again"
        except jwt.InvalidTokenError:
            return "Invalid token"

    def __repr__(self):
        return "<User {}>".format(self.email)

class Bug(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String,nullable=False)
    body = db.Column(db.String,nullable=False)
    user = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Bug {}>".format(self.subject)
