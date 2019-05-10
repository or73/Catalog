import config
# ------------------------ DB
from modules import app_DB

from flask import Flask, g
from flask import session as f_session
from flask_httpauth import HTTPBasicAuth   # python 3

# Application
config.app = Flask(__name__)
# Flask session
config.session = f_session
# DB Session
config.db_session = (app_DB.DBSession()).get_session()
# Authentication
config.g = g
# Authentication
config.auth = HTTPBasicAuth()
