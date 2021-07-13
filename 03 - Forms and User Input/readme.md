**Introduction to Flask-WTF**</br>
To handle the web forms in this application I'm going to use the Flask-WTF extension, which is a thin wrapper around the WTForms package that nicely integrates it with Flask.

Flask extensions are regular Python packages that are installed with pip. You can go ahead and install Flask-WTF in your virtual environment:
```
pip install flask-wtf
```
**Configuration**
There are several formats for the application to specify configuration options. The most basic solution is to define your variables as keys in app.config, which uses a dictionary style to work with variables. For example, you could do something like this:
```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
# ... add more variables here as needed
```
While the above syntax is sufficient to create configuration options for Flask, I like to enforce the principle of separation of concerns, so instead of putting my configuration in the same place where I create my application I will use a structure that allows me to keep my configuration in a separate file.

To keep things nicely organized, I'm going to create the configuration class in a separate Python module. Below you can see the new configuration class for this application, stored in a config.py module in the package (under blog folder).

```python
# FileName: Flask-Blog > blog > config.py
import os, secrets

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
    #  I prefer the "or" method, as that also works if the environment variable is set to an empty string.
```
The configuration settings are defined as class variables inside the Config class. As the application needs more configuration items, they can be added to this class
The SECRET_KEY configuration variable that I added as the only configuration item is an important part in most Flask applications. Flask and some of its extensions use the value of the secret key as a cryptographic key, useful to generate signatures or tokens. The Flask-WTF extension uses it to protect web forms against a nasty attack called Cross-Site Request Forgery or CSRF (pronounced "seasurf"). As its name implies, the secret key is supposed to be secret, as the strength of the tokens and signatures generated with it depends on no person outside of the trusted maintainers of the application knowing it.

The value of the secret key is set as an expression with two terms, joined by the or operator. The first term looks for the value of an environment variable, also called SECRET_KEY. The second term, is dynamic way to generate key. The idea is that a value sourced from an environment variable is preferred, but if the environment does not define the variable, then the dynamic string is used instead. 

Now that I have a config file, I need to tell Flask to read it and apply it. That can be done right after the Flask application instance is created using the app.config.from_object() method:

```python
# FileName: Flask-Blog > blog > __init__.py
from flask import Flask
from blog.config import Config

# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog

app = Flask(__name__)
app.config.from_object(Config)

from blog import routes
```
The way I'm importing the Config class may seem confusing at first, but if you look at how the Flask class (uppercase "F") is imported from the flask package (lowercase "f") you'll notice that I'm doing the same with the configuration. The lowercase "config" is the name of the Python module config.py, and obviously the one with the uppercase "C" is the actual class.

The configuration items can be accessed with a dictionary syntax from app.config. Here you can see a quick session with the Python interpreter where I check what is the value of the secret key:
```python
Flask-Blog$python
>>> from blog import app
>>> app.config['SECRET_KEY']
'_eo3FOdfU2m0VVFNbrHRc9mMNKSP3tI4y2BLX11o7vU'
```

**User Login Form**
The Flask-WTF extension uses Python classes to represent web forms. A form class simply defines the fields of the form as class variables.

Once again having separation of concerns in mind, I'm going to use a new blog/forms.py module to store my web form classes. To begin, let's define a user registration and login forms.
```forms.py
# FileName: Flask-Blog > blog > forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
```

In this form we have imported FlaskForm class from flask_wtf extension. The four classes that represent the field types that I'm using for this form are imported directly from the WTForms package, since the Flask-WTF extension does not provide customized versions. For each field, an object is created as a class variable in the LoginForm and RegistratioForm class. Each field is given a description or label as a first argument.

The optional validators argument that you see in some of the fields is used to attach validation behaviors to fields. The DataRequired validator simply checks that the field is not submitted empty. There are many more validators available, some of which like Length, Email, EqualTo are also used.

**Login and Registration Templates**

The next step is to add the form to an HTML template so that it can be rendered on a web page. The good news is that the fields that are defined in the RegistrationForm and LoginForm class know how to render themselves as HTML, so this task is fairly simple.</br>
**login.html**
```html
{% extends "layout.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.email.label }}<br>
            {{ form.email() }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password() }}
        </p>
        <p>{{ form.remember() }} {{ form.remember.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```
**Explanations:**</br>
1. The HTML <form> element is used as a container for the web form. The action attribute of the form is used to tell the browser the URL that should be used when submitting the information the user entered in the form. When the action is set to an empty string the form is submitted to the URL that is currently in the address bar, which is the URL that rendered the form on the page. 

2. The method attribute specifies the HTTP request method that should be used when submitting the form to the server. The default is to send it with a GET request, but in almost all cases, using a POST request makes for a better user experience because requests of this type can submit the form data in the body of the request, while GET requests add the form fields to the URL
  
3. The novalidate attribute is used to tell the web browser to not apply validation to the fields in this form, which effectively leaves this task to the Flask application running in the server. Using novalidate is entirely optional, but for this first form it is important that you set it because this will allow you to test server-side validation later.
  
4. The form.hidden_tag() template argument generates a hidden field that includes a token that is used to protect the form against CSRF attacks. All you need to do to have the form protected is include this hidden field and have the SECRET_KEY variable defined in the Flask configuration. If you take care of these two things, Flask-WTF does the rest for you.
  
5. If you've written HTML web forms in the past, you may have found it odd that there are no HTML fields in this template. This is because the fields from the form object know how to render themselves as HTML. All I needed to do was to include {{ form.<field_name>.label }} where I wanted the field label, and {{ form.<field_name>() }} where I wanted the field. For fields that require additional HTML attributes, those can be passed as arguments. </br>
  
**Form Views**</br>
The final step before you can see this form in the browser is to code a new view function in the application that renders the template from the previous section.
So let's write a new view function mapped to the /login URL that creates a form, and passes it to the template for rendering. This view function can also go in the app/routes.py module with the previous one:</br>
**routes.py**
```python
#Flask-Blog > blog > routes.py
from flask import render_template
from blog import app
from blog.forms import LoginForm

# print(f"In routes.py: {__name__}") o/p: In routes.py: blog.routes
user = {'username': 'Alok'}

..................

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
```
What I did here is import the LoginForm class from forms.py, instantiated an object from it, and sent it down to the template. The form=form syntax may look odd, but is simply passing the form object created in the line above (and shown on the right side) to the template with the name form (shown on the left). This is all that is required to get form fields rendered.

At this point you can run the application and see the form in your web browser. With the application running, type http://localhost:5000/ in the browser's address bar, and then click on the "Login" link in the top navigation bar to see the new login form.

**Receiving Form Data**</br>
If you try to press the submit button the browser is going to display a "Method Not Allowed" error. This is because the login view function from the previous section does one half of the job so far. It can display the form on a web page, but it has no logic to process data submitted by the user yet. This is another area where Flask-WTF makes the job really easy. Here is an updated version of the view function that accepts and validates the data submitted by the user:

```python
#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect
from blog import app
from blog.forms import LoginForm
..........
..........
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect('/home')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
```

**Explanation**
1. The first new thing in this version is the methods argument in the route decorator. This tells Flask that this view function accepts GET and POST requests, overriding the default, which is to accept only GET requests. The HTTP protocol states that GET requests are those that return information to the client (the web browser in this case). All the requests in the application so far are of this type. POST requests are typically used when the browser submits form data to the server (in reality GET requests can also be used for this purpose, but it is not a recommended practice). The "Method Not Allowed" error that the browser showed you before, appears because the browser tried to send a POST request and the application was not configured to accept it. By providing the methods argument, you are telling Flask which request methods should be accepted.

2. The form.validate_on_submit() method does all the form processing work. When the browser sends the GET request to receive the web page with the form, this method is going to return False, so in that case the function skips the if statement and goes directly to render the template in the last line of the function.

3. When the browser sends the POST request as a result of the user pressing the submit button, form.validate_on_submit() is going to gather all the data, run all the validators attached to fields, and if everything is all right it will return True, indicating that the data is valid and can be processed by the application. But if at least one field fails validation, then the function will return False, and that will cause the form to be rendered back to the user, like in the GET request case. Later I'm going to add an error message when validation fails.

4. When form.validate_on_submit() returns True, the login view function calls two new functions, imported from Flask. The flash() function is a useful way to show a message to the user. A lot of applications use this technique to let the user know if some action has been successful or not.

5. I don't have readl user yet so will check this form with email =admin@blog.com and password=password.

6. The second new function used in the login view function is redirect(). This function instructs the client web browser to automatically navigate to a different page, given as an argument. This view function uses it to redirect the user to the home page of the application.

7. When you call the flash() function, Flask stores the message, but flashed messages will not magically appear in web pages. The templates of the application need to render these flashed messages in a way that works for the site layout. I'm going to add these messages to the includes\/\_messages.html and refer that in layout template, so that all the templates inherit this functionality. This is the updated templats:</br>

**\templates\includes\_messages.html**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
```
An interesting property of these flashed messages is that once they are requested once through the get_flashed_messages function they are removed from the message list, so they appear only once after the flash() function is called.</br>

**\templates\layout.html**
```html
    <body>
        {% include 'includes/_navbar.html' %}
        <main role="main" class="container">
            <div class="row">
              <div class="col-md-8">
                {% include 'includes/_messages.html' %}
                {% block content %}{% endblock %}
              </div>
              <div class="col-md-4">
                <div class="content-section">
                  <h3>Our Sidebar</h3>
                  <p class='text-muted'>You can put any information here you'd like.
                    <ul class="list-group">
                      <li class="list-group-item list-group-item-light">Latest Posts</li>
                      <li class="list-group-item list-group-item-light">Announcements</li>
                      <li class="list-group-item list-group-item-light">Calendars</li>
                      <li class="list-group-item list-group-item-light">etc</li>
                    </ul>
                  </p>
                </div>
              </div>
            </div>
          </main>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </body>
```
**Improving Field Validation**</br>
The validators that are attached to form fields prevent invalid data from being accepted into the application. The way the application deals with invalid form input is by re-displaying the form, to let the user make the necessary corrections.

If you tried to submit invalid data, I'm sure you noticed that while the validation mechanisms work well, there is no indication given to the user that something is wrong with the form, the user simply gets the form back. The next task is to improve the user experience by adding a meaningful error message next to each field that failed validation.

In fact, the form validators generate these descriptive error messages already, so all that is missing is some additional logic in the template to render them.

**login.html**
```html
{% extends "layout.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.email.label }}<br>
            {{ form.email() }}
            {% for error in form.email.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password() }}
            {% for error in form.password.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>{{ form.remember() }} {{ form.remember.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```
The only change I've made is to add for loops right after the username and password fields that render the error messages added by the validators in red color. As a general rule, any fields that have validators attached will have error messages added under form.<field_name>.errors.

If you try to submit the form with an empty email or password or invalid format of email, you will now get a nice error message in red.


**Generating Links**
We have been using links directly in templates.One problem with writing links directly in templates and source files is that if one day you decide to reorganize your links, then you are going to have to search and replace these links in your entire application.

```html
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # ...
        return redirect('/index')
```

To have better control over these links, Flask provides a function called url_for(), which generates URLs using its internal mapping of URLs to view functions. For example, url_for('login') returns /login, and url_for('index') return '/index. The argument to url_for() is the endpoint name, which is the name of the view function.

So from now on, I'm going to use url_for() every time I need to generate an application URL. Let me update all URLs in \_navbar.html and login.html. I will correct this on other
templates as well if i see direct links. 

**routes.py**
```python
#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for
from blog import app
from blog.forms import LoginForm

# print(f"In routes.py: {__name__}") o/p: In routes.py: blog.routes
user = {'username': 'Alok'}

posts = [
    {
        'author': 'Alok',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Jul 11, 2021'
    },
    {
        'author': 'Chris',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Jul 12, 2021'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', user=user, posts= posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
```
**\_navbar.html**
```html
<header class="site-header">
    <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
      <div class="container">
        <a class="navbar-brand mr-4" href="/">Flask Blog</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarToggle">
          <div class="navbar-nav mr-auto">
            <a class="nav-item nav-link" href="{{ url_for('home') }}">Home</a>
            <a class="nav-item nav-link" href="{{ url_for('about') }}">About</a>
          </div>
          <!-- Navbar Right Side -->
          <div class="navbar-nav">
            <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
            <a class="nav-item nav-link" href="#">Register</a>
          </div>
        </div>
      </div>
    </nav>
  </header>
```
Now, I will implement similar concepts for register page by creating register.html and adding register function view in routes.html. I will also update ```<a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>``` in \_navbar.html

**register.html**
```html
{% extends "layout.html" %}

{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username() }}
            {% for error in form.username.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.email.label }}<br>
            {{ form.email() }}
            {% for error in form.email.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>        
        <p>
            {{ form.password.label }}<br>
            {{ form.password() }}
            {% for error in form.password.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.confirm_password.label }}<br>
            {{ form.confirm_password() }}
            {% for error in form.confirm_password.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>        
        <p>{{ form.submit() }}</p>
        <p>Already Have An Account? <a href="{{ url_for('login') }}">Sign In</a></p>
    </form>
{% endblock %}
```
**routes.py**
```python
#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for
from blog import app
from blog.forms import LoginForm, RegistrationForm
............
............
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
```
