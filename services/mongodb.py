from flask_pymongo import PyMongo
import flask
import certifi

app = flask.Flask(__name__)

username = 'amya'
password = 'amit9799'

app.config["MONGO_URI"] = "mongodb+srv://amya:amit9799@cluster0.jya5k.mongodb.net/portfolio?retryWrites=true&w=majority"
mongodb_client = PyMongo(app , tlsCAFile=certifi.where())
