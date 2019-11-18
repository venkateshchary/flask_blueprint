from flask import Flask
from .flaskbp import dashboard
from .dataview import data
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.register_blueprint(dashboard)
app.register_blueprint(data, url_prefix="/data")
