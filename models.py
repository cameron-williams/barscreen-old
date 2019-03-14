"""
Barscreen Web App Models
"""

from flask_sqlalchemy import SQLAlchemy

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
    password = db.Column(db.CHAR(120), nullable=True)

    def __init__(self, first_name, last_name, phone_number, email, company, password=None, ads=False, confirmed=False):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.company = company
        self.email = email
        self.ads = ads
        self.confirmed = confirmed
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)


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
