"""
File Path: application/modules/user/methods.py
Description: Category methods for App - Define Category methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask_login import current_user

# from setup import db
from application.setup import db
from .models import User


class UserMethod:
    @staticmethod
    def create_user(authenticated, email, first_name, last_name, password, picture,
                    profile, provider, session_token, username):
        """
        Create 'createUser' function, which receives a 'session'
        and creates a new user in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'.
        It then return the 'user.id' of the new created user.
        :param authenticated
        :param email
        :param first_name
        :param last_name
        :param password
        :param picture
        :param profile
        :param provider
        :param session_token
        :param username
        :return: user.id
        """
        print('-------------------- user-methods: create_user')
        new_user = User(authenticated=authenticated,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                        picture=picture,
                        profile=profile,
                        provider=provider,
                        session_token=session_token,
                        username=username)
        db.session.add(new_user)
        db.session.commit()
        # Validate if user was created
        user = User.query.filter_by(email=email).first()
        if user:
            return user.id
        else:
            return 'User could not be created'

    @staticmethod
    def get_current_user_id():
        """ Return current_user_id """
        if current_user.id:
            print('current_user_id: ', current_user.id)
            return current_user.id
        print('current.user: ', current_user)
        return None

    @staticmethod
    def get_email_by_id(user_id):
        """ return user_email by its user_id"""
        print('-------------------- User - get_email_by_id')
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.get_email()
        return None

    @staticmethod
    def get_email_by_username(user_username):
        """ return user_email by its user_username """
        print('-------------------- User - get_email_by_username')
        user = User.query.filter_by(username=user_username).first()
        if user:
            return user.get_email()
        return None

    @staticmethod
    def get_id_by_email(user_email):
        """ return user_id by its user_email """
        print('-------------------- User - get_id_by_email')
        user = User.query.filter_by(email=user_email).first()
        if user:
            return user.get_id()
        return None

    @staticmethod
    def get_id_by_session_token(session_token):
        """ return user_id by its session_token """
        print('-------------------- User - get_id_by_username')
        user = User.query.filter_by(session_token=session_token).first()
        if user:
            return user.get_user_id()
        return None

    @staticmethod
    def get_id_by_username(user_username):
        """ return user_id by tis user_username """
        print('-------------------- User - get_id_by_username')
        user = User.query.filter_by(usename=user_username).first()
        if user:
            return user.get_user_id()
        return None

    @staticmethod
    def get_session_token_by_id(user_id):
        """ return session_token by its user_id """
        print('-------------------- User - get_session_token_by_id')
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.get_session_token()
        return None

    @staticmethod
    def get_session_token_by_email(user_email):
        """ return session_token by its user_email """
        print('-------------------- User - get_session_token_by_email')
        return (User.query.filter_by(email=user_email).first()).get_session_token()

    @staticmethod
    def get_session_token_by_username(user_username):
        """ return session_token by its user_username """
        print('-------------------- User - get_session_token_by_username')
        return (User.query.filter_by(usename=user_username).first()).get_session_token()

    @staticmethod
    def get_user_by_id(user_id):
        """ return user object by its user_id """
        print('-------------------- User - get_user_by_id')
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(user_email):
        """ return user object by its user_email """
        print('-------------------- User - get_user_by_email')
        return User.query.filter_by(email=user_email).first()

    @staticmethod
    def get_user_by_session_token(user_session_token):
        """ return user object by its user_session_token """
        print('-------------------- User - get_user_by_session_token')
        return User.query.filter_by(session_token=user_session_token).first()

    @staticmethod
    def get_user_by_username(user_username):
        """ return user object by its user_username """
        print('-------------------- User - get_user_by_username')
        return User.query.filter_by(username=user_username).first()

    @staticmethod
    def get_username_by_id(user_id):
        """ return user_username by its user_id """
        print('-------------------- User - get_username_by_id')
        return (User.query.filter_by(id=user_id).first()).get_username()

    @staticmethod
    def get_username_by_email(user_email):
        """ return user_username by its user_email """
        print('-------------------- User - get_username_by_email')
        return (User.query.filter_by(email=user_email).first()).get_username()

    @staticmethod
    def get_username_by_session_token(user_session_token):
        """ return user_username by its user_session_token """
        print('-------------------- User - get_username_by_session_token')
        return (User.query.filter_by(email=user_session_token).first()).get_username()

    @staticmethod
    def load_user(user_id):
        return User.query.get(int(user_id))

    @staticmethod
    def validate_owner(user_id):
        """ return a comparison between provided user_id and current session user_id """
        print('-------------------- User - validate_owner')
        owner = User.query.filter_by(id=UserMethod.get_current_user_id()).first()
        return owner == user_id
