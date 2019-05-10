"""
app_User_Session.py

@author: OR73
This File contains all Users registered in a session
"""
# --------------- DataBase
from sqlalchemy.exc import SQLAlchemyError
# --------------- HTTP Authorization
from flask_httpauth import HTTPBasicAuth

import random
import string

from database.database_setup import UserSession
from config import db_session, session

# Authorization & Authentication
auth = HTTPBasicAuth()


# --------------- User Functions ---------------
def create_user(user_data):
    """
    Create 'createUser' function, which receives a 'session'
    and creates a new user in the database, extracting all
    of the fields required to populate it with the information
    gathered from the 'session'.
    It then return the 'user.id' of the new created user.
    :param user_data: User data
    :return: user.id
    """
    new_user = UserSession(username=user_data['username'],
                           email=user_data['email'],
                           profile=user_data['profile'])
    db_session.add(new_user)
    db_session.commit()
    user = get_user(user_data['email'])
    # db_session.query(UserSession).filter_by(email=user_data['email']).first()
    return user


def del_user(user_id):
    """
    Search a user by its provided email, and if the user exists in the DB, then
    User is removed from UserSession table
    :param email: user email
    :return: True if user has been removed or False if not
    """
    try:
        db_session.query(UserSession).filter_by(_id=user_id).delete()
        db_session.commit()
        user_deleted = get_user_info_id(user_id)
        if user_deleted:
            return False
        else:
            return True
    except SQLAlchemyError:
        return False


def get_user(email):
    """
    Search a user by its provided email, and if the user exists in the DB, then
    User object is returned
    :param email: user email
    :return: User Object if user exists or None if does not exist
    """
    try:
        user = db_session.query(UserSession).filter_by(email=email).first()
        if user:
            return user
        else:
            return False
    except SQLAlchemyError:
        return None


def get_user_id(email):
    """
    Search a user by its provided email, and if the user exists in the DB, then
    user._id is returned
    :param email: user email
    :return: user.id if user exists or None if does not exist
    """
    try:
        user = db_session.query(UserSession).filter_by(email=email).first()
        if user:
            return user._id
        else:
            return False
    except SQLAlchemyError:
        return None


def get_user_info_id(user_id):
    """
    Find a user searching in DB by its provided user_id
    :param user_id: user id to search in DB
    :return: user data
    """
    user = db_session.query(UserSession).filter_by(_id=user_id).first()
    return user


def get_user_info_name(user_name):
    """
    Find a user searching in DB by its provided username
    :param user_name: user name to search in DB
    :return: user data
    """
    user = db_session.query(UserSession).filter_by(username=user_name).first()
    return user
