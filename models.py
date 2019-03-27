"""
Barscreen Web App Models
"""
import imghdr

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
from helpers import hash_password
from sqlalchemy.orm import validates

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Users(BaseModel):
    "Customer users model"
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    company = db.Column(db.String, nullable=False)
    ads = db.Column(db.BOOLEAN, default=False)
    confirmed = db.Column(db.BOOLEAN, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.CHAR(128), nullable=True)
    admin = db.Column(db.BOOLEAN, default=False)

    def __init__(self, first_name, last_name, phone_number, email, company, confirmed_on=None, admin=None, password=None, ads=False, confirmed=False):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.company = company
        self.email = email
        self.ads = ads
        self.confirmed = confirmed
        self.password = password

        if admin:
            self.admin = admin
        
        if confirmed_on:
            self.confirmed_on = confirmed_on

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @property
    def is_authenticated(self):
        return self.confirmed

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        self.password = hash_password(password)
        return True


class User(BaseModel):
    """
    GUI user model
    """
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.CHAR(120), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)


class Show(BaseModel):
    """
    Channel Show Model
    """
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Show {}>'.format(self.name)

    def get_id(self):
        return str(self.id)


class Clip(BaseModel):
    """
    Clip Model
    """
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=0)
    clip_data = db.Column(db.LargeBinary)


class Channel(BaseModel):
    """
    Channel Model
    """
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image_data = db.Column(db.LargeBinary)
    
    @validates('image_data')
    def validate_image_data(self, key, image_data):
        if not image_data:
            raise AssertionError("No image data provided")
        img_type = imghdr.what('', image_data)
        if img_type != 'jpeg' and img_type != 'png':
            raise AssertionError("Please use  a jpeg or a png file for a channel image")
        return image_data

