from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://../../flick'
db = SQLAlchemy(app)
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
