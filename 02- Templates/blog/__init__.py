from flask import Flask

# print(f"In __init__.py: {__name__}") o/p : In __init__.py: blog

app = Flask(__name__)

from blog import routes