# FileName: Flask-Blog > blog > __init__.py
from flask import Flask
from blog.config import Config
from flask_mysqldb import MySQL


# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog

app = Flask(__name__)
app.config.from_object(Config)
# init MYSQL
mysql = MySQL(app)

from blog import routes