from marshmallow import Schema, fields, ValidationError, validates
from models import User
class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    firstname = fields.Str()
    lastname = fields.Str()
    region = fields.Int()
    service_provider = fields.Bool()
    admin = fields.Bool()
    date_joined = fields.Date()
    recommender = fields.Bool()
    passwordhash = fields.Str(dump_only=True)

    @validates('email')
    def validate_email(self,value):
        user = User.query.filter_by(email=value).first()
        if user:
            raise ValidationError('email is already taken')

    @validates('phone')
    def validate_phone(self,value):
        user = User.query.filter_by(phone=value).first()
        if user:
            raise ValidationError('phone number is already in use.')

        if len(value)<10:
            raise ValidationError('Not a valid phone number')    