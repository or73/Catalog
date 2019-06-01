# application/config.py
"""Config class"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration vars"""

    # General Config
    DEFAULT_PWD: str = os.environ.get('DEFAULT_PWD')

    # Constants - Google
    GMAIL_CLIENT_ID: str = os.getenv('GMAIL_CLIENT_ID')
    google_url_token: str = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='
    google_url_logout: str = 'https://accounts.google.com/o/oauth2/revoke?token='

    # Constants - Facebook
    FACEBOOK_APP_ID: str = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_SECRET: str = os.getenv('FACEBOOK_APP_SECRET')

    facebook_url_client_id: str = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id='
    facebook_url_client_secret: str = '&client_secret='
    facebook_url_fb_exchange_token: str = '&fb_exchange_token='

    facebook_url_token1: str = 'https://graph.facebook.com/v2.8/me?access_token='
    facebook_url_token2: str = '&fields=name,id,email'

    facebook_url_picture1: str = 'https://graph.facebook.com/v2.8/me/picture?access_token='
    facebook_url_picture2: str = '&redirect=0&height=200&width=200'

    facebook_url_userinfo: str = 'https://www.googleapis.com/oauth2/v1/userinfo'
    facebook_url_logout1: str = 'https://graph.facebook.com/'
    facebook_url_logout2: str = '/permissions?access_token='
