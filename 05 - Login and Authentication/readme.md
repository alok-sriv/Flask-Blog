Introduction to Flask-Login
In this chapter I'm going to introduce you to a very popular Flask extension called Flask-Login. This extension manages the user logged-in state, so that for example users can log in to the application and then navigate to different pages while the application "remembers" that the user is logged in. It also provides the "remember me" functionality that allows users to remain logged in even after closing the browser window. To be ready for this chapter, you can start by installing Flask-Login in your virtual environment:

```
pip install flask-login
```
As with other extensions, Flask-Login needs to be created and initialized right after the application instance in app/__init__.py. This is how this extension is initialized:
```python
# FileName: Flask-Blog > blog > __init__.py
# ...
from flask_login import LoginManager

app = Flask(__name__)
# ...
login = LoginManager(app)

# ...
```
Preparing The User Model for Flask-Login**  
The Flask-Login extension works with the application's user model, and expects certain properties and methods to be implemented in it
