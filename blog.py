from blog import app

# print(f"In blog.py: {__name__}") o/p: In blog.py: __main__
if __name__ == '__main__':
    app.run(debug=True) 