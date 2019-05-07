"""
app_DB.py

@author: OR73
This Class create a DataBase session
"""
# ------------------------ Environment
from dotenv import load_dotenv
# ------------------------ Data Base
from database_setup import Base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import os

# Environment
load_dotenv()


class DBSession:
    def __init__(self):
        # DB Session
        engine = create_engine(str(os.getenv('DB')), echo=True)
        Base.metadata.bind = engine
        session = sessionmaker(bind=engine)
        self.session = scoped_session(session)
        # self.session = session()

    def get_session(self):
        return self.session
