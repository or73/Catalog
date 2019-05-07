"""
app_Item.py

@author: OR73
This File contains all modules to interact with Item Object
"""
# --------------- DataBase
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError

from database.database_setup import Item
from config import db_session


# --------------- Item FUNCTIONS ---------------
def get_item_id(item_name):
    """
    Search a item by its provided name, and if the item exists in the DB, then
    item._id is returned
    :param item_name: item name
    :return: item._id if item exists or None if does not exist
    """
    try:
        item = db_session.query(Item).filter_by(name=item_name).first()
        return item.get_id()
    except SQLAlchemyError:
        return None


def get_item_info(item_id):
    """
    Find an item searching in DB by its provided item_id
    :param item_id: item id to search in DB
    :return: item data
    """
    item = db_session.query(Item).filter_by(_id=item_id).first()
    return item


def get_all_item_create(order_type, amount):
    """
    :param order_type: 'asc' fos ascendant or 'desc' for descendant
    :param amount: amount of items for loading
    :return: query object
    """
    item_query = db_session.query(Item)
    if order_type == 'asc':
        return item_query.order_by(asc(Item.created)).limit(amount)
    elif order_type == 'desc':
        return item_query.order_by(desc(Item.created)).limit(amount)
    else:
        return None
