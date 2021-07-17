**Blueprint**
So far we have put all our code in a single file, for example routes.py file contain all the routes for different functionalities. 

Folders : posts - users - main
Files : \_\_init\_\_.py : all
         routes.py : all
         forms.py : posts/users
         utils.py : users : this is for methods like def save_picture
         
Create a blueprint
 1. routes.py 
    from flask import Blueprint
    main = Blueprint('main', __name__)

 2. Move different routes from main routes.py to routes.py under different folders
 3. replace @app with @name of blueprint e.g. main
 4. move your forms into forms.py
 5. corect your imports
 6. Add following lines in maine init.py
from blog.users.routes import users
from blog.posts.routes import posts
from blog.main.routes import main
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

7. update url_for e.g. url_form('post') --> url_for(posts.post)

8. in main init.py : update login.login_view = 'login' to login.login_view = 'user.login'
9. define create_app
10. replace app import with >> from flask import current_app

need to update errorhandler is a method inherited from Flask, not Blueprint. If you are using Blueprint, the equivalent is app_errorhandler 
