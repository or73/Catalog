"""
File Path: application/modules/category/models.py
Description: Category models for App - Define Category models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime
import json

from setup import db
from ..base_model import BaseModel
from crud import CRUDMixin


class Category(CRUDMixin, db.Model):   # BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    # Category
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)

    # Category Control
    last_update = db.Column(db.DateTime)

    # Owner
    owner = db.Column(db.Integer)

# -------------------- INIT --------------------
    def __init__(self, name, description, owner):
        # User session init/end fields
        self.name = name
        self.description = description
        self.owner = owner
        self.last_update = self.set_time()

    def __repr__(self):
        return '<Category {}>'.format(self.id)

    # -------------------- PROPERTIES --------------------
    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        return {
            'id': self.id,
            'name': self.category_id,
            'description': self.item_id,
            'last_update': self.last_update,
            'owner': self.owner
        }

    # -------------------- GETTERS --------------------
    def get_id(self):
        """ GET - Category: return category_id """
        return self.id

    def get_name(self):
        """ GET - Category: return name """
        return self.name

    def get_description(self):
        """ GET - Category: return description """
        return self.description

    def get_last_update(self):
        """ GET - Category: return last_update - last update time """
        return self.last_update

    def get_owner(self):
        """ GET - Category: return owner """
        return self.owner

    # -------------------- SETTERS --------------------
    def set_name(self, name):
        """ SET - Category: name """
        self.name = name

    def set_description(self, description):
        """ SET - Category: description """
        self.description = description

    def set_last_update(self):
        """ SET - Category: last_update - last update time"""
        self.last_update = self.set_time()

    def set_owner(self, owner):
        """ SET - Category: owner """
        self.owner = owner

    # -------------------- STATIC METHODS --------------------
    @staticmethod
    def set_time():
        """ Return current datetime """
        return datetime.datetime.now()
