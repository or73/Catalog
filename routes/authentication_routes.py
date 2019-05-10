"""
authentication_routes.py

@author: OR73
This File contains all routes required for user authentication
"""
import httplib2
import json
import random
import requests
import string

# ------------------------ Environment
from dotenv import load_dotenv
import os

from flask import Blueprint, jsonify, make_response, redirect, render_template, request, url_for
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
# ------------------------ HTTP Authorization
from flask_httpauth import HTTPBasicAuth  # python 3
from oauth2client.contrib.flask_util import UserOAuth2

from modules import app_User, app_User_Session

from config import session

load_dotenv()
authentication_routes = Blueprint('authentication_routes', __name__, template_folder='templates')

GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_SECRET = os.getenv('FACEBOOK_APP_SECRET')

# Authorization & Authentication
auth = HTTPBasicAuth()
oauth2 = UserOAuth2()

"""
 * * * * * * * * * * * * * * * * * * * * * * * *
 --------------- AUTHENTICATION ---------------
 * * * * * * * * * * * * * * * * * * * * * * * *
"""
# Create a state token to prevent request forgery.
# Store it in the session for later validation
# http://localhost:5000/google/auth

# Login route
@authentication_routes.route('/login/')
def show_login():
    print('-------------- Login --------------')
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    session['state'] = state
    print('session: ', session)
    print('GMAIL_CLIENT_ID: ', GMAIL_CLIENT_ID)
    print('facebook_app_id: ', FACEBOOK_APP_ID)
    return render_template('login.html', gmail_client_id=GMAIL_CLIENT_ID, facebook_app_id=FACEBOOK_APP_ID, state=state)


# Disconnect based on provider
@authentication_routes.route('/logout')
def logout():
    if 'username' in session:
        # Remove user from UserSession table
        if app_User_Session.del_user(session['user_id']):
            print('User session has been removed successfully...')
        else:
            print('User session could not been removed...')

        # Delete the user's profile and the credentials stored by oauth2
        if session['provider'] == 'google':
            print('-------------- LOGOUT Gmail')
            g_disconnect()
            del session['access_token']
            del session['gmail_id']
        if session['provider'] == 'facebook':
            print('-------------- LOGOUT Facebook')
            fb_disconnect()
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
        return redirect(url_for('catalog_routes.show_catalog', session=session))
    else:
        # flash("You were not logged out")
        return redirect(url_for('catalog_routes.show_catalog', session=session))


@authentication_routes.route('/login/<provider>', methods=['POST'])
def login_provider(provider):
    print('-------------- PROVIDER LOGIN VALIDATION --------------')
    print('provider: %s' % provider)

    if request.method == 'POST':
        if provider == 'google':
            print('-------------- GOOGLE LOGIN --------------')
            print('request: ', request)
            print('request.args: ', request.args)
            print('request.args.get(state): ', request.args.get('state'))
            print('session[state]: ', session['state'])
            # Validate state token
            if request.args.get('state') != session['state']:
                response = make_response(json.dumps('Invalid state parameter'), 400)
                response.headers['Content-type'] = 'application/json'
                return response
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
                oauth_flow = flow_from_clientsecrets('secrets/client_secrets_gmail.json', scope='')
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
            user = app_User.get_user(session['email'])  # getUserID(session['email'])

            if not user:
                print('User does not exist... creating new user...')
                user = app_User.create_user(session)

            # Validate if user session exists
            user_session_id = app_User_Session.get_user_id(session['email'])
            if not user_session_id and user:
                print('User session does not exist... creating a new session...')
                user_session_id = app_User_Session.create_user(session)
            session['user_id'] = user_session_id

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
            # graph = facebook.GraphAPI(access_token=FACEBOOK_APP_ID, version='2.8')
            # print('graph: ', graph)
            if request.args.get('state') != session['state']:
                response = make_response(json.dumps('Invalid state parameter'), 400)
                response.headers['Content-type'] = 'application/json'
            print('STEP 1. - Parse auth code')
            auth_code = request.data.decode('utf-8')  # request.data
            print('auth_code: ', auth_code)
            url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&' \
                  'client_id=%s&' \
                  'client_secret=%s&' \
                  'fb_exchange_token=%s' % (FACEBOOK_APP_ID, FACEBOOK_SECRET, auth_code)
            print('STEP 2. - url: ', url)
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]
            result = result.decode('utf-8')
            print('STEP 3. - result: ', result)
            # Use auth_code to get user info form API
            userinfo_url = 'https://graph.facebook.com/v.2.8/me'
            """
            Due to the formatting for the result from the server token exchange we have to
            split the token first on commas and select the first index which gives us the key : value
            for the server access token then we split it on colons to pull out the actual token value
            and replace the remaining quotes with nothing so that it can be used directly in the graph
            """
            token = result.split(',')[0].split(':')[1].replace('"', '')
            print('STEP 4. - token: ', token)

            url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
            print('url: ', url)
            h = httplib2.Http()
            print('h: ', h)
            result = h.request(url, 'GET')[1]
            print('result: ', result)
            data = json.loads(result)
            print('1. data: ', data)

            # Get user picture
            url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
            h = httplib2.Http()
            result = h.request(url, 'GET')[1]
            data_picture = json.loads(result)
            print('2. data_picture: ', data_picture)

            # The token must be stored in the login_session in order to properly logout
            session['access_token'] = token
            session['email'] = data['email']
            session['facebook_id'] = data['id']
            session['password'] = str(os.getenv('DEFAULT_PWD'))
            session['picture'] = data_picture['data']['url']
            session['profile'] = False
            session['provider'] = 'facebook'
            session['username'] = data['name']

            print('STEP 4. session: ', session)

            # Validate if user exists
            user_id = app_User.get_user_id(session['email'])

            # if user_id does not exist, then create a new User
            if not user_id:
                print('User does not exist... creating new user...')
                user_id = app_User.create_user(session)

            # Validate if user session exists
            user_session_id = app_User_Session.get_user_id(session['email'])
            if not user_session_id and user_id:
                print('User session does not exist... creating user session...')
                user_session_id = app_User_Session.create_user(session)
            session['user_id'] = user_session_id

            # STEP 5 - Create token
            print('STEP 5 - Create Token')
            user = app_User.get_user_info_id(user_id)
            token = user. generate_auth_token(600)
            print('token: ', token)
            print('STEP 6 - Token Created')

            # STEP 5 - Send back token to the client
            print('STEP 7 - Shows token, redirect web page')
            print(jsonify({'token': token.decode('ascii')}))
            # return redirect(url_for('showCatalogPrivate', session=session))
            print('STEP 7 - Token to return')
            return jsonify({'token': token.decode('ascii')})
        else:
            print('-------------- USERNAME LOGIN --------------')
            username = request.form['username']
            password = request.form['password']
            print('username: %s \t password: %s' % (username, password))

            # Validate user data with Database
            user_query = app_User.get_user_info_name(username)
            # getUserInfo_name(username)   # session.query(User).filter_by(username=username).one()

            if user_query:  # User exists
                print('The user %s exists...' % user_query.username)

                # Validate Password
                # if verify_password(username, password):
                if app_User.verify_password(username, password):
                    print('Generate session ID')
                else:
                    print('Password invalid')
            else:  # User does not exist
                # Show message 'User does not exist'
                print('Show message: User does not exist')


@authentication_routes.route('/fb_disconnect')
def fb_disconnect():
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# DISCONNECT - Revoke a current user's token and reset their session
@authentication_routes.route('/g_disconnect')
def g_disconnect():
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
