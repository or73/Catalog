"""
File Path: application/modules/user/models.py
Description: User models for App - Define User models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash

from setup import db
from ..base_model import BaseModel
from crud import CRUDMixin
from config import Config


class User(UserMixin, CRUDMixin, db.Model):   # BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    # User authentication fields
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True)
    # User fields
    active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(100))
    # User Control
    authenticated = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now())
    provider = db.Column(db.String(10), default='local')   # local - facebook - google
    profile = db.Column(db.String(10), default='user')     # user - admin
    session_token = db.Column(db.String(150), unique=True)

# -------------------- INIT --------------------
    def __init__(self, authenticated, email, first_name, last_name, password,
                 picture, profile, provider, username, session_token):
        # User authentication fields
        self.email = email
        self.password_hash(password)
        self.username = username
        # User Fields
        self.first_name = first_name
        self.last_name = last_name
        self.picture = picture
        # User Control
        self.authenticated = authenticated
        self.set_last_login()
        self.profile = profile
        self.provider = provider
        if session_token:
            self.session_token = session_token
        else:
            self.session_token = self.generate_auth_token(600)

    def __repr__(self):
        return '<Username {}>'.format(self.username)

    # -------------------- PROPERTIES --------------------
    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'authenticated': self.authenticated,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'last_login': self.last_login,
            'picture': self.picture,
            'profile': self.profile,
            'provider': self.provider,
            'session_token': self.session_token
        }

    # -------------------- GETTERS --------------------
    def get_id(self):
        """ GET - User: return user_id """
        # return self.id
        return self.session_token

    def get_user_id(self):
        """ GET - User: return user_id """
        return self.id

    def get_username(self):
        """ GET - User: return username """
        return self.username

    def get_authenticated(self):
        """ GET - User: return authenticated """
        return self.authenticated

    def get_email(self):
        """ GET - User: return email """
        return self.email

    def get_first_name(self):
        """ GET - User: return first_name """
        return self.first_name

    def get_last_name(self):
        """ GET - User: return last_name """
        return self.last_name

    def get_last_login(self):
        """ GET - User: return last_login - last login time """
        return self.last_login

    def get_session_token(self):
        """ GET - User: return session_token """
        return self.session_token

    # -------------------- SETTERS --------------------
    def set_authenticated(self, authenticated):
        """ SET - User: authenticated """
        self.authenticated = authenticated

    def set_email(self, email):
        """ SET - User: email """
        self.email = email

    def set_first_name(self, first_name):
        """ SET - User: first_name """
        self.first_name = first_name

    def set_last_name(self, last_name):
        """ SET - User: last_name """
        self.last_name = last_name

    def set_last_login(self):
        """ SET - User: last_login - last login time"""
        self.last_login = self.set_time()

    def set_session_token(self):
        """SET - User: session_token"""
        self.session_token = self.generate_auth_token(600)

    def set_username(self, username):
        """ SET - User: username """
        self.username = username

    # -------------------- METHODS --------------------
    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_owner_category(self, category_name):
        from ..category import CategoryMethod
        return self.id == CategoryMethod.get_owner_by_name(category_name)

    def is_owner_item(self, item_name):
        from ..item import ItemMethod
        return self.id == ItemMethod.get_owner_by_name(item_name)

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY,
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    def password_hash(self, password):
        """ Hash password """
        self.password = generate_password_hash(password, method='sha256')

    def validate_password(self, password):
        """ Validate provided password with password in DB """
        return check_password_hash(self.password, password)

    # -------------------- STATIC METHODS --------------------
    @staticmethod
    def set_time():
        """ Return current datetime """
        return datetime.datetime.now()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None   # Valid token, but expired
        except BadSignature:
            return None   # Invalid Token
        user = User.query.get(data['id'])
        return user
