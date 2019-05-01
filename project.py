# ------------------------ Data Base
from database_setup import Base, Category, Item, item_category, User, user_category
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import asc, create_engine, desc
# ------------------------ HTTP Authorization
from flask import render_template_string
from flask import session as login_session
from flask_httpauth import HTTPBasicAuth   # python 3
# from flask.ext.httpauth import HTTPBasicAuth   # python 2.7
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import requests
import string

from flask import abort, Flask, jsonify, g, make_response, request, render_template, url_for
from functools import update_wrapper


auth = HTTPBasicAuth()

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# redis = Redis()
app = Flask(__name__)
CLIENT_ID_GMAIL = json.loads(open('client_secrets_gmail.json', 'r').read())['web']['client_id']
CLIENT_ID_FB = json.loads(open('client_secrets_fb.json', 'r').read())['web']['app_id']


# Create a state token to prevent request forgery.
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    client_secrets = {}
    with open('client_secrets_gmail.json') as f:
        client_secrets = json.load(f)
    print('client_secrets: ', client_secrets)
    # return 'The current session state is %s' % login_session['state']
    print('The current session state is %s' % login_session['state'])
    return render_template('login.html',
                           STATE=state,
                           secrets=client_secrets)


# --------------- CATEGORY
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
# <a class='cat_item_main_page' href='#'>{{ item.name }}
#   <span class='item_category'>({{ item.categories | safe }})</span>
# </a>
    for item in items_query:
        # Create categories property into item, to store all categories name
        item.categories = ''
        # Make a query in item_category table, by item._id
        item_category_query = session.query(item_category).filter_by(_item_id=item._id).all()
        print('%s: ' % item.name)
        # Loop in item_categories query, to catch item _id
        for category in item_category_query:
            print('\tcategory[0]: ', category[0])
            # Make a query in Category by _id, to catch the name
            category_query = session.query(Category).filter_by(_id=category[0]).one()
            # Update item.categories string
            if category_query:
                print('category_query.name: ', category_query.name)
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
    print('category1: ', category.name)

    if category:
        print('category2: ', category.name)
        # Load all category items
        items_query = session.query(item_category).filter_by(_category_id=category_id)
        items = []
        for item in items_query:
            print('item: ', item)
            print('item[0]: ', item[0])
            print('item[1]: ', item[1])
            items.append(session.query(Item).filter_by(_id=item[1]).one())
            print('items: ', items)
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


# --------------- ITEM
# Show an Item of a Category
@app.route('/catalog/category/<int:item_id>')
@app.route('/catalog/category/<int:item_id>/item/')
def showItem(item_id):
    print('--------------- showItem')
    item = getItemInfo(item_id)
    return render_template('showItem_public.html',
                           item=item)


# --------------- FUNCTIONS
def createUser(login_session):
    """
    Create 'createUser' function, which receives a 'login_session'
    and creates a new user in 'restaurantmenuwithusers.db' database,
    extracting all of the fields required to populate it with the
    information gathered from the 'login_session'.  It then return the 'user.id' of the new created user.
    :param login_session: login_session
    :return: user.id
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user._id


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
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0',
            port=5000)
