**Blueprint**
In Flask, a blueprint is a logical structure that represents a subset of the application. A blueprint can include elements such as routes, view functions, forms, templates and static files. If you write your blueprint in a separate Python package, then you have a component that encapsulates the elements related to specific feature of the application.

The contents of a blueprint are initially in a dormant state. To associate these elements, the blueprint needs to be registered with the application. During the registration, all the elements that were added to the blueprint are passed on to the application. So you can think of a blueprint as a temporary storage for application functionality that helps in organizing your code.

So far we have put all our code in a single file, for example routes.py file contain all the routes for different functionalities. Now, I have decided to re-organize my application in following blueprints:
1. Posts Blueprint
2. Main Blueprint
3. Error Blueprint
4. Users Blueprint

**Posts Blueprint**
```
blog/
    posts/                              <-- blueprint package
        __init__.py                     <-- define posts as package
        forms.py                        <-- posts forms
        routes.py                       <-- posts routes and blueprint creation
    templates/
        posts/                          <-- blueprint templates
            create_post.html
            post.html
            user_posts.html
    __init__.py                         <-- blueprint registration
```
Steps:
```
1. Create a directory posts in /blog/

2. Create a directory posts in /blog/template/

3. Move all posts related templates from /blog/templates to /blog/templates/posts/

4. Create a file \_\_init.\_\_.py in posts folder

5. Create a file routes.py in posts folder

6. Create blueprint by updating /blog/posts/routes.py
         from flask import Blueprint
         posts = Blueprint('posts', \_\_name\_\_)

6. Move your posts related routes(view functions) from existing /blog/routes.py into /blog/posts/routes.py and correct 
   all the imports

7. Update all the routes in /blog/posts/routes.py with blueprint name example :
         @app.route("/post/new", methods=['GET', 'POST']) >>>> @posts.route("/post/new", methods=['GET', 'POST'])

8. Update location of all rendered templates in /blog/posts/routes.py with new location of templates. Example :
         return render_template('create_post.html', .....)  >>>> return render_template('posts/create_post.html', ......)

9. Check all your files in project folder to update url_for e.g. url_form('post') --> url_for(posts.post). 

10. Blueprint Registration by updating /blog/\_\_init\_\_.py as :
         from blog.posts.routes import posts
         app.register_blueprint(posts)
```     
You need to repeat same steps for main, errors and users blueprint. Below are the few important changes that i have done for simplicity and correctness.
1. Renamed errors.py to handlers.py after moving into errors folder.

2. Replaced errorhandler with app_errorhandler, because errorhandler is a method inherited from Flask, not Blueprint. If you are using Blueprint, the equivalent is    app_errorhandler.

3. If you are importing any Class from modules of blueprint, need to update blueprint name while import. Example :
         from blog.forms import PostForm >>> from blog.posts.forms import PostForm

4. Created a file utils.py in Users blueprint to keep function like save_picture.

5. I have renamed blog.py to run.py and updated .flaskenv as FLASK_APP=run.py

6. We need to update login.login_view = 'login' >> login.login_view = 'users.login' in \_\_init\_\_.py after creating users blueprint

**Important Notes on Blueprint**
1. Flask blueprints can be configured to have a separate directory for templates or static files. I have decided to move the templates into a sub-directory of the application's template directory so that all templates are in a single hierarchy, but if you prefer to have the templates that belong to a blueprint inside the blueprint package, that is supported. For example, if you add a template_folder='templates' argument to the Blueprint() constructor, you can then store the blueprint's templates in blog/errors/templates/.

2. The Blueprint class takes the name of the blueprint, the name of the base module (typically set to \_\_name\_\_ like in the Flask application instance), and a few optional arguments e.g. posts = Blueprint('posts', \_\_name\_\_)

3. To register a blueprint, the register_blueprint() method of the Flask application instance is used. When a blueprint is registered, any view functions, templates, static files, error handlers, etc. are connected to the application. I put the import of the blueprint right above the app.register_blueprint() to avoid circular dependencies.

4. The register_blueprint() call in this case has an extra argument, url_prefix. This is entirely optional, but Flask gives you the option to attach a blueprint under a URL prefix, so any routes defined in the blueprint get this prefix in their URLs. In many cases this is useful as a sort of "namespacing" that keeps all the routes in the blueprint separated from other routes in the application or other blueprints. For authentication, I thought it was nice to have all the routes starting with /auth, so I added the prefix. So now the login URL is going to be http://localhost:5000/auth/login. Because I'm using url_for() to generate the URLs, all URLs will automatically incorporate the prefix.
    from blog.users.routes import users
    app.register_blueprint(users, url_prefix='/auth')
    
**The Application Factory Pattern**</br>
As I mentioned in the introduction to this chapter, having the application as a global variable introduces some complications, mainly in the form of limitations for some testing scenarios. Before I introduced blueprints, the application had to be a global variable, because all the view functions and error handlers needed to be decorated with decorators that come from app, such as @app.route. But now that all routes and error handlers were moved to blueprints, there are a lot less reasons to keep the application global.

So what I'm going to do, is add a function called create_app() that constructs a Flask application instance, and eliminate the global variable.

**\_\_init\_\_.py**
```python
from flask import Flask
from blog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os

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
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(file_handler)    

    app.logger.addHandler(file_handler)
    app.logger.info('Blog startup')

    return app
```
1. You have seen that most Flask extensions are initialized by creating an instance of the extension and passing the application as an argument. When the application does not exist as a global variable, there is an alternative mode in which extensions are initialized in two phases. The extension instance is first created in the global scope as before, but no arguments are passed to it. This creates an instance of the extension that is not attached to the application. At the time the application instance is created in the factory function, the init_app() method must be invoked on the extension instances to bind it to the now known application.

2. Other tasks performed during initialization remain the same, but are moved to the factory function instead of being in the global scope. This includes the registration of blueprints and logging configuration.

3. So who calls the application factory function? The obvious place to use this function is the top-level run.py script, which is the only module in which the application now exists in the global scope.
```python
# FileName: Flask-Blog > run.py
from blog import create_app

app = create_app()

if __name__ == '__main__':
    app.run() 
```   
 
4. Most references to app went away with the introduction of blueprints, but there were some still in the code that I had to address for example users/utils.py, from flask import app etc. The current_app variable that Flask provides is a special "context" variable that Flask initializes with the application before it dispatches a request. Replacing app with Flask's current_app variable eliminates the need of importing the application instance as a global variable.

**Start Aplication**</br>
```python
env\Scripts\activate
flask run
```
**Project Hierarchy**
```python
Flask-Blog
|---config.py
|---models.py
|---__init__.py
|---.env
|---.flaskenv
|---run.py
|--+logs
|   |  blog.log
|--+env
|--+blog
|   +---errors
|   |       handlers.py
|   |       __init__.py
|   |
|   +---main
|   |       routes.py
|   |       __init__.py
|   |
|   +---posts
|   |       forms.py
|   |       routes.py
|   |       __init__.py
|   +---users
|   |       forms.py
|   |        routes.py
|   |        utils.py
|   |        __init__.py
|   |
|   +---static
|   |   |   main.css
|   |   |
|   |   +---profile_pics
|   |           67fcb7f498d57cf6.JPG
|   |           b33c2f540f685ae9.JPG
|   |           default.JPG
|   |
|   +---templates
|   |   |   layout.html
|   |   |
|   |   +---errors
|   |   |       403.html
|   |   |       404.html
|   |   |       500.html
|   |   |
|   |   +---includes
|   |   |       _messages.html
|   |   |       _navbar.html
|   |   |
|   |   +---main
|   |   |       about.html
|   |   |       home.html
|   |   |
|   |   +---posts
|   |   |       create_post.html
|   |   |       post.html
|   |   |       user_posts.html
|   |   |
|   |   +---users
|   |           account.html
|   |           login.html
|   |           register.html


```
