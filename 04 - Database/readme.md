I am going to use MySQL database, for that I have installed XAMPP (https://www.apachefriends.org/download.html). After installation, you need to type "XAMPP Control Panel" in run of your system to open this. Follow mentioned steps :
1. Start Apache Module from XAMPP
2. Start MySQL Module from XAMPP
3. Click on "Admin" of MySQL module, that will open a browser on your local machine.
4. Click on "Databases" tab and create a new database "flask_blog" for your application.
5. By default root user does not require password, that I am going to use. So, let's update and configuration to allow it to accept password.
```
    1. grant all privileges on *.* to root@localhost identified by 'enter-your-password' with grant option;
    
    2. update following settings in C:\xampp\phpMyAdmin\config.inc.php
            $cfg['Servers'][$i]['password'] = 'enter-your-password';
            
            $cfg['Servers'][$i]['AllowNoPassword'] = False;
    
    3. Open Xampp Control Panel > click on Config of MSQL Module > my.ini, update password in following section
            # The following options will be passed to all MySQL clients
              [client]
              password       = enter-your-password
              port=3306
```
6. Stop/Start MySQL module to make connection.
7. I have configured environment variable (env) Flask-Blog>set MYSQL_PASSWORD=enter-your-password. We will use this soon.
8. Create required tables using follwing scripts:

```sql
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL UNIQUE,
  `email` varchar(100) NOT NULL UNIQUE,
  `image_file` varchar(100) NOT NULL DEFAULT 'default.jpg',
  `password` varchar(100) NOT NULL,
  `register_date` timestamp NOT NULL DEFAULT current_timestamp()
) ;

ALTER TABLE `users` ADD PRIMARY KEY (`id`);
ALTER TABLE `users` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `date_posted` timestamp NOT NULL DEFAULT current_timestamp(),
  `author` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL 
  
) ;

ALTER TABLE `posts` ADD PRIMARY KEY (`id`);
ALTER TABLE `posts` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `posts` ADD FOREIGN KEY (`user_id`) REFERENCES `users`(id);
```
**Databases in Flask**</br>
As I'm sure you have heard already, Flask does not support databases natively. This is one of the many areas in which Flask is intentionally not opinionated, which is great, because you have the freedom to choose the database that best fits your application instead of being forced to adapt to one.

There are great choices for databases in Python, many of them with Flask extensions that make a better integration with the application. 

The first required extension is  Flask-SQLAlchemy, an extension that provides a Flask-friendly wrapper to the popular SQLAlchemy package, which is an Object Relational Mapper or ORM. ORMs allow applications to manage a database using high-level entities such as classes, objects and methods instead of tables and SQL. The job of the ORM is to translate the high-level operations into database commands.

The nice thing about SQLAlchemy is that it is an ORM not for one, but for many relational databases. SQLAlchemy supports a long list of database engines, including the popular MySQL, PostgreSQL and SQLite. 

To install Flask-SQLAlchemy in your virtual environment, make sure you have activated it first, and then run:
```
pip instal flask-sqlalchemy
pip install pymysql # we will need this for MYSQL DB
```
**Flask-SQLAlchemy Configuration**</br>

Update config.py for MYSQL parameters.Refer https://flask-mysqldb.readthedocs.io/en/latest/ for more details.
```python
# FileName: Flask-Blog > blog > config.py
import os, secrets

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
```
The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature of Flask-SQLAlchemy that I do not need, which is to signal the application every time a change is about to be made in the database.

The database is going to be represented in the application by the database instance. These are objects that need to be created after the application, in the blog/\_\_init\_\_.py file:
```python
# FileName: Flask-Blog > blog > __init__.py
from flask import Flask
from blog.config import Config
from flask_sqlalchemy import SQLAlchemy


# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from blog import routes, models
```
I have made two changes to the init script. First, I have added a db object that represents the database. Finally, I'm importing a new module called models at the bottom. This module will define the structure of the database.

**Database Models**</br>
The data that will be stored in the database will be represented by a collection of classes, usually called database models. The ORM layer within SQLAlchemy will do the translations required to map objects created from these classes into rows in the proper database tables.So now that I know what I want for my users table, I can translate that into code in the new blog/models.py module:

```python
from blog import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(100), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" 
```
The User class created above inherits from db.Model, a base class for all models from Flask-SQLAlchemy. This class defines several fields as class variables. Fields are created as instances of the db.Column class, which takes the field type as an argument, plus other optional arguments that, for example, allow me to indicate which fields are unique and nullable, which is important so that database searches are efficient.

The \_\_repr\_\_ method tells Python how to print objects of this class, which is going to be useful for debugging. 


**Update Register function View**</br>
We will use sha256_crypt to encrypt password before storing them in dataase, and for this we have already install extension "passlib". 
```python
#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for
from blog import app, db
from blog.forms import LoginForm, RegistrationForm
from passlib.hash import sha256_crypt
from blog.models import User, Post

.........
.........
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data,email=form.email.data,password=sha256_crypt.encrypt(str(form.password.data)))
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
```
Now, you should run application and try to resgiter few users from GUI and check in database for vefification. Later, we will implement authentication logic.
