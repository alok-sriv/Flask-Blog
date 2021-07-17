**What Are Templates?**
```python
from blog import app

# print(f"In routes.py: {__name__}") o/p: In routes.py: blog.routes

@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Alok'}
    return ''' <h1>Home Page,Hi '''+ user['username'] +''' !</h1>'''

@app.route("/about")
def about():
    return '''<h1>About Page</h1>'''
```
```
So far we have implemented HTML logic for different routes in routes.py file, but I hope you agree with me that the 
solution used to deliver HTML to the browser is not good. Consider how complex the code in this view function will 
become when I have the blog posts from users, which are going to constantly change.

If you could keep the logic of your application separate from the layout or presentation of your web pages, then things 
would be much better organized. Templates help achieve this separation between presentation and business logic. 

In Flask, templates are written as separate files, stored in a templates folder that is inside the application package, 
that is "blog" in my case.

Steps:
1. cd blog
2. mkdir templates
3. Create some html templates
```
**home.html**
```html
<html>
    <head>
        <title>{{ title }} - FlaskBlog</title>
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```
```
Note:
The only interesting thing in this page is that there are a couple of placeholders for the dynamic content, 
enclosed in {{ ... }} sections. These placeholders represent the parts of the page that are variable and 
will only be known at runtime.

Now that the presentation of the page was offloaded to the HTML template, the view function can be simplified:
```
**routes.py**
```python
#Flask-Blog > blog > routes.py
from flask import render_template
from blog import app

# print(f"In routes.py: {__name__}") o/p: In routes.py: blog.routes

@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Alok'}
    return render_template('home.html', title='Home', user=user)

@app.route("/about")
def about():
    return '''<h1>About Page</h1>'''
```
```
Notes:
The operation that converts a template into a complete HTML page is called rendering. To render the template I had to 
import a function that comes with the Flask framework called render_template(). This function takes a template filename
and a variable list of template arguments and returns the same template, but with all the placeholders in it replaced 
with actual values.

The render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework. 
Jinja2 substitutes {{ ... }} blocks with the corresponding values, given by the arguments provided in the 
render_template() call.
```

**Conditional Statements**</br >
The next version of the home.html template adds a conditional statement:
```html
<html lang="en">
    <head>
        {% if title %}
        <title>{{ title }} - FlaskBlog</title>
        {% else %}
        <title>Welcome to FlaskBlog!</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```
```
Now the template is a bit smarter. If the view function forgets to pass a value for the title placeholder variable, 
then instead of showing an empty title the template will provide a default one. You can try how this conditional works
by removing the title argument in the render_template() call of the view function.
```

**Loops**</br>
The logged in user will probably want to see recent posts from connected users in the home page, so what I'm going to </br>
do now is extend the application to support that. Once again, I'm going to hardcode some posts to show in routes.py </br>
Moreover, I will create about.html and render that for "/about".

```python
#Flask-Blog > blog > routes.py
from flask import render_template
from blog import app

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
```
**home.html**
```html
<html lang="en">
    <head>
        {% if title %}
        <title>{{ title }} - FlaskBlog</title>
        {% else %}
        <title>Welcome to FlaskBlog!</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
        {% for post in posts %}
        <div><p>{{ post.title }} by {{ post.author }}</p></div>
        <div><p>{{ post.content }} on date {{ post.date_posted }}</p></div>
        {% endfor %}        
    </body>
</html>
```
**about.html**
```html
<html lang="en">
    <head>
        {% if title %}
        <title>{{ title }} - FlaskBlog</title>
        {% else %}
        <title>Welcome to FlaskBlog!</title>
        {% endif %}
    </head>
    <body>
        <h1>About Page</h1>
      
    </body>
</html>
```

**Template Inheritance**</br>
You can see some of similar code in about.html and home.html as:</br>
```html
    <head>
        {% if title %}
        <title>{{ title }} - FlaskBlog</title>
        {% else %}
        <title>Welcome to FlaskBlog!</title>
        {% endif %}
    </head>
```
We will need similar code in all of our html files. I don't really want to have to maintain several copies of the this </br>
in many HTML templates, it is a good practice to not repeat yourself if that is possible.</br>

Jinja2 has a template inheritance feature that specifically addresses this problem. In essence, what you can do is move the</br>
parts of the page layout that are common to all templates to a base template, from which all other templates are derived.</br>

So what I'm going to do now is define a base template called layout.html that includes the title logic. You need to write the</br>
following template in file blog/templates/layout.html:</br>

**layout.html**</br>
```html
<html lang="en">
    <head>
        {% if title %}
            <title>{{ title }} - FlaskBlog</title>
        {% else %}
            <title>Welcome to FlaskBlog!</title>
        {% endif %}
    </head>
    <body>
        {% block content %} {% endblock content %}
    </body>
</html>
```
In this template I used the block control statement to define the place where the derived templates can insert themselves.</br>
Blocks are given a unique name, which derived templates can reference when they provide their content.Now, we will inherit</br>
this template in about.html and home.html</br>

**about.html**</br>
```html
{% extends "layout.html" %}
{% block content %}
<h1>About Page</h1>
{% endblock content %}
```
**home.html**</br>
```html
{% extends "layout.html" %}
{% block content %}
        <h1>Hello, {{ user.username }}!</h1>
        {% for post in posts %}
        <div><p>{{ post.title }} by {{ post.author }}</p></div>
        <div><p>{{ post.content }} on date {{ post.date_posted }}</p></div>
        {% endfor %}        
{% endblock content %}
```
Since the __layout.html__ template will now take care of title logic, I have removed all those elements from home.html and about.html</br>
and left only the content part. The extends statement establishes the inheritance link between the two templates, so that Jinja2 knows</br>
that when it is asked to render home.html it needs to embed it inside layout.html. The two templates have matching block statements</br>
with name content, and this is how Jinja2 knows how to combine the two templates into one.</br>
Now if I need to create additional pages for application, I can create them as derived templates from the same layout.html template </br>
and that is how I can have all the pages of the application sharing the same look and feel without duplication.</br>

**Add Bootstrap**</br>
Let's add bootstrap to your application for better look. I will add required code in "layout.html" as that is being extended by all of </br>
my html files. I will use following link: https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template </br>
Moreover, I will move my {% block content %} in bootstrap container class for better padding, and then hard referesh browser with </br>
__Ctrl+Shift+R__ </br>

**layout.html**
```html
<html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        {% if title %}
            <title>{{ title }} - FlaskBlog</title>
        {% else %}
            <title>Welcome to FlaskBlog!</title>
        {% endif %}
    </head>
    <body>
        <div class="container">
        {% block content %} {% endblock content %}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </body>
</html>
```

Let's Add Navbar in your blog, I used https://getbootstrap.com/docs/4.0/components/navbar/ for code, but i modified based</br>
on my requirement. I will use sub-templating method for cleaner code. 
> mkdir -p blog/templates/includes</br>
***\_navbar.html***
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
            <a class="nav-item nav-link" href="/">Home</a>
            <a class="nav-item nav-link" href="/about">About</a>
          </div>
          <!-- Navbar Right Side -->
          <div class="navbar-nav">
            <a class="nav-item nav-link" href="/login">Login</a>
            <a class="nav-item nav-link" href="/register">Register</a>
          </div>
        </div>
      </div>
    </nav>
  </header>
```

I used main.css for better colors, and place that file in static. In flask we put files such as css, images in static folder.</br>
> mkdir -p blog/static </br>

I have updated layout.html to add sidebar and include main.css.</br>

I have updated home.html as well with some better html code for posts </br>

I have not explained all these html and css code as we will focus on Flask. Refer code in GitHub repo for more details.</br>

Now, you will see better site for our blog.



