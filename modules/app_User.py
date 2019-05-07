"""
app_User.py

@author: OR73
This File contains all modules to interact with User Object
"""
# --------------- DataBase
from sqlalchemy.exc import SQLAlchemyError
# --------------- HTTP Authorization
from flask_httpauth import HTTPBasicAuth

import random
import string

from database.database_setup import User
from config import db_session, session

# Constants
SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

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
    new_user = User(username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    picture=user_data['picture'],
                    profile=user_data['profile'])
    new_user.hash_password(user_data['password'])
    db_session.add(new_user)
    db_session.commit()
    user = db_session.query(User).filter_by(email=user_data['email']).first()
    return user


def get_user_id(email):
    """
    Search a user by its provided email, and if the user exists in the DB, then
    user._id is returned
    :param email: user email
    :return: user.id if user exists or None if does not exist
    """
    try:
        user = db_session.query(User).filter_by(email=email).first()
        if user:
            return user.get_id()
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
    user = db_session.query(User).filter_by(_id=user_id).first()
    return user


def get_user_info_name(user_name):
    """
    Find a user searching in DB by its provided username
    :param user_name: user name to search in DB
    :return: user data
    """
    user = db_session.query(User).filter_by(username=user_name).first()
    return user


@auth.verify_password
def verify_password(self, username, password):
    print('------- verify_password -------')
    print('username: %s\n password: %s' % (username, password))
    user = self.getUserInfo_name(username)
    print('user: ', type(user))

    if not user:
        print('User not found')
        return False
    elif not user.verify_password(password):
        print('Unable to verify password')
        return False
    # g.user = user
    print('The user has been validated successfully...')
    return True
