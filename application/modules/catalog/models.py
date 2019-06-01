"""
File Path: application/modules/catalog/models.py
Description: Catalog models for App - Define Catalog models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from ..base_model import BaseModel
from crud import CRUDMixin


class Catalog(CRUDMixin, db.Model):   # BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    # Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    # Item
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'))
    # Catalog Control
    last_update = db.Column(db.DateTime)

# -------------------- INIT --------------------
    def __init__(self, category_id, item_id):
        # User session init/end fields
        self.category_id = category_id
        self.item_id = item_id
        self.last_update = self.set_time()

    def __repr__(self):
        return '<Catalog {}>'.format(self.id)

    # -------------------- PROPERTIES --------------------
    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        return {
            'id': self.id,
            'category_id': self.category_id,
            'item_id': self.item_id,
            'last_update': self.last_update
        }

    # -------------------- GETTERS --------------------
    def get_id(self):
        """ GET - Catalog: return  catalog_id """
        return self.id

    def get_category_id(self):
        """ GET - Catalog: return category_id """
        return self.category_id

    def get_item_id(self):
        """ GET - Catalog: return last_update - last update time """
        return self.login_time

    # -------------------- SETTERS --------------------
    def set_category_id(self, category_id):
        """ SET - Catalog: category_id """
        self.category_id = category_id

    def set_last_update(self):
        """ SET - Catalog: : last_update - last update time """
        self.last_update = self.set_time()

        # -------------------- STATIC METHODS --------------------
    @staticmethod
    def set_time():
        """ Return current datetime """
        return datetime.datetime.now()
