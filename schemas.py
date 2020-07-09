from marshmallow import Schema, fields

class BugSchema(Schema):
    id = fields.Int(dump_only=True)
    subject = fields.Str()
    body = fields.Str()