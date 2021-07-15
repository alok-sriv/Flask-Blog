#Flask-Blog > blog > routes.py
from flask import render_template, flash, redirect, url_for, request
from blog import app, db, bcrypt
from blog.forms import LoginForm, RegistrationForm
from blog.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

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
    return render_template('home.html', title='Home Page', posts= posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))     
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')