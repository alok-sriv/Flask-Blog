#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for
from blog import app
from blog.forms import LoginForm, RegistrationForm

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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)