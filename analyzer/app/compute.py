from flask.ext.classy import FlaskView, route
from flask import request
from models import MovieGenre, Movies, User
import pickle
from . import db


class HomeView(FlaskView):
    route_base = '/home/'
    def __init(self):
        self.genre_encoder = ''
        self.actor_encoder = ''
        
    def detPref(self, themovie, userPref):
        new_mov = Movies.query.get(themovie.movie_id)
        actors = new_mov.actors
        genres = new_mov.genres
        actor_ids = [x.actor_id for x in actors]
        genre_idz = [x.genre_id for x in genres]
        userPref = pickle.load(open(user.pref_model.model_path, 'rb'))
        if len(actors_id) < 4:

    
    
    @route('get_recommended', method=['GET'])
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
        userPref = pickle.load(open(user.pref_model.model_path, 'rb'))
        recommended = map(lambda p: self.detPref(p, userPref), themovies)

    def get_popular(self):
        pass
