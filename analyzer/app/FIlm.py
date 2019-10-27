from flask.ext.classy import FlaskView, route
from flask import request, jsonify
# from models import MovieGenre, Movies, User
from . import r, q
from calc import calc
from models import UserPreference, Actors


class Film(FlaskView):
    route_base = '/film/'
    @route('onrate', methods=['GET'])
    def onrate(self):
        user_id = request.args.get('user_id')
        userRate = 'userRate_' + user_id
        lenq = r.lLen(userRate)
        if lenq > 5:
            calculate = calc(user_id=user_id)
            user_model = UserPreference.query.filter(
                UserPreference.user_id == user_id
            ).first()
            # check actors catalog.
            nactors = r.lLen('nactors')
            if (nactors/Actors.query.count()) > 0.14:
                user_model = False

            if user_model:
                #
                job = q.enqueue(calculate.retrain)
                return jsonify({
                    'status': 1,
                    'message': 'user preferences relearn',
                    'job_id': job.id})
            else:
                job = q.enqueue(calculate.train)
                return jsonify({
                    'status': 2,
                    'message': 'user preferences learn',
                    'job_id': job.id
                })
        else:
            return jsonify({
                'status': 0,
                'message': 'user preferences tobe learned',
                'job_id': -1
            })
