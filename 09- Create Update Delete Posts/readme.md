**Create Update Delete Posts**</br>
Let's add some functionality to create, update and delete posts. So, far we have been using dummy post to show in application, but now we will remove that. 

Firstly, we will add a route in route.py for new post.

**routes.py**
```python
........
#
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user.username)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form=form, legend='New Post')
```

Create a post form in forms.py by importing a new validator TextAreaField

**forms.py**
```python

# FileName: Flask-Blog > blog > forms.py
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,ValidationError)
from blog.models import User

................
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
```

At this step, i relalized that i should have a column "author" in posts table instead of "userid". I have dropped posts table and recreated with following sql:
```sql
CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `date_posted` timestamp NOT NULL DEFAULT current_timestamp(),
  `content` text NOT NULL,
  `author` varchar(30) NOT NULL
  
) ;

ALTER TABLE `posts` ADD PRIMARY KEY (`id`);
ALTER TABLE `posts` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `posts` ADD CONSTRAINT FK_Authr  ADD FOREIGN KEY (`author`) REFERENCES `users`(username);
```

Updated models.py as well to reflect these changes :</br>
**models.py**
```python
...........
#
class Post(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" 
..................
```````
Now, i will create a new html create_post.html to render and will update \_navbar.html as well to provide link to create post after authentication.

**create_post.html**
```html
{% extends "layout.html" %}

{% block content %}
    <h1>Create a New Post </h1>
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.title.label }}<br>
            {{ form.title(class="form-control") }}
            {% for error in form.title.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.content.label }}<br>
            {{ form.content(class="form-control") }}
            {% for error in form.content.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```
**\_navbar.html**
```html
..........
          <div class="navbar-nav">
            <a class="nav-item nav-link" href="{{ url_for('account') }}">Account</a>
            {% if current_user.is_authenticated %}
            <a class="nav-item nav-link" href="{{ url_for('new_post') }}">Create Post</a>
            <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
            {% else %}
            <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
            <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
            {% endif %}
            </div>
```

Now, if you run you application and try to submit post, that will work fine. But,we need to update home.html and view function.
**routes.html**</br>
```python
............
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all() # this will help to query all the posts 
    return render_template('home.html', title='Home Page', posts= posts) #send posts to html template
............
```
I want to display image file as well along with posts on home page so, let me add a backref relationship in models.py because that will ease our job.

**models.py**</br>
```python
from blog import db
from datetime import datetime
from flask_login import UserMixin
from blog import login

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(100), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts_virtual = db.relationship('Post', backref='writer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" 


```
**home.html**</br>
```html
{% extends "layout.html" %}
{% block content %}
    {% for post in posts %}
        <article class="media content-section">
          <img class= "rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.writer.image_file) }}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
            </div>
            <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}
{% endblock content %}
```

We are done with submitting new posts and display them on home page with image and date-format as yyyy-mm-dd for date posted.

**Create a new route to display a single post**</br>

**routes.py**</br>
```python
...............
@app.route("/post/<int:post_id>") #if user enter post/1 then post_id will be 1
def post(post_id): # pass post_id to post function
    post = Post.query.get_or_404(post_id) #get_or_404 method return post with mentioned post_id else return error 404
    return render_template('post.html', title=post.title, post=post) 
```
    
**create new template post.html**</br>
**post.html**</br>
```html
{% extends "layout.html" %}
{% block content %}
        <article class="media content-section">
          <img class= "rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.writer.image_file) }}"> 
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
            </div>
            <h2><class="article-title">{{ post.title }}</h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
{% endblock content %}
```
This is similar to home.html except for loop and removal of href from post.title.

We need to update home.html and mention href for posts which is # as of now.

**home.html**</br>
```html
{% extends "layout.html" %}
{% block content %}
    {% for post in posts %}
        <article class="media content-section">
          <img class= "rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.writer.image_file) }}"> 
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
            </div>
            <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}
{% endblock content %}
```



