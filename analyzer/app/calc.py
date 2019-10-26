from flask.ext.classy import FlaskView, route
from flask import request
from models import MovieGenre, Movies, User, UserViews, MovieActors
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import threading
from sqlalchemy import load_only
import pandas as pd


class Trainer:  
    
    def __init__(self):
        self.userviews = []
        self.actors = []
    
    def get_actors(self):
        # get all movie actors.
        actors = []
        for j in self.userviews:
            # get actors.
            movie_actors = MovieActors.query.filter(
                MovieActors.movies_id == j.movies_id).options(
                    load_only('actors_id'))
            temp = dict()
            temp['movies_id'] = j.movies_id
            temp['actors'] = movie_actors
            actors.append(temp)
        self.actors = actors
    
    def get_genres(self):

    def train(self, user_id):
        # get movies
        userViews = UserViews.query.filter(UserViews.user_id == user_id).all()
        self.userviews = userViews
        # thread get actors
        thread1 = threading.Thread(target=self.get_actors, args=(self))
        thread2 = threading.Thread(target=self.get_genres, args=(self))
        # thread to get genre
        # continue to get ratings
        # after ratings
