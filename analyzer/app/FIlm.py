from flask.ext.classy import FlaskView, route
from flask import request
from models import MovieGenre, Movies, User

class Film(FlaskView):
    
    def trainRecomEngine(self):
        
