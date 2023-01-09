from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from os import urandom, getcwd


app = Flask(__name__)

# Configuring folder for uploading files
app.config['UPLOAD_FOLDER'] = getcwd() + '/gis/static'

# Only .csv is allowed for upload
app.config['UPLOAD_EXTENSIONS'] = ['.csv']

app.config['SECRET_KEY'] = urandom(12)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gis.db'

# Initializing database
db = SQLAlchemy(app)

# I wasn't able to run the app until i moved this import to the bottom of the file
from gis import routes
