# ------------------------ Environment
from dotenv import load_dotenv

# ------------------------ Data Base
from database_setup import Base, Category, Item, item_category, User, user_category
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import asc, create_engine, desc
# ------------------------ HTTP Authorization
from flask import session as login_session
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

from flask import abort, Flask, jsonify, g, make_response
from flask import redirect, request, render_template, render_template_string, url_for
from flask_jsglue import JSGlue
from functools import update_wrapper


auth = HTTPBasicAuth()
engine = create_engine('sqlite:///catalog.db')
oauth2 = UserOAuth2()
load_dotenv()

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# redis = Redis()
app = Flask(__name__)
GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')   # json.loads(open('client_secrets_gmail.json', 'r').read())['web']['client_id']
# print('Facebook Client Secret: ', os.getenv('FB_APP_SECRET'))

# --------------- Initialize the OAuth2 helper
# oauth2.init_app(
#    app,
#    scopes=['email', 'profile'],
#    authorize_callback=_request_user_info
# )

# * * * * * * * * * * * * * * * * * * * * * * * *
# --------------- AUTHENTICATION ---------------
# * * * * * * * * * * * * * * * * * * * * * * * *

# Create a state token to prevent request forgery.
# Store it in the session for later validation
# http://localhost:5000/google/auth
@app.route('/login/')
def showLogin():
    print('-------------- Login --------------')
    return render_template('login.html', gmail_client_id=GMAIL_CLIENT_ID)


@app.route('/logout')
def logout():
    # Delete the user's profile and the credentials stored by oauth2
    # del session['profile']
    # session.modified = True
    # oauth2.storage.delete()
    # return render_template_string('showCatalog.html')

    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print('access_token: ', access_token)
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print('result[status]: ', result['status'])

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCatalog'))   # render_template('showCatalog_public.html')  # response   #return render_template('showCatalog_public.html')   # response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login/<provider>', methods=['POST'])
def loginProvider(provider):
    print('-------------- PROVIDER LOGIN VALIDATION --------------')
    print('provider: %s' % provider)

    if request.method == 'POST':
        if provider == 'google':
            print('-------------- GOOGLE LOGIN --------------')
            print('---------- GOOGLE - login ----------')
            # STEP 1 - Parse the auth code
            auth_code = request.data # request.json.get('auth_code')
            # STEP 2 - Exchange for a token
            try:
                # Upgrade the authorization code into a credential object
                oauth_flow = flow_from_clientsecrets('client_secrets_gmail.json', scope='')
                oauth_flow.redirect_uri = 'postmessage'
                credentials = oauth_flow.step2_exchange(auth_code)
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

            print('Step 2 Complete! Access Token: %s' % credentials.access_token)

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
                response = make_response(json.dumps('Token\'s client ID does not march app\'s'), 401)
                response.headers['Content-type'] = 'application/json'
                return response

            stored_access_token = login_session.get('access_token')
            stored_gmail_id = login_session.get('gmail_id')
            if stored_access_token is not None and gmail_id == stored_gmail_id:
                response = make_response(json.dumps('Current user is already connected'), 200)
                response.headers['Content-type'] = 'application/json'
                return response

            # Store the access token in the session for later use
            print('Storing the access token in the session...')
            login_session['access_token'] = credentials.access_token
            login_session['gmail_id'] = gmail_id

            # STEP 3 - Find User or make a new one
            # Get user info
            print('Get user info')
            userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
            params = {'access_token': credentials.access_token, 'alt': 'json'}
            answer = requests.get(userinfo_url, params=params)

            data = answer.json()

            login_session['username'] = data['name']
            login_session['picture'] = data['picture']
            login_session['email'] = data['email']
            login_session['profile'] = False
            login_session['password'] = str(os.getenv('DEFAULT_PWD'))

            # see if user exists, if it doesn't make a new one
            user = getUserID(login_session['email'])   # session.query(User).filter_by(email=email).first()

            print('login_session: ', login_session)

            if not user:
                print('Use does not exist... creating new user...')
                user = createUser(login_session)   # User(username=name, picture=picture, email=email)

            # STEP 4 - Make token
            token = user.generate_auth_token(600)
            print('token: ', token)

            # STEP 5 - Send back token to the client
            return jsonify({'token': token.decode('ascii')})
        elif provider == 'facebook':
            print('-------------- FACEBOOK LOGIN --------------')
        else:
            print('-------------- USERNAME LOGIN --------------')
            username = request.form['username']
            password = request.form['password']
            print('username: %s \t password: %s' % (username, password))

            # Validate user data with Database
            user_query = session.query(User).filter_by(username=username).one()

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


# * * * * * * * * * * * * * * * * * * * * *
# --------------- CATEGORY ---------------
# * * * * * * * * * * * * * * * * * * * * *

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    print('-------------- Initial route --------------')
    # Load all categories
    print('Loading all categories...')
    categories_query = session.query(Category).order_by(asc(Category.name))
    # Load all latest items
    print('Loading all 10 latest items')
    items_query = list(session.query(Item).order_by(desc(Item.created)).limit(10))

    for item in items_query:
        # Create categories property into item, to store all categories name
        item.categories = ''
        # Make a query in item_category table, by item._id
        item_category_query = session.query(item_category).filter_by(_item_id=item._id).all()
        # Loop in item_categories query, to catch item _id
        for category in item_category_query:
            # Make a query in Category by _id, to catch the name
            category_query = session.query(Category).filter_by(_id=category[0]).one()
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


# Show a Catalog Category
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/category/')
def showCategory(category_id):
    print('--------------- showCategory')
    print('category_id: ', category_id)

    # Validate if category_id exists
    category = session.query(Category).filter_by(_id=category_id).one()

    if category:
        # Load all category items
        items_query = session.query(item_category).filter_by(_category_id=category_id)
        items = []
        for item in items_query:
            items.append(session.query(Item).filter_by(_id=item[1]).one())
        return render_template('showCategory_public.html',
                               category=category.name,
                               items=items)
    else:  # Category does not exist
        print('Category does not exist')

        #items = session.query(MenuItem).filter_by(
        #    restaurant_id=restaurant_id).all()
        #if 'username' not in login_session or creator.id != login_session['user_id']:
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
def createUser(login_session):
    """
    Create 'createUser' function, which receives a 'login_session'
    and creates a new user in 'restaurantmenuwithusers.db' database,
    extracting all of the fields required to populate it with the
    information gathered from the 'login_session'.  It then return the 'user.id' of the new created user.
    :param login_session: login_session
    :return: user.id
    """
    newUser = User(username=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'],
                   profile=login_session['profile'])
    newUser.password = newUser.hash_password(login_session['password'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user


def getUserID(email):
    """
    Search a user by its provided email, and if the user exists in the DB, then
    user._id is returned
    :param email: user email
    :return: user.id if user exists or None if does not exist
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user._id
    except:
        return None


def getUserInfo(user_id):
    """
    Find a user searching in DB by its provided user_id
    :param user_id: user id to search in DB
    :return: user data
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


@auth.verify_password
def verify_password(username, password):
    print('------- verify_password -------')
    print('username: %s\npassword: %s' % (username, password))
    user = session.query(User).filter_by(username=username).first()
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


# --------------- Item FUNCTIONS ---------------
def getItemID(item_name):
    """
        Search a item by its provided name, and if the item exists in the DB, then
        item._id is returned
        :param item_name: item name
        :return: item._id if item exists or None if does not exist
        """
    try:
        item = session.query(Item).filter_by(name=item_name).one()
        return item._id
    except:
        return None


def getItemInfo(item_id):
    """
        Find an item searching in DB by its provided item_id
        :param item_id: item id to search in DB
        :return: item data
    """
    item = session.query(Item).filter_by(_id=item_id).one()
    return item


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')   # 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0',
            port=5000)
