from marshmallow import Schema, fields

class BugSchema(Schema):
    id = fields.Int(dump_only=True)
    subject = fields.Str()
    body = fields.Str()

class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    phone = fields.Str()
    firstname = fields.Str()
    lastname = fields.Str()
    region = fields.Int()
    service_provider = fields.Bool()
    admin = fields.Bool()
    date_joined = fields.Date()
    recommender = fields.Bool()
    passwordhash = fields.Str(dump_only=True)