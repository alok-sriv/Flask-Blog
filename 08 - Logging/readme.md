**Debug Mode**</br>
When you are developing your application, you can enable debug mode, a mode in which Flask outputs a really nice debugger directly on your browser. To activate debug mode, stop the application, and then set the following environment variable:

> (env)$FLASK_ENV=development

After you set FLASK_ENV, restart the server. The output on your terminal is going to be slightly different than what you are used to see.

It is extremely important that you never run a Flask application in debug mode on a production server. The debugger allows the user to remotely execute code in the server, so it can be an unexpected gift to a malicious user who wants to infiltrate your application or your server. As an additional security measure, the debugger running in the browser starts locked, and on first use will ask for a PIN number, which you can see in the output of the "flask run or pyton blog.py" command.

Since I am in the topic of debug mode, I should mention the second important feature that is enabled with debug mode, which is the reloader. This is a very useful development feature that automatically restarts the application when a source file is modified. If you run flask while in debug mode, you can then work on your application and any time you save a file, the application will restart to pick up the new code.


**Logging to a File**</br>
To enable a file based log another handler, this time of type RotatingFileHandler, needs to be attached to the application logger.

**\_\_init\_\_.py**
```python
# ...
from logging.handlers import RotatingFileHandler
import os
..........
..........
if not app.debug: # To enable logger when the application is running without debug mode, which is indicated by app.debug being True. I have commented this in my actual code
                  # as i want to keep logs on OS irrespective of debug mode.
  if not os.path.exists('logs'):
      os.mkdir('logs')
  file_handler = RotatingFileHandler('logs/blog.log', maxBytes=10240,backupCount=10)
  # file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')) # for more detailed output
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

  logging.getLogger('werkzeug').setLevel(logging.DEBUG)
  logging.getLogger('werkzeug').addHandler(file_handler)
  
  #below code will add "Blog Startup" message in logs and on CMD( where you run your app) everytime app restarts
  app.logger.addHandler(file_handler)
  app.logger.info('Blog startup')

```
**Explanation**</br>
1. I'm writing the log file with name microblog.log in a logs directory, which I create if it doesn't already exist.

2. The RotatingFileHandler class is nice because it rotates the logs, ensuring that the log files do not grow too large when the application runs for a long time. In this case I'm limiting the size of the log file to 10KB, and I'm keeping the last ten log files as backup.

3. The logging.Formatter class provides custom formatting for the log messages. Since these messages are going to a file, I want them to have as much information as possible. So I'm using a format that includes the timestamp, the logging level, the message and the source file and line number from where the log entry originated.

4. I have used logging level as DEBUG. In case you are not familiar with the logging categories, they are DEBUG, INFO, WARNING, ERROR and CRITICAL in increasing order of severity.

**Environment Variables**</br>

```python
(env) $Flask-Blog>pip install python-dotenv
Collecting python-dotenv
  Downloading python_dotenv-0.18.0-py2.py3-none-any.whl (18 kB)
Installing collected packages: python-dotenv
Successfully installed python-dotenv-0.18.0
```

As you have seen as I built this application, there are a number of configuration options that depend on having variables set up in your environment before you start the server. This includes your secret key, email server information, database URL, and Microsoft Translator API key. You'll probably agree with me that this is inconvenient, because each time you open a new terminal session those variables need to be set again.

A common pattern for applications that depend on lots of environment variables is to store these in a .env file in the root application directory. The application imports the variables in this file when it starts, and that way, there is no need to have all these variables manually set by you.

There is a Python package that supports .env files called python-dotenv, and it is already installed because I used it with the .flaskenv file earlier in the tutorial. While the .env and .flaskenv files are similar, Flask expects Flask's own configuration variables to be in .flaskenv, while application configuration variables (including some that can be of a sensitive nature) to be in .env. The .flaskenv file can be added to your source control, as it does not contain any secrets or passwords. The .env file is not supposed to be added to source control to ensure that your secrets are protected.

The flask command automatically imports into the environment any variables defined in the .flaskenv and .env files. This is sufficient for the .flaskenv file, because its contents are only needed when running the application through the flask command. The .env file, however, is going to be used also in the production deployment of this application, which is not going to use the flask command. For that reason, it is a good idea to explicitly import the contents of the .env file.

Since the config.py module is where I read all the environment variables, I'm going to import the .env file before the Config class is created, so that the variables are already set when the class is constructed:

```python
# FileName: Flask-Blog > blog > config.py
import os, secrets
from dotenv import load_dotenv

basedir = os.path.dirname(__file__) # __file__ represents current file. and basedir will have directory of current file e.g. config.py o/p: Flask-Blog\blog
rootdir = os.path.dirname(basedir)  # directory of basedir i.e. Flask-Blog
load_dotenv(os.path.join(rootdir, '.env'))

...........
```

I will keep .env and .flaskenv files in root diretory e.g. Flask-Blog.

**.env file**</br>
```python
MYSQL_PASSWORD=xxxxxxxx
```
**.flaskenv**</br>
```python
FLASK_APP=blog.py
FLASK_ENV=development
```

**Start Application**</br>
1. Enable Virtual Environment
2. flask run
