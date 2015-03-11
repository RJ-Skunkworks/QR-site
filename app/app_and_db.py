from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is the WSGI compliant web application object
app = Flask(__name__)

# This is the SQLAlchemy ORM object
db = SQLAlchemy(app)
