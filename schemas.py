from marshmallow import Schema, fields, ValidationError, validates, INCLUDE
from models import User, Category, SubCategory
from config import db

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
    passwordhash = fields.Str(load_only=True)

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

    class Meta:
        unknown = INCLUDE  
        ordered = True

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()

    @validates('name')
    def validate_name(self,value):
        category = Category.query.filter_by(name=value).first()
        if category:
            raise ValidationError("Category already exists")

class SubCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    category = fields.Int()

    @validates('name')
    def validate_name(self,value):
        subcategory = SubCategory.query.filter_by(name=value).first()
        if subcategory:
            raise ValidationError("Category already exists")