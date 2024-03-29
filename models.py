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
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())


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
    promos = db.relationship("Promo", backref="user", lazy=True)
    loops = db.relationship("Loop", backref="user", lazy=True)
    password = db.Column(db.CHAR(128), nullable=True)
    admin = db.Column(db.BOOLEAN, default=False)
    api_key = db.Column(db.String, nullable=True)

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


class Show(BaseModel):
    """
    Channel Show Model
    """
    name             = db.Column(db.String, nullable=False, unique=True)
    description      = db.Column(db.String, nullable=False)
    lookback         = db.Column(db.Integer, default=1)
    order            = db.Column(db.String, default="recent")
    channel_id       = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    clips            = db.relationship("Clip", backref="show", lazy=True)

    def __repr__(self):
        return '<Show {}>'.format(self.name)

    def get_id(self):
        return str(self.id)


class Clip(BaseModel):
    """
    Clip Model
    """
    name        = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    duration    = db.Column(db.Integer, nullable=False, default=0)
    clip_url    = db.Column(db.String, nullable=True)
    show_id     = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    image_url   = db.Column(db.String, nullable=True)


class Channel(BaseModel):
    """
    Channel Model
    """
    name        = db.Column(db.String, nullable=False, unique=True)
    category    = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image_url   = db.Column(db.String, nullable=True)
    shows       = db.relationship("Show", backref="channel", lazy=True)

    @validates('image_data')
    def validate_image_data(self, key, image_data):
        if not image_data:
            raise AssertionError("No image data provided")
        img_type = imghdr.what('', image_data)
        if img_type != 'jpeg' and img_type != 'png':
            raise AssertionError(
                "Please use  a jpeg or a png file for a channel image")
        return image_data


class Promo(BaseModel):
    name        = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    duration    = db.Column(db.String, nullable=True)
    clip_url    = db.Column(db.String, nullable=True)
    image_url   = db.Column(db.String, nullable=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Loop(BaseModel):
    name              = db.Column(db.String, nullable=False)
    playlist          = db.Column(db.ARRAY(db.String), nullable=False)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lp_clips          = db.Column(db.String, nullable=True) # sid=cid&sid=cid
    image_url         = db.Column(db.String, nullable=True)

    def get_last_played_clips(self):
        if not self.lp_clips:
            return {}
        clips = self.lp_clips.split("&")
        out = {}
        for x in clips:
            x = x.split("=")
            out[int(x[0])] = int(x[1])
        return out

    def set_last_played_clips(self, d):
        self.lp_clips = "&".join(["=".join([str(k), str(d[k])]) for k in d])


shortFormVideoSchema = {
    "id": str,
    "title": str,
    "content": str,
    "thumbnail": str,
    "shortDescription": str,
}
