"""
File path: application/modules/auth/models.py
Description: Auth models for App - Define auth/login data model
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from ..base_model import BaseModel
from crud import CRUDMixin


class Auth(CRUDMixin, db.Model):   #, BaseModel):
    """ Model for Auth """
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    # User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # LogIn
    login_time = db.Column(db.DateTime, default=datetime.datetime.now())
    # LogOut
    logout_time = db.Column(db.DateTime, default=None)

    # _default_fields = ['user_id', 'login_time', 'logout_time']
    # _hidden_fields = []
    # _read_only_fields = []

    # -------------------- INIT --------------------
    def __init__(self, user_id):
        # User session init/end fields
        self.user_id = user_id
        self.login_time = self.set_time()
        self.logout_time = None

    def __repr__(self):
        return '<Login {}>'.format(self.user_id)

    # -------------------- PROPERTIES --------------------
    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'login_time': self.login_time,
            'logout_time': self.logout_time
        }

    # -------------------- GETTERS --------------------
    def get_id(self):
        """ GET - return auth id """
        return self.id

    def get_user_id(self):
        """ GET - return auth_user_id """
        return self.user_id

    def get_login_time(self):
        """ GET - return auth_login_time - session login time """
        return self.login_time

    def get_logout_time(self):
        """ GET - return auth_logout_time - session logout time """
        return self.logout_time

    # -------------------- SETTERS --------------------
    def set_user_id(self, user_id):
        """ SET - Auth: user_id """
        self.user_id = user_id

    def set_login_time(self):
        """ SET - Auth: login_time - session login time """
        self.login_time = self.set_time()

    def set_logout_time(self):
        """ SET - Auth: logout_time - session logout time"""
        self.logout_time = self.set_time()

    # -------------------- STATIC METHODS --------------------
    @staticmethod
    def set_time():
        """ Return current datetime """
        return datetime.datetime.now()
