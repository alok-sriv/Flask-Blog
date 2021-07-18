from flask import Flask
from blog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os


# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'users.login'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)

    from blog.users.routes import users
    app.register_blueprint(users, url_prefix='/auth')

    from blog.posts.routes import posts
    app.register_blueprint(posts)

    from blog.main.routes import main
    app.register_blueprint(main)

    from blog.errors.handlers import errors
    app.register_blueprint(errors)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = ConcurrentRotatingFileHandler('logs/blog.log', maxBytes=10240,backupCount=10)
    # file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,backupCount=10)
    # file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(file_handler)    

    app.logger.addHandler(file_handler)
    app.logger.info('Blog startup')

    return app



 
