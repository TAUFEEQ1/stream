# from flask.ext.classy import FlaskView, route
# from flask import request
from models import MovieGenre, UserViews, MovieActors, UserPreference
from models import Actors, Genre
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import threading
from sqlalchemy import load_only
import pandas as pd
import numpy as np
from . import socketio, r, p, db
import json
from sklearn.linear_model import LinearRegression
import uuid


class Trainer:

    def __init__(self):
        self.userviews = []
        self.user_id = 0
        self.glisten = True

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
        if r.get('genrez') and r.get('mratings'):
            r.publish('encoding', 'done')

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
        if r.get('actors') and r.get('mratings'):
            r.publish('encoding', 'done')

    def get_ratings(self):
        ratings = dict()
        ratings['movies_id'] = list()
        ratings['ratings'] = list()
        for j in self.userviews:
            ratings['movies_id'].append(j.id)
            ratings['ratings'].append(j.ratings)
        r.set('mratings', json.dumps(ratings))
        if r.get('actors') and r.get('genrez'):
            r.publish('encoding', 'done')

    @socketio.on('usertrain')
    def train(self, user_id):
        self.user_id = user_id
        # get movies
        userViews = UserViews.query.filter(UserViews.user_id == user_id).all()
        self.userviews = userViews
        # thread get actors
        thread1 = threading.Thread(target=self.get_actors, args=(self))
        thread2 = threading.Thread(target=self.get_genres, args=(self))
        thread3 = threading.Thread(target=self.get_ratings, args=(self))
        thread1.start()
        thread2.start()
        thread3.start()

        def trainer(thedata):
            y = thedata['ratings']
            X = thedata[['genres', 'actors']]
            reg = LinearRegression().fit(X, y)
            theid = str(uuid.uuid4())
            modelpath = "models/{0}/{1}".format(user_id, theid)
            pickle.dump(reg, open(modelpath, 'wb'))
            user_pref = UserPreference()
            user_pref.user_id = self.user_id
            user_pref.model_path = modelpath
            db.session.add(user_pref)
            db.session.commit()

        def encoding_done(msg):
            genz = json.loads(r.get('genrez'))
            actors = json.loads(r.get('actors'))
            ratings = json.loads(r.get('mratings'))
            df1 = pd.DataFrame(genz)
            df2 = pd.DataFrame(actors)
            df3 = pd.DataFrame(ratings)
            # join two tables
            thedata = pd.merge(df1, df2, df3, on='movies_id')
            trainer(thedata)
            self.glisten = False
            thread1.join()
            thread2.join()
            thread3.join()
        while self.glisten:
            p.subscribe(**{'encoding': encoding_done})
