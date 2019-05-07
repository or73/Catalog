"""
app_Category.py

@author: OR73
This File contains all modules to interact with Cateogory Object
"""
# --------------- DataBase
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError

from database.database_setup import Category, item_category
from config import db_session


# --------------- Category FUNCTIONS ---------------
def get_category(category_id):
    """
    Search a category by its provided _id, and if the category exists in the DB, then
    category is returned
    :param category_id: category _id
    :return: category if item exists or None if does not exist
    """
    try:
        category = db_session.query(Category).filter_by(_id=category_id).first()
        return category
    except SQLAlchemyError:
        return None


def get_category_id(category_name):
    """
    Search a category by its provided name, and if the category exists in the DB, then
    category._id is returned
    :param category_name: category name
    :return: category._id if item exists or None if does not exist
    """
    try:
        category = db_session.query(Category).filter_by(name=category_name).first()
        return category.get_id()
    except SQLAlchemyError:
        return None


def get_all_categories_name(order_type):
    """
    :param order_type:
    :return:
    """
    category_query = db_session.query(Category)
    if order_type == 'asc':
        return category_query.order_by(asc(Category.name))
    elif order_type == 'desc':
        return category_query.order_by(desc(Category.name))
    else:
        return None


def get_all_category_items(item_id):
    category_items = db_session.query(item_category).filter_by(_item_id=item_id).all()
    return category_items
