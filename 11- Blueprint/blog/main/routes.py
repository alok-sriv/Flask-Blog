from blog.models import Post
from blog.config import Config
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=Config.PER_PAGE_POSTS)
    return render_template('main/home.html', title='Home Page', posts= posts)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')
