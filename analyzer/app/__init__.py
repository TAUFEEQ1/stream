from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import redis
from flask_marshmallow import Marshmallow
from rq import Queue

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://../../flick'
db = SQLAlchemy(app)
socketio = SocketIO(app)
ma = Marshmallow(app)
r = redis.Redis(host='localhost', port=6379, db=0)
q = Queue(connection=r)
p = r.pubsub()
