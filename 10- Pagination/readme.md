**Pagination**</br>
Now, our task is to display certain numbers of posts on Home page instead of loading all of them, because loading all posts with images will eventually slowe down performance.

We wil update routes.py for this. But, firsst understand this from pytho interpreter with following commands:

```python
(env) Flask-Blog>python
>>> from blog.models import Post
>>> posts = Post.query.all()
>>> for post in posts:
...     post
...
Post('New Post', '2021-07-16 18:11:42')
Post('My Post2', '2021-07-17 12:01:45')
Post('My Post3', '2021-07-17 12:02:00')
Post('My Post 4', '2021-07-17 12:02:20')
Post('Title5', '2021-07-17 12:02:38')
Post('Post1', '2021-07-17 12:03:17')
Post('Post2', '2021-07-17 12:03:27')
Post('Post3', '2021-07-17 12:03:37')
Post('Post4', '2021-07-17 12:03:46')
Post('Post5', '2021-07-17 12:03:57')
>>>
>>>
>>> posts = Post.query.paginate()
>>> posts
<flask_sqlalchemy.Pagination object at 0x000001A04724CF28>
>>> dir(posts) #it will display all the attributes
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', 
'__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
'__str__', '__subclasshook__', '__weakref__', 'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages', 'per_page', 'prev', 
'prev_num', 'query', 'total']
>>>
>>> posts.per_page #default per page items
20
>>>
>>> posts.page
1

>>> for post in posts.items:
...     print(post)
...
Post('New Post', '2021-07-16 18:11:42')
Post('My Post2', '2021-07-17 12:01:45')
Post('My Post3', '2021-07-17 12:02:00')
Post('My Post 4', '2021-07-17 12:02:20')
Post('Title5', '2021-07-17 12:02:38')
Post('Post1', '2021-07-17 12:03:17')
Post('Post2', '2021-07-17 12:03:27')
Post('Post3', '2021-07-17 12:03:37')
Post('Post4', '2021-07-17 12:03:46')
Post('Post5', '2021-07-17 12:03:57')


>>> posts = Post.query.paginate(per_page=5) #modify default value to show only 5 items per page
>>> for post in posts.items:
...     print(post)
...
Post('New Post', '2021-07-16 18:11:42')
Post('My Post2', '2021-07-17 12:01:45')
Post('My Post3', '2021-07-17 12:02:00')
Post('My Post 4', '2021-07-17 12:02:20')
Post('Title5', '2021-07-17 12:02:38')
>>>
>>> #access 2nd page now
...
>>> posts = Post.query.paginate(per_page=5, page=2)
>>> for post in posts.items:
...     print(post)
...
Post('Post1', '2021-07-17 12:03:17')
Post('Post2', '2021-07-17 12:03:27')
Post('Post3', '2021-07-17 12:03:37')
Post('Post4', '2021-07-17 12:03:46')
Post('Post5', '2021-07-17 12:03:57')
>>>

>>> posts.total
10
>>>

```
Let's implement this in our flask app.
**routes.py**</br>
```python
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int) # get page number from URL, this is optional so will use page num 1 as default and type should be integer
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #order by based on date_posted along with pagination attributes
    return render_template('home.html', title='Home Page', posts= posts)
 ```
 
 Update home.html template
 **home.html**
 ```html
{% extends "layout.html" %}
{% block content %}
    {% for post in posts.items %}
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
    {% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}# to limit number of page buttons on screen
      {% if page_num %}
        {% if posts.page == page_num %}
          <a class="btn btn-info mb-4" href="{{ url_for('home', page=page_num) }}">{{ page_num }}</a>
        {% else %}
          <a class="btn btn-outline-info mb-4" href="{{ url_for('home', page=page_num) }}">{{ page_num }}</a>
        {% endif %}
      {% else %}
        ...
      {% endif %}
    {% endfor %}
{% endblock content %}
```

So far we are done with pagination. Now we will add new functionality to view posts only by a specific person, if we click on his name on home page.

Let's add another route for this in routes.py:
```python
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user.username).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)
```
    
Let's create a new template user_posts.html, it woul be simiar to home.html except few urls.

```html
{% extends "layout.html" %}
{% block content %}
    <h1 class="mb-3">Posts by {{ user.username }} ({{ posts.total }})</h1>
    {% for post in posts.items %}
        <article class="media content-section">
          <img class= "rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.writer.image_file) }}"> 
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="{{ url_for('user_posts', username=post.author) }}">{{ post.author}}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
            </div>
            <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}
    {% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
      {% if page_num %}
        {% if posts.page == page_num %}
          <a class="btn btn-info mb-4" href="{{ url_for('user_posts', username=user.username, page=page_num) }}">{{ page_num }}</a>
        {% else %}
          <a class="btn btn-outline-info mb-4" href="{{ url_for('user_posts', username=user.username, page=page_num) }}">{{ page_num }}</a>
        {% endif %}
      {% else %}
        ...
      {% endif %}
    {% endfor %}
{% endblock content %}
```

Now, I will update Home.html and post.html for following href:
```html
<a class="mr-2" href="{{ url_for('user_posts', username=post.author) }}">{{ post.author}}</a>
```

Refer GitHub for updated code.
