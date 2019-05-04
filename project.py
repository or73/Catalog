# ------------------------ Environment
from dotenv import load_dotenv

# ------------------------ Data Base
from database_setup import Base, Category, Item, item_category, User, user_category
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import asc, create_engine, desc
# ------------------------ HTTP Authorization
from flask import session 
from flask_httpauth import HTTPBasicAuth   # python 3

# from flask.ext.httpauth import HTTPBasicAuth   # python 2.7
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.contrib.flask_util import UserOAuth2
import httplib2
import json
import os
import random
import requests
import string

from flask import abort, flash, Flask, jsonify, g, make_response
from flask import redirect, request, render_template, render_template_string, url_for
from flask_jsglue import JSGlue
from functools import update_wrapper

# Authorization & Authentication
auth = HTTPBasicAuth()
oauth2 = UserOAuth2()

# DB Session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Environment
load_dotenv()

# Application
app = Flask(__name__)

# Constants
GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')


# * * * * * * * * * * * * * * * * * * * * * * * *
# --------------- AUTHENTICATION ---------------
# * * * * * * * * * * * * * * * * * * * * * * * *

# Create a state token to prevent request forgery.
# Store it in the session for later validation
# http://localhost:5000/google/auth

# Login route
@app.route('/login/')
def showLogin():
    print('-------------- Login --------------')
    return render_template('login.html', gmail_client_id=GMAIL_CLIENT_ID)


# Disconnect based on provider
@app.route('/logout')
def logout():
    if 'provider' in session:
        # Delete the user's profile and the credentials stored by oauth2
        if session['provider'] == 'google':
            print('-------------- LOG OUT Gmail')
            gdisconnect()
            del session['access_token']
            del session['gmail_id']
        if session['provider'] == 'facebook':
            print('-------------- LOG OUT Facebook')
            fbdisconnect()
            del session['facebook_id']

        del session['email']
        del session['password']
        del session['picture']
        del session['profile']
        del session['provider']
        del session['username']

        session.modified = True
        # oauth2.storage.delete()

        # flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog', session=session))
    else:
        # flash("You were not logged out")
        return redirect(url_for('showCatalog', session=session))


@app.route('/login/<provider>', methods=['POST'])
def loginProvider(provider):
    print('-------------- PROVIDER LOGIN VALIDATION --------------')
    print('provider: %s' % provider)

    if request.method == 'POST':
        if provider == 'google':
            print('-------------- GOOGLE LOGIN --------------')
            print('---------- GOOGLE - login ----------')
            # STEP 1 - Parse the auth code
            print('STEP 1 - Parse auth code')
            auth_code = request.data   # request.json.get('auth_code')
            print('STEP 1 - Complete! - Auth Code Parsed')
            print('auth_code: ', auth_code)
            # STEP 2 - Exchange for a token
            print('STEP 2 - Exchange for a token')
            try:
                # Upgrade the authorization code into a credential object
                oauth_flow = flow_from_clientsecrets('client_secrets_gmail.json', scope='')
                oauth_flow.redirect_uri = 'postmessage'
                credentials = oauth_flow.step2_exchange(auth_code)
                print('credentials: ', credentials)
            except FlowExchangeError:
                response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
                response.header['Content-type'] = 'application/json'
                return response

            # Check that the access token is valid
            access_token = credentials.access_token
            url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
            h = httplib2.Http()
            result = json.loads(h.request(url, 'GET')[1])

            # If there was an error in the access token info, abort
            if result.get('error') is not None:
                response = make_response(json.dumps(result.get('error')), 500)
                response.headers['Content-type'] = 'application/json'
                return response

            print('STEP 2 - Complete! Access Token: %s' % credentials.access_token)

            # Verify that the access token is used for the intended user
            print('Verify that access token is used for the intended user')
            gmail_id = credentials.id_token['sub']
            if result['user_id'] != gmail_id:
                response = make_response(json.dumps('Token\'s user ID doesn\'t match given user ID'), 401)
                response.headers['Content-type'] = 'application/json'
                return response

            # Verify that the access token is valid for this app
            print('Verify that the access token is valid for this app')
            if result['issued_to'] != GMAIL_CLIENT_ID:
                response = make_response(json.dumps('Token\'s client ID does not match app\'s'), 401)
                response.headers['Content-type'] = 'application/json'
                return response

            stored_access_token = session.get('access_token')
            stored_gmail_id = session.get('gmail_id')
            if stored_access_token is not None and gmail_id == stored_gmail_id:
                response = make_response(json.dumps('Current user is already connected'), 200)
                response.headers['Content-type'] = 'application/json'
                return response

            # Store the access token in the session for later use
            print('Storing the access token in the session...')
            session['access_token'] = credentials.access_token
            session['gmail_id'] = gmail_id

            # STEP 3 - Find User or make a new one
            # Get user info
            print('STEP 3 - Get user info')
            userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
            params = {'access_token': credentials.access_token, 'alt': 'json'}
            answer = requests.get(userinfo_url, params=params)

            data = answer.json()
            print('*** data: ', data)

            session['email'] = data['email']
            session['password'] = str(os.getenv('DEFAULT_PWD'))
            session['picture'] = data['picture']
            session['profile'] = False
            session['provider'] = 'google'
            session['username'] = data['name']

            print('*** session: ', session)

            # see if user exists, if it doesn't create a new one
            user = getUserID(session['email'])

            if not user:
                print('User does not exist... creating new user...')
                user = createUser(session)   # User(username=name, picture=picture, email=email)
            print('STEP 3 - User Info Obtained')
            # STEP 4 - Create token
            print('STEP 4 - Create Token')
            token = user.generate_auth_token(600)
            print('token: ', token)
            print('STEP 4 - Token Created')

            # STEP 5 - Send back token to the client
            print('STEP 5 - Shows token, redirect web page')
            print(jsonify({'token': token.decode('ascii')}))
            # return redirect(url_for('showCatalogPrivate', session=session))
            print('STEP 5 - Token to return')
            return jsonify({'token': token.decode('ascii')})
        elif provider == 'facebook':
            print('-------------- FACEBOOK LOGIN --------------')
        else:
            print('-------------- USERNAME LOGIN --------------')
            username = request.form['username']
            password = request.form['password']
            print('username: %s \t password: %s' % (username, password))

            # Validate user data with Database
            user_query = getUserInfo_name(username)   # session.query(User).filter_by(username=username).one()

            if user_query:  # User exists
                print('The user %s exists...' % user_query.username)

                # Validate Password
                if verify_password(username, password):
                    print('Generate session ID')
                else:
                    print('Password invalid')
            else:  # User does not exist
                # Show message 'User does not exist'
                print('Show message: User does not exist')


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# DISCONNECT - Revoke a current user's token and reset their session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# * * * * * * * * * * * * * * * * * * * * *
# --------------- CATEGORY ---------------
# * * * * * * * * * * * * * * * * * * * * *

# Show all categories - PUBLIC
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    print('-------------- Initial route --------------')
    # Load all categories
    print('Loading all categories...')
    categories_query = db_session.query(Category).order_by(asc(Category.name))
    # Load all latest items
    print('Loading all 10 latest items')
    items_query = list(db_session.query(Item).order_by(desc(Item.created)).limit(10))

    for item in items_query:
        # Create categories property into item, to store all categories name
        item.categories = ''
        # Make a query in item_category table, by item._id
        item_category_query = db_session.query(item_category).filter_by(_item_id=item._id).all()
        # Loop in item_categories query, to catch item _id
        for category in item_category_query:
            # Make a query in Category by _id, to catch the name
            category_query = db_session.query(Category).filter_by(_id=category[0]).one()
            # Update item.categories string
            if category_query:
                item_str = ''
                item_str += '<a class="item_category"'
                item_str += 'href="{{ url_for(\'showCategory\', category_id=%s) }}">' % category_query._id
                item_str += '- %s</a>' % category_query.name

                item.categories += render_template_string(item_str)
    return render_template('showCatalog_public.html',
                           categories=categories_query,
                           items=items_query)


# Show all categories - PRIVATE
@app.route('/catalog/private/')
def showCatalogPrivate():
    print('-------------- Initial route --------------')
    # Load all categories
    print('Loading all categories...')
    categories_query = db_session.query(Category).order_by(asc(Category.name))
    # Load all latest items
    print('Loading all 10 latest items')
    items_query = list(db_session.query(Item).order_by(desc(Item.created)).limit(10))

    for item in items_query:
        # Create categories property into item, to store all categories name
        item.categories = ''
        # Make a query in item_category table, by item._id
        item_category_query = db_session.query(item_category).filter_by(_item_id=item._id).all()
        # Loop in item_categories query, to catch item _id
        for category in item_category_query:
            # Make a query in Category by _id, to catch the name
            category_query = db_session.query(Category).filter_by(_id=category[0]).one()
            # Update item.categories string
            if category_query:
                item_str = ''
                item_str += '<a class="item_category"'
                item_str += 'href="{{ url_for(\'showCategory\', category_id=%s) }}">' % category_query._id
                item_str += '- %s</a>' % category_query.name

                item.categories += render_template_string(item_str)
    return render_template('showCatalog.html',
                           categories=categories_query,
                           items=items_query)


# Show a Catalog Category
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/category/')
def showCategory(category_id):
    print('--------------- showCategory')
    print('category_id: ', category_id)

    # Validate if category_id exists
    category = db_session.query(Category).filter_by(_id=category_id).one()

    if category:
        # Load all category items
        items_query = db_session.query(item_category).filter_by(_category_id=category_id)
        items = []
        for item in items_query:
            items.append(db_session.query(Item).filter_by(_id=item[1]).one())
        return render_template('showCategory_public.html',
                               category=category.name,
                               items=items)
    else:  # Category does not exist
        print('Category does not exist')

        #items = session.query(MenuItem).filter_by(
        #    restaurant_id=restaurant_id).all()
        #if 'username' not in session or creator.id != session['user_id']:
        #    return render_template('publicmenu.html',
        #                           items=items,
        #                           restaurant=restaurant,
        #                           creator=creator)
        #else:
        #    return render_template('menu.html',
        #                           items=items,
        #                           restaurant=restaurant,
        #                           creator=creator)
        return


# * * * * * * * * * * * * * * * * * * *
# --------------- ITEM ---------------
# * * * * * * * * * * * * * * * * * * *

# Show an Item of a Category
@app.route('/catalog/category/<int:item_id>/')
@app.route('/catalog/category/<int:item_id>/item/')
def showItem(item_id):
    print('--------------- showItem')
    item = getItemInfo(item_id)
    return render_template('showItem_public.html',
                           item=item)


# * * * * * * * * * * * * * * * * * * * * *
# --------------- FUNCTIONS ---------------
# * * * * * * * * * * * * * * * * * * * * *

# --------------- User Functions ---------------
def createUser(user_data):
    """
    Create 'createUser' function, which receives a 'session'
    and creates a new user in 'restaurantmenuwithusers.db' database,
    extracting all of the fields required to populate it with the
    information gathered from the 'session'.  It then return the 'user.id' of the new created user.
    :param session: session
    :return: user.id
    """
    newUser = User(username=user_data['username'],
                   email=user_data['email'],
                   password=user_data['password'],
                   picture=user_data['picture'],
                   profile=user_data['profile'])
    # newUser['password'] = newUser.hash_password(session['password'])
    newUser.hash_password(session['password'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=user_data['email']).first()
    return user


def getUserID(email):
    """
    Search a user by its provided email, and if the user exists in the DB, then
    user._id is returned
    :param email: user email
    :return: user.id if user exists or None if does not exist
    """
    try:
        user = db_session.query(User).filter_by(email=email).first()
        return user._id
    except:
        return None


def getUserInfo_id(user_id):
    """
    Find a user searching in DB by its provided user_id
    :param user_id: user id to search in DB
    :return: user data
    """
    user = db_session.query(User).filter_by(_id=user_id).first()
    return user


def getUserInfo_name(user_name):
    """
        Find a user searching in DB by its provided username
        :param user_name: user name to search in DB
        :return: user data
    """
    user = db_session.query(User).filter_by(username=user_name).first()
    return user


@auth.verify_password
def verify_password(username, password):
    print('------- verify_password -------')
    print('username: %s\npassword: %s' % (username, password))
    user = getUserInfo_name(username)
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


# --------------- Category FUNCTIONS ---------------
def getCategory(category_id):
    """
        Search a category by its provided _id, and if the category exists in the DB, then
        category is returned
        :param category_id: category _id
        :return: category if item exists or None if does not exist
    """
    try:
        category = db_session.query(Category).filter_by(_id=category_id).one()
        return category
    except:
        return None


def getCategoryID(category_name):
    """
        Search a category by its provided name, and if the category exists in the DB, then
        category._id is returned
        :param category_name: category name
        :return: category._id if item exists or None if does not exist
    """
    try:
        category = db_session.query(Category).filter_by(name=category_name).one()
        return category._id
    except:
        return None


# --------------- Item FUNCTIONS ---------------
def getItemID(item_name):
    """
        Search a item by its provided name, and if the item exists in the DB, then
        item._id is returned
        :param item_name: item name
        :return: item._id if item exists or None if does not exist
    """
    try:
        item = db_session.query(Item).filter_by(name=item_name).one()
        return item._id
    except:
        return None


def getItemInfo(item_id):
    """
        Find an item searching in DB by its provided item_id
        :param item_id: item id to search in DB
        :return: item data
    """
    item = db_session.query(Item).filter_by(_id=item_id).one()
    return item


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')   # 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0',
            port=5000)
