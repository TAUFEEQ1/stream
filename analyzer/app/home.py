from flask_classy import FlaskView, route
from flask import jsonify, redirect
from flask import request, url_for
from models import MovieGenre, Movies, User, MovieActors, UserPreference
# from models import UserViews
import pickle
from app import db
from sqlalchemy.orm import load_only
import numpy as np
from serializers import MovieSchema


class HomeView(FlaskView):
    route_base = '/home/'

    def __init__(self):
        self.userPref = ''
        self.genres_labeler = ''
        self.actors_labeler = ''

    def detPref(self, themovie):
        new_mov = Movies.query.get(themovie.movie_id)
        actors = MovieActors.query.filter(
            MovieActors.movies_id == themovie.movie_id
        ).options(
            load_only('actors_id')
        ).all()
        genres = MovieGenre.query.filter(
            MovieGenre.movies_id == themovie.movie_id
        ).options(
            load_only('genres_id')
        ).all()
        genrez = np.array(genres)
        actorz = np.array(actors)
        genz = self.genres_labeler.transform(genrez)[0]
        actaz = self.actors_labeler.transform(actorz)[0]
        merged = np.concatenate((genz, actaz), axis=0)
        theanswer = self.userPref.predict([merged])[0]
        if (theanswer):
            return new_mov

    @route('get_recommended', methods=['GET'])
    def get_recommended(self):
        # count user views
        thefilter = request.json
        thequery = db.session.query(MovieGenre).join(Movies)
        if 'categories' in thefilter:
            genres = thefilter['categories']
            thequery = thequery.filter(
                MovieGenre.genre_id.in_(genres))

        if 'daterange' in thefilter:
            dates = thefilter['daterange']
            thequery = thequery.filter(
                Movies.created_at.between(dates[0], dates[1])
            )
        themovies = thequery.all()
        userid = thefilter['user_id']
        user = User.query.get(userid)
        model_path = UserPreference.query.filter(
            UserPreference.user_id == user.user_id
        ).options(
            load_only('model_path')
        ).first()
        if(model_path):
            self.userPref = pickle.load(open(model_path, 'rb'))
            self.genres_labeler = pickle.load(open('genreslabeler', 'rb'))
            self.actors_labeler = pickle.load(open('actorslabeler', 'rb'))
            recommended = list(map(self.detPref, themovies))
            recommended = list(filter(None, recommended))
            return jsonify(MovieSchema(recommended))
        else:
            redirect(url_for('get_popular'), code=307)
