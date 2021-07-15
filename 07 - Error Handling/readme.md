**Custom Error Pages**</br>
Flask provides a mechanism for an application to install its own error pages, so that your users don't have to see the plain and boring default ones. 
As an example, let's define custom error pages for the HTTP errors 404, 403 and 500, the two most common ones. Defining pages for other errors works in the same way.
To declare a custom error handler, the @errorhandler decorator is used. I'm going to put my error handlers in a new blog/errors.py module.

```python
# FileName: Flask-Blog > blog > errors.py
from flask import render_template
from blog import app, db

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
```

The error functions work very similarly to view functions. For these two errors, I'm returning the contents of their respective templates. Note that both functions return a second value after the template, which is the error code number. For all the view functions that I created so far, I did not need to add a second return value because the default of 200 (the status code for a successful response) is what I wanted. In this case these are error pages, so I want the status code of the response to reflect that.

The error handler for the 500 errors could be invoked after a database error. To make sure any failed database sessions do not interfere with any database accesses triggered by the template, I issue a session rollback. This resets the session to a clean state.

Now, we need to create templates for there errors. For that I will create a directory named "errors" in "templates" folder.

**404.html**
```html
{% extends "layout.html" %}

{% block content %}
    <h1>Oops. Page Not Found (404)</h1>
    <p>That page does not exist. Please try a different location</p>
    <p><a href="{{ url_for('home') }}">Back</a></p>
{% endblock %}
```
**403.html**
```html
{% extends "layout.html" %}

{% block content %}
    <h1>You don't have permission to do that (403)</h1>
    <p>Please check your account and try again</p>
    <p><a href="{{ url_for('home') }}">Back</a></p>
{% endblock %}
```
**500.html**
```html
{% extends "base.html" %}

{% block content %}
    <h1>Something went wrong (500)</h1>
    <p>We're experiencing some trouble on our end. Please try again in the near future</p>
    <p><a href="{{ url_for('home') }}">Back</a></p>
{% endblock %}
```



To get these error handlers registered with Flask, I need to import the new blog/errors.py module after the application instance is created:

**\_\_init\_\_.py**
```python
# ...

from app import routes, models, errors
```

