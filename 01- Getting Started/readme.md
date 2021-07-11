**Setup Environment**

**1. Install Python and check for version<br />**
```
python --version
Python 3.6.4rc1
```

**2. Change your current working dir to project folder ad Create Virtual Environment : python -m venv env (I have used "env" as name of my virtual environment, you can use any name).<br />**
```
cd Flask-Blog
Flask-Blog >python -m venv env
```
**3. Activate your virtual environment : env\Scripts\activate [Windows]<br />**
```
Flask-Blog >env\Scripts\activate
(env) Flask-Blog >python -m pip install --upgrade pip
Cache entry deserialization failed, entry ignored
Collecting pip
  Using cached https://files.pythonhosted.org/packages/47/ca/f0d790b6e18b3a6f3bd5e80c2ee4edbb5807286c21cdd0862ca933f751dd/pip-21.1.3-py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 9.0.1
    Uninstalling pip-9.0.1:
      Successfully uninstalled pip-9.0.1
Successfully installed pip-21.1.3
```
**4. Update PIP in virtual environment : python -m pip install --upgrade pip<br />**
```
(env) Flask-Blog >python -m pip install --upgrade pip
Cache entry deserialization failed, entry ignored
Collecting pip
  Using cached https://files.pythonhosted.org/packages/47/ca/f0d790b6e18b3a6f3bd5e80c2ee4edbb5807286c21cdd0862ca933f751dd/pip-21.1.3-py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 9.0.
    Uninstalling pip-9.0.1:
      Successfully uninstalled pip-9.0.1
Successfully installed pip-21.1.3
```
**5. Install Flask : python -m pip install flask<br />**
```
(env) Flask-Blog >python -m pip install flask
Collecting flask
.........
Installing collected packages: zipp, typing-extensions, MarkupSafe, importlib-metadata, dataclasses, colorama, Werkzeug, Jinja2, itsdangerous, click, flask
Successfully installed Jinja2-3.0.1 MarkupSafe-2.0.1 Werkzeug-2.0.1 click-8.0.1 colorama-0.4.4 dataclasses-0.8 flask-2.0.1 importlib-metadata-4.6.1
itsdangerous-2.0.1 typing-extensions-3.10.0.0 zipp-3.5.0
```

**Steps**
```
The application will exist in a package. In Python, a sub-directory that includes a __init__.py file is considered a package,
and can be imported. When you import a package, the __init__.py executes and defines what package exposes to the outside 
world.

Let's create a package called blog, that will host the application. Make sure you are in the Flask-Blog directory and then 
run the following command:
1. (env) Flask-Blog > mkdir blog
2. cd blog
3. create __init__.py: Flask application instance
4. create routes.py: Home page route
5. cd ../Flask-Blog
6. create blog.py: Main application module
7. Start Flask Application : (env) Flask-Blog >python blog.py
8. Access Application From Local Browser :  http://localhost:5000/ or  http://127.0.0.1:5000/ 
```

**Explanations**
```
__init__.py :
1. This script simply creates the application object "app" as an instance of class Flask imported from the flask package. 
In another words, the app variable is defined as an instance of class Flask imported from the flask package in the 
__init__.py script, which makes it a member of the blog package.

2. The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module
e.g. __main__in which it is used if file gets executed directly e.g. vi abc.py : print(__name__)= __main__ if we execute python 
abc.py. However, __name__ will take the name of caller module, if we don't run script directly.

3. The application then imports the routes module.

4. Another peculiarity is that the routes module is imported at the bottom and not at the top of the script as it is always 
done. The bottom import is a workaround to circular imports, a common problem with Flask applications. You are going to see 
that the routes module needs to import the app variable defined in this script, so putting one of the reciprocal imports 
at the bottom avoids the error that results from the mutual references between these two files.

5. The "blog" package is defined by the blog directory and the __init__.py script, and is referenced in the 
"from blog import routes". 
```

```
routes.py :
1. The routes are the different URLs that the application implements. 

2. In Flask, handlers for the application routes are written as Python functions, called view functions. View functions 
are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

3. The strange @app.route lines above the function are decorators, a unique feature of the Python language. 
A decorator modifies the function that follows it. A common pattern with decorators is to use them to register 
functions as callbacks for certain events. 

4. In this case, the @app.route decorator creates an association between the URL given as an argument and the function.
In this example there are two decorators, which associate the URLs / and /home to "home" function. This means that when 
a web browser requests either of these two URLs, Flask is going to invoke "home" function and pass the return value of it 
back to the browser as a response.

```
```
blog.py :
1. Import Flask Application Instance "app" from "Blog" Package.

2. debug=True : You Don't need to restart your application after making changes in code.
```
