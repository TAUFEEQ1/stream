from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
#init flask app
app = Flask(__name__)
#sqlite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://../../flick'
from app import app
db = SQLAlchemy(app)
#redis config
r = redis.Redis(host='localhost', port=6379, db=0)
#PUBSUB OBJECT.
p = r.pubsub()
