# from flask.ext.classy import FlaskView, route
# from flask import request
from models import MovieGenre, UserViews, MovieActors
from models import Actors, Genre
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import threading
from sqlalchemy import load_only
import pandas as pd
import numpy as np
from . import socketio, r
import json


class Trainer:

    def __init__(self):
        self.userviews = []
    
    @socketio.on('labelactors')
    def actors_label(self):
        # rank actors.
        actors = Actors.query.options(load_only('id')).all()
        mlb = MultiLabelBinarizer()
        actorz = np.array(actors)
        # for training
        tactorz = np.reshape(actorz, (-1, 1))
        mlb.fit(tactorz)
        # write to disk
        pickle.dump(mlb, open('actorslabeler', 'wb'))
    
    def get_actors(self):
        actors_labeler = pickle.load(open('actorslabeler', 'rb'))
        # get all movie actors.
        actors = dict()
        actors['movies_id'] = []
        actors['actors'] = []
        for j in self.userviews:
            # get actors.
            movie_actors = MovieActors.query.filter(
                MovieActors.movies_id == j.id).options(
                    load_only('actors_id'))
            actors['movies_id'].append(j.id)
            mactors = np.array(movie_actors)
            # tactorz = np.reshape(mactors, (-1,4))
            actors['actors'].append(actors_labeler(mactors)[0])
        r.set('actors', json.dumps(actors))
    
    def genres_label(self):
        genres = Genre.query.options(load_only('id')).all()
        mlb = MultiLabelBinarizer()
        genrez = np.array(genres)
        tgenrez = np.reshape(genrez, (-1, 1))
        mlb.fit(tgenrez)
        pickle.dump(mlb, open('genreslabeler', 'wb'))

    def get_genres(self):
        genz = dict()
        genz['movies_id'] = list()
        genz['genres'] = list()
        genres_labeler = pickle.load(open('genreslabeler', 'rb'))
        for j in self.userviews:
            genres = MovieGenre.query.filter(
                MovieGenre.movies_id == j.id).options(
                    load_only('movies_id')
                )
            genrez = np.array(genres)
            tgenrez = np.reshape(genrez, (-1, 1))
            genz['movies_id'].append(j.id)
            genz['genres'].append(genres_labeler(tgenrez)[0])
        r.set('genrez', json.dumps(genz))
    
    @socketio.on('usertrain')
    def train(self, user_id):
        # get movies
        userViews = UserViews.query.filter(UserViews.user_id == user_id).all()
        self.userviews = userViews
        # thread get actors
        thread1 = threading.Thread(target=self.get_actors, args=(self))
        thread2 = threading.Thread(target=self.get_genres, args=(self))
        thread1.start()
        thread2.start()
        # thread to get genre
        # continue to get ratings
        # after ratings

        
