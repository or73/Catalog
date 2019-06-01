"""
File Path: application/setup.py
Description: setup the App
This will have the function to create the App which will initialize the database and register all blueprints.
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask import flash, Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Init SQLAlchemy


def create_app():
    """Initialize the core application"""

    app = Flask(__name__)   # , instance_relative_config=True)
    app.config.from_object('config.Config')
    """ Load configuration """

    db.init_app(app)
    login_manager = LoginManager(app)  # Init LoginManager
    """ Initialize plugins """

    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth_bp.login'

    from application import UserMethod
    @login_manager.user_loader
    # def load_user(user_id):
    def load_user(session_token):
        # print('load_user - user_id - session_token: ', session_token)
        print('loading auth...')
        user_id = UserMethod.get_id_by_session_token(session_token)
        # print('loaded user_id: %s with token: %s ' % (user_id, session_token))
        # return user_id
        return UserMethod.load_user(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        """ Redirect unauthorized users to Login page"""
        flash('You must be logged in to view that page')
        return redirect(url_for('catalog_bp.index'))

    with app.app_context():
        """ Blueprints """
        from application import auth_bp, catalog_bp, category_bp, item_bp, user_bp
        """ Blueprint for Module routes in App """

        """" Register Blueprints """
        app.register_blueprint(auth_bp)
        app.register_blueprint(catalog_bp)
        app.register_blueprint(category_bp)
        app.register_blueprint(item_bp)
        app.register_blueprint(user_bp)

        from application import Auth, Catalog, Category, Item, User
        """Import the models so that sqlalchemy can detect them and create the DB """

        db.create_all()
        """ Create Tables from Models into the DB """
        return app
