'''Defines the app and configures the connection to the database 
and secret key for reading forms and files'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bancodedados.db"
app.config["SECRET_KEY"] = "aaeee19c0e0f4c5b6d081f66c6dd56ef"

database = SQLAlchemy(app)

from recomb import routes
