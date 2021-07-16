# FileName: Flask-Blog > blog > config.py
import os, secrets
from dotenv import load_dotenv

basedir = os.path.dirname(__file__)
rootdir = os.path.dirname(basedir)
load_dotenv(os.path.join(rootdir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
    #  I prefer the "or" method, as that also works if the environment variable is set to an empty string.

   # Config MySQL
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = 'flask_blog'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+MYSQL_USER+':'+MYSQL_PASSWORD+'@'+MYSQL_HOST+'/'+MYSQL_DB

    SQLALCHEMY_TRACK_MODIFICATIONS = False   