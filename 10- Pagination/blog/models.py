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

