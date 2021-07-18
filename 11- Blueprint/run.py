# FileName: Flask-Blog > run.py
from blog import create_app

app = create_app()

# print(f"In blog.py: {__name__}") o/p: In blog.py: __main__
if __name__ == '__main__':
    app.run() 