# FileName: Flask-Blog > blog > config.py
import os, secrets

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
    #  I prefer the "or" method, as that also works if the environment variable is set to an empty string.

