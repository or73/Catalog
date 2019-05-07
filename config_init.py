import config
# ------------------------ DB
from modules import app_DB

from flask import Flask
from flask import session as f_session

# Application
config.app = Flask(__name__)
# Flask session
config.session = f_session
# DB Session
config.db_session = (app_DB.DBSession()).get_session()
