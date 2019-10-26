from flask.ext.classy import FlaskView, route
from flask import request
from models import MovieGenre, Movies, User
import pickle
from sklearn.preprocessing import MultiLabelBinarizer

class Trainer:
    
    def __init(self):
        self.user_id = ''
    
    def train(self):
        