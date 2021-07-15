We have already created registration and login pages. Now, we will update our code to provide options to update details of regsitered users and also to update profile photo.

First we need to create a class in forms.py.

**forms.py**

```python
# FileName: Flask-Blog > blog > forms.py
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,ValidationError)
from blog.models import User

..................

.................
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

```

In Flask we keep image files in static folder, so first create a \_profile\_pics folder under /templates/static folder. I'll keep default.jpg in this folder, this image will be used as default image while any user registration.

Let's update account.html to render all required details.

**account.html**
```html
{% extends "layout.html" %}

{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ image_file }}"></td>
            <td>
                <h3>User: {{ current_user.username }}</h3>
                
            </td>
        </tr>
    </table>    
    <p><h2>Account Info</h2></p>
    <form action="" method="post" enctype="multipart/form-data">
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
            {{ form.picture.label }}<br>
            {{ form.picture() }}
            {% for error in form.picture.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```
Key thing to notice here is use of enctype="multipart/form-data", without this image update will not work.

We need to install Pillow extension that will help us in deal with image resizing, that will come soon.

```python
pip install pillow
```
And finally, here is the view function that ties everything together:
**routes.py**
```python
#Flask-Blog > blog > routes.py
import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from blog import app, db, bcrypt
from blog.forms import LoginForm, RegistrationForm, UpdateAccountForm
from blog.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

..................
..................
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file, form=form)
   
```
**Explanation**
This view function processes the form in a slightly different way. 
1. If validate_on_submit() returns True I copy the data from the form into the user object and then write the object to the database. 

2. But when validate_on_submit() returns False it can be due to two different reasons. First, it can be because the browser just sent a GET request, which I need to respond by providing an initial version of the form template. It can also be when the browser sends a POST request with form data, but something in that data is invalid. 

3. For this form, I need to treat these two cases separately. When the form is being requested for the first time with a GET request, I want to pre-populate the fields with the data that is stored in the database, so I need to do the reverse of what I did on the submission case and move the data stored in the user fields to the form, as this will ensure that those form fields have the current data stored for the user. 

4. But in the case of a validation error I do not want to write anything to the form fields, because those were already populated by WTForms. To distinguish between these two cases, I check request.method, which will be GET for the initial request, and POST for a submission that failed validation.

5. We have created and called save_picture method to save picure. Let's understand that function line-by-line

```python
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) 
    #it will randamize name of uploaded image with 8 bytes, else we will have conflict if 2 users upload image with 
    #same name
    f_name, f_ext = os.path.splitext(form_picture.filename) 
    # it will help to get the image extension in f_ext e.g. png or jpg
    picture_fn = random_hex + f_ext 
    # cncatenate randamize name with extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) 
    #concatenate filename with path
    #form_picture.save(picture_path) 
    #save image at picture_path at OS Level
    #return picture_fn 
    #return picture_path to another function that can save in database but we should resize the image before saving 
    #on OS because large images can slow your website
    #Pillow extension will help us in resizing, We have already instaled Pillow using pip so, let's import
    #from PIL import Image
    #let's comment form_picture.save(picture_path) and return picture_fn now
    output_size = (125, 125)  
    #125 pixcel
    i = Image.open(form_picture)
    i.thumbnail(output_size) 
    # resizing
    i.save(picture_path) 
    # save resized image at OS level

    return picture_fn
```
