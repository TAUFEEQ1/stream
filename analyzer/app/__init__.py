from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import redis


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://../../flick'
db = SQLAlchemy(app)
socketio = SocketIO(app)
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
