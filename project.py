"""
project.py

@author: OR73
This is the main project File
"""

import os
import config
import config_init
# ------------------------ Environment
from dotenv import load_dotenv

# Routes
from routes.authentication_routes import authentication_routes
from routes.catalog_routes import catalog_routes
from routes.category_routes import category_routes
from routes.item_routes import item_routes

# Environment
load_dotenv()

# Routes
config.app.register_blueprint(authentication_routes)
config.app.register_blueprint(catalog_routes)
config.app.register_blueprint(category_routes)
config.app.register_blueprint(item_routes)

if __name__ == '__main__':
    config.app.secret_key = os.getenv('SECRET_KEY')
    config.app.debug = True
    config.app.run(host=os.getenv('HOST'),
                   port=int(os.getenv('PORT')))
