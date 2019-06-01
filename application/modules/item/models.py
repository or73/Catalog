"""
File Path: application/modules/item/models.py
Description: Item models for App - Define Item models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from ..base_model import BaseModel
from crud import CRUDMixin


class Item(CRUDMixin, db.Model):   # BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    # Item
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.String(15))

    # Item Control
    last_update = db.Column(db.DateTime)

    # Owner
    owner = db.Column(db.Integer)

# -------------------- INIT --------------------
    def __init__(self, name, description, price, owner):
        # User session init/end fields
        self.name = name
        self.description = description
        self.price = price
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
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'owner': self.owner,
            'last_update': self.last_update
        }

    # -------------------- GETTERS --------------------
    def get_id(self):
        """ GET - Item: return item_id """
        return self.id

    def get_name(self):
        """ GET - Item: return name """
        return self.name

    def get_description(self):
        """ GET - Item: return description """
        return self.description

    def get_last_update(self):
        """ GET - Item: return last_update - last update time """
        return self.last_update

    def get_owner(self):
        """ GET - Item: return owner """
        return self.owner

    def get_price(self):
        """ GET - Item: return price """
        return self.price

    # -------------------- SETTERS --------------------
    def set_name(self, name):
        """ SET - Item: name """
        self.name = name

    def set_description(self, description):
        """ SET - Item: description """
        self.description = description

    def set_last_update(self):
        """ SET - Item: last_update - last update time"""
        self.last_update = self.set_time()

    def set_owner(self, owner):
        """ SET - Item: owner """
        self.owner = owner

    def set_price(self, price):
        """ SET - Item: price """
        self.price = price

    # -------------------- STATIC METHODS --------------------
    @staticmethod
    def set_time():
        """ Return current datetime """
        return datetime.datetime.now()
