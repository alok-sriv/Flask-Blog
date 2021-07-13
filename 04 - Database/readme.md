I am going to use MySQL database, for that I have installed XAMPP (https://www.apachefriends.org/download.html). After installation, you need to type "XAMPP Control Panel" in run of your system to open this. Follow mentioned steps :
1. Start Apache Module from XAMPP
2. Start MySQL Module from XAMPP
3. Click on "Admin" of MySQL module, that will open a browser on your local machine.
4. Click on "Databases" tab and create a new database "flask_blog" for your application.
5. By default root user does not require password, that I am going to use. So, let's update and configuration to allow it to accept password.
```
    grant all privileges on *.* to root@localhost identified by 'enter-your-password' with grant option;
    update following settings in C:\xampp\phpMyAdmin\config.inc.php
      $cfg['Servers'][$i]['password'] = 'enter-your-password';
      $cfg['Servers'][$i]['AllowNoPassword'] = False;
    Opne Xampp Control Panel > click on Config of MSQL Module > my.ini, update password in following section
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
**Update config.py for MYSQL parameters**
Refer https://flask-mysqldb.readthedocs.io/en/latest/ for more details.
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
    MYSQL_CURSORCLASS = 'DictCursor'
```
MYSQL_CURSORCLASS : The default fetchall() method of the cursor class returns a tuple, but we want to return as Dictionary, so we have used DictCursor to get output in dictionary format.
Now, you need to install few extension which we will use soon.
```
pip install flask_mysqldb
pip install passlib
```

**Update \_\_init\_\_.py to import MySQL class and initialize it**
```python
# FileName: Flask-Blog > blog > __init__.py
from flask import Flask
from blog.config import Config
from flask_mysqldb import MySQL


# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog

app = Flask(__name__)
app.config.from_object(Config)

# initialize MYSQL
mysql = MySQL(app)

from blog import routes
```

**Update Register function View**
We will use sha256_crypt to encrypt password before storing them in dataase, and for this we have already install extension "passlib". 
```python
#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for, request
from blog import app, mysql
from blog.forms import LoginForm, RegistrationForm
from passlib.hash import sha256_crypt

.........
.........
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email,password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()    
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
```
Now, you should run application and try to resgiter few users from GUI and check in database for vefification. Later, we will implement authentication logic.





