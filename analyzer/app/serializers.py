from . import ma
from models import Movies


class MovieSchema(ma.Schema):
    class Meta:
        model = Movies
