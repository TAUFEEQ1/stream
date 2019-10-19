from flask.ext.classy import FlaskView


class HomeView(FlaskView):
    route_prefix = '/home/'

    def get_recommended(self):
        pass

    def get_popular(self):
        pass
