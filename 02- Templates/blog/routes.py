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

