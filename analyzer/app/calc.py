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
from . import r, p, db
import json
from sklearn.linear_model import LinearRegression
import uuid


class Trainer:

    def __init__(self, user_id=0):
        self.userviews = []
        self.user_id = 0
        self.glisten = True

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
        # get all actors
        actarz = Actors.query.all()
        colnames = ['movies_id']
        for a in actarz:
            colnames.append('a_'+a.id)

        # get all movie actors.
        actors = pd.DataFrame(columns=colnames)
        for j in self.userviews:
            # get actors.
            movie_actors = MovieActors.query.filter(
                MovieActors.movies_id == j.id).options(
                    load_only('actors_id'))
            new_row = [j.id]
            mactors = np.array(movie_actors)
            # tactorz = np.reshape(mactors, (-1,4))
            new_row.extend(actors_labeler(mactors)[0])
            actors.loc[len(actors)] = new_row
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
        allgens = Genre.query.all()
        colnames = ['movies_id']
        for k in allgens:
            colnames.append('g_'+k.id)
        genz = pd.DataFrame(columns=colnames)
        genres_labeler = pickle.load(open('genreslabeler', 'rb'))
        for j in self.userviews:
            genres = MovieGenre.query.filter(
                MovieGenre.movies_id == j.id).options(
                    load_only('movies_id')
            )
            genrez = np.array(genres)
            tgenrez = np.reshape(genrez, (-1, 1))
            new_row = [j.id]
            new_row.extend(genres_labeler(tgenrez)[0])
            genz.loc[len(genz)] = new_row
        r.set('genrez', json.dumps(genz.to_dict()))
        if r.get('actors') and r.get('mratings'):
            r.publish('encoding', 'done')

    def get_ratings(self):
        ratings = pd.DataFrame(columns=['movies_id', 'ratings'])
        for j in self.userviews:
            new_row = [j.id, j.ratings]
            ratings.loc[len(ratings)] = new_row
        r.set('mratings', json.dumps(ratings.to_dict()))
        if r.get('actors') and r.get('genrez'):
            r.publish('encoding', 'done')

    def train(self):
        # get movies
        userViews = UserViews.query.filter(
            UserViews.user_id == self.user_id).all()
        self.userviews = userViews
        self.genres_label()
        self.actors_label()
        # thread get actors
        thread1 = threading.Thread(target=self.get_actors, args=(self))
        thread2 = threading.Thread(target=self.get_genres, args=(self))
        thread3 = threading.Thread(target=self.get_ratings, args=(self))
        thread1.start()
        thread2.start()
        thread3.start()

        def trainer(thedata):
            y = thedata['ratings'].to_numpy()
            thedata.drop(['ratings'], axis=1)
            X = thedata.to_numpy()
            reg = LinearRegression().fit(X, y)
            theid = str(uuid.uuid4())
            modelpath = "models/{0}/{1}".format(self.user_id, theid)
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
            thedata.drop(['movies_id'], axis=1)
            trainer(thedata)
            self.glisten = False
            thread1.join()
            thread2.join()
            thread3.join()
        while self.glisten:
            p.subscribe(**{'encoding': encoding_done})

    def retrain(self):
        # Label the new entrants
        actors_labeler = pickle.load(open('actorslabeler', 'rb'))
        genres_labeler = pickle.load(open('genreslabeler', 'rb'))
        userRate = 'userRate_' + self.user_id
        uviews = r.lrange(userRate, 0, -1)
        y = []
        X = []
        for j in uviews:
            userview = UserViews.query.get(j)
            movie = userview.movie
            actors = movie.actors
            actor_idz = [x.actors_id for x in actors]
            actorz = np.array(actor_idz)
            tactorz = np.reshape(actorz, (-1, 1))
            actarz = actors_labeler(tactorz)[0]
            genres = movie.genres
            genrez = np.array(genres)
            tgenrez = np.reshape(genrez, (-1, 1))
            genz = genres_labeler(tgenrez)[0]
            lbl = np.hstack(genz, actarz)
            X.append(lbl)
            ratings = userview.ratings
            y.append(ratings)
        user_model = UserPreference.query.filter(
            UserPreference.user_id == self.user_id).first()
        userPref = pickle.load(open(user_model.model_path, 'rb'))
        userPref.fit(X, y)

        theid = str(uuid.uuid4())
        npath = 'models/{0}/{1}'.format(self.user_id, theid)
        pickle.dump(userPref, open(npath, 'wb'))
        userp = UserPreference.query.get(user_model.id)
        userp.model_path = npath
        db.session.commit()
