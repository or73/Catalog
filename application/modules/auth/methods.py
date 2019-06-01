"""
File Path: application/modules/auth/methods.py
Description: Auth methods for App - Define auth/login methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from flask_login import current_user

from setup import db
from .models import Auth
from ..user import UserMethod


class AuthMethod:
    @staticmethod
    def create_auth(user_id):
        """
        Create 'createUser' function, which receives a 'session'
        and creates a new user in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'.
        It then return the 'user.id' of the new created user.
        :param user_id: User id
        :return: auth
        """
        print('-------------------- create_auth')
        new_auth = Auth(user_id=user_id)
        """ Create new_auth """
        db.session.add(new_auth)
        """ Add new_auth to DB """
        db.session.commit()
        """ Commit Add operation to DB """

        """ Validate if Auth was created, if True the return Auth, else return None """
        auth_validation = Auth.query.filter_by(user_id=user_id).first()
        if auth_validation:
            print('Auth session has been created...')
            return auth_validation
        print('Auth session could not be created...')
        return None

    @staticmethod
    def dump_datetime(value):
        """ Deserialize datetime object into string form for JSON processing """
        if value is None:
            return None
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_all_in_dictionary():
        """ Return a dictionary with username, login/logout time in string format """
        all_auth = Auth.query.order_by(Auth.user_id).all()
        """ All auth login/logout events """

        login_logout = {}
        """ Dictionary to return """

        for auth in all_auth:
            auth_user = UserMethod.get_user_by_id(auth.user_id)
            login = auth.get_login_time()
            logout = None
            if auth.logout_time is None:
                duration = datetime.datetime.now() - login
            else:
                logout = datetime.datetime.now()
                duration = logout - login

            login_logout[auth_user.get_username()] = {
                'login': AuthMethod.dump_datetime(login),
                'logout': AuthMethod.dump_datetime(logout),
                'duration': duration
            }
        return login_logout

    @staticmethod
    def get_current_user_id():
        """ Return current_user_id """
        if current_user.id:
            print('current_user_id: ', current_user.id)
            return current_user.id
        print('current.user: ', current_user)
        return None

    @staticmethod
    def get_all_login_time_of_user(user_id):
        """ Return all login times of user_id """
        return Auth.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_login_time_of_users_in_period_of_time(start_time, end_time):
        """ Return all login times of users in a range of time """
        return Auth.query.filter(Auth.login_time >= start_time, Auth.login_time <= end_time).all()

    @staticmethod
    def get_all_logout_time_of_user(user_id):
        """ Return all logout times of user_id """
        return Auth.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_logout_time_of_user_in_period_of_time(start_time, end_time):
        """ Return all logout times of users in a range of time """
        return Auth.query.filter(Auth.logout_time >= start_time, Auth.logout_time <= end_time).all()

    @staticmethod
    def get_login_time_of_user(user_id):
        """ Return login_time of user_id """
        return (Auth.query.filter_by(user_id=user_id).first()).get_login_time()

    @staticmethod
    def get_logout_time_of_user(user_id):
        """ Return logout_time of user_id """
        return (Auth.query.filter_by(user_id=user_id).first()).get_logout_time()

    @staticmethod
    def get_first_link_by_user_id(user_id):
        return Auth.query.filter_by(user_id=user_id).order_by(Auth.login_time.desc()).first()

    # -------------------------- USER METHODS
    @staticmethod
    def user_method_create_user(authenticated, email, first_name, last_name, password, picture,
                                profile, provider, session_token, username):
        """ Return a new User """
        return UserMethod.create_user(authenticated=authenticated, email=email,
                                      first_name=first_name, last_name=last_name,
                                      password=password, picture=picture,
                                      profile=profile, provider=provider,
                                      session_token=session_token, username=username)

    @staticmethod
    def user_method_get_id_by_session_token(session_token):
        """ Return User_id by session_token """
        return UserMethod.get_id_by_session_token(session_token)

    @staticmethod
    def user_method_get_user_by_id(user_id):
        """ Return User by its id """
        return UserMethod.get_user_by_id(user_id)

    @staticmethod
    def user_method_get_user_by_email(email):
        """ Return User by its email """
        return UserMethod.get_user_by_email(email)
