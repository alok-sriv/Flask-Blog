# FileName: Flask-Blog > blog > __init__.py
from flask import Flask, request
from blog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
bcrypt = Bcrypt(app)

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,backupCount=10)
# file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(file_handler)

app.logger.addHandler(file_handler)
app.logger.info('Blog startup')

from blog import routes, models, errors