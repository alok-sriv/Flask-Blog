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
**Preparing The User Model for Flask-Login**  </br>
The Flask-Login extension works with the application's user model, and require certain properties and methods to be implemented in it
The four required items are listed below:
1. is_authenticated: a property that is True if the user has valid credentials or False otherwise.
2. is_active: a property that is True if the user's account is active or False otherwise.
3. is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
4. get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python 2).

Flask-Login provides a mixin class called UserMixin that includes generic implementations that are appropriate for most user model classes. Here is how the mixin class is added to the model:
```python
..........
from flask_login import UserMixin

class User(UserMixin, db.Model):
...........
```
**User Loader Function**</br>
Flask-Login keeps track of the logged-in user by storing its unique identifier in Flask's user session, a storage space assigned to each user who connects to the application. Each time the logged-in user navigates to a new page, Flask-Login retrieves the ID of the user from the session, and then loads that user into memory.

Because Flask-Login knows nothing about databases, it needs the application's help in loading a user. For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID. This function can be added in the blog/models.py module:
```python
.........
from blog import login
# ...

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
..........
```
The user loader is registered with Flask-Login with the @login.user_loader decorator. The id that Flask-Login passes to the function as an argument is going to be a string, so databases that use numeric IDs need to convert the string to integer as you see above.


**Logging Users In**</br>
Let's revisit the login view function, which as you recall, implemented a fake login that just issued a flash() message. Now that the application has access to a user database and knows how to generate and verify password hashes, this view function can be completed.

```python
#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for, request
from blog import app, db, bcrypt
from blog.forms import LoginForm, RegistrationForm
from blog.models import User, Post
from flask_login import current_user, login_user

........
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home')) 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

```
**Explanations**</br>

1. The top two lines in the login() function deal with a weird situation. Imagine you have a user that is logged in, and the user navigates to the /login URL of your application. Clearly that is a mistake, so I want to not allow that. The current_user variable comes from Flask-Login and can be used at any time during the handling to obtain the user object that represents the client of the request. 

2. The value of this variable can be a user object from the database (which Flask-Login reads through the user loader callback I provided above), or a special anonymous user object if the user did not log in yet. Remember those properties that Flask-Login required in the user object? One of those was is_authenticated, which comes in handy to check if the user is logged in or not. When the user is already logged in, I just redirect to the home page.

3. In place of the flash() call that I used earlier, now I can log the user in for real. The first step is to load the user from the database. The username came with the form submission, so I can query the database with that to find the user. For this purpose I'm using the filter_by() method of the SQLAlchemy query object. The result of filter_by() is a query that only includes the objects that have a matching username. Since I know there is only going to be one or zero results, I complete the query by calling first(), which will return the user object if it exists, or None if it does not.

4. The first() method is another commonly used way to execute a query, when you only need to have one result.

5. If I got a match for the username that was provided, I can next check if the password that also came with the form is valid. This is done by invoking the check_password_hash() method I defined above. This will take the password hash stored with the user and determine if the password entered in the form matches the hash or not.

6. Now I have two possible error conditions: the username can be invalid, or the password can be incorrect for the user. In either of those cases, I flash an message, and keep user on login page.

7. If the username and password are both correct, then I call the login_user() function, which comes from Flask-Login. This function will register the user as logged-in, that means for any future pages that user navigates, will have the current_user variable set to that user.

8. After To complete the login process, I just redirect the newly logged-in user to the home page.

**Logging Users Out**</br>
I know I will also need to offer users the option to log out of the application. This can be done with Flask-Login's logout_user() function. Here is the logout view function:

```python
#Flask-Blog > blog > routes.py
........
from flask_login import logout_user
........
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
 ```
 To expose this link to users, I can make the Login link in the navigation bar automatically switch to a Logout link after the user logs in. This can be done with a conditional in the \_navbar.html template:
 **\_navbar.html**</br>
 ```html
          <div class="navbar-nav">
            {% if current_user.is_authenticated %}
            <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
            {% else %}
            <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
            <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
            {% endif %}
          </div>
```
The is_anonymous property is one of the attributes that Flask-Login adds to user objects through the UserMixin class. The current_user.is_authenticated expression is going to be True only when the user is logged in.


**Requiring Users To Login**</br>
Flask-Login provides a very useful feature that forces users to log in before they can view certain pages of the application. If a user who is not logged in tries to view a protected page, Flask-Login will automatically redirect the user to the login form, and only redirect back to the page the user wanted to view after the login process is complete.

For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins. This can be added in blog/__init__.py:
```python
# FileName: Flask-Blog > blog > __init__.py
.........
login.login_view = 'login'
.........
```
The way Flask-Login protects a view function against anonymous users is with a decorator called @login_required. When you add this decorator to a view function below the @app.route decorators from Flask, the function becomes protected and will not allow access to users that are not authenticated. Here is how the decorator can be applied to the account view function of the application, that i am going to create now:
**account.html**</br>
```html
{% extends "layout.html" %}
{% block content %}
    <h1>{{ current_user.username }}</h1>
{% endblock content %}
```
```python
from flask_login import login_required
...........
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
```
**\_navbar.html**
```html
........
          <div class="navbar-nav">
            <a class="nav-item nav-link" href="{{ url_for('account') }}">Account</a>
            {% if current_user.is_authenticated %}
            <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
            {% else %}
            <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
            <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
            {% endif %}
          </div>
........
```

What remains is to implement the redirect back from the successful login to the page the user wanted to access. When a user that is not logged in accesses a view function protected with the @login_required decorator, the decorator is going to redirect to the login page, but it is going to include some extra information in this redirect so that the application can then return to the first page. If the user navigates to /index, for example, the @login_required decorator will intercept the request and respond with a redirect to /login, but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index. The next query string argument is set to the original URL, so the application can use that to redirect back after login.

Here is a snippet of code that shows how to read and process the next query string argument:
```python
....
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))     
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
 .......
```
Right after the user is logged in by calling Flask-Login's login_user() function, the value of the next query string argument is obtained. Flask provides a request variable that contains all the information that the client sent with the request. In particular, the request.args attribute exposes the contents of the query string in a friendly dictionary format. If the login URL includes a next argument , then the user is redirected to that URL, else to home page.

**Showing The Logged In User in Templates**

So far we have been using fake user to display on home page. Well, the application has real users now, so I can now remove the fake user and start working with real users. Instead of the fake user I can use Flask-Login's current_user in the template:

**home.html**
```html
{% extends "layout.html" %}
{% block content %}
    <h1>Hello, {{ current_user.username }}!</h1>
.........
```

And I can remove the user template argument in the view function:
**routes.py**
```python
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home Page', posts= posts)

```

**Validation in Registration Form**
As of now , we don't have any validation on duplicate user registration. So, if you try to use duplicate user or email, Flask will through weired error as sqlalchemy.exc.IntegrityError. Let's update forms.py

**forms.py**
```python
# FileName: Flask-Blog > blog > forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.') 
 ............
 ...........
 ```

