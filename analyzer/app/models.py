from app import db


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    subtitle = db.Column(db.String)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    other = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class MovieActors():
    __tablename__ = 'movieactors'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.movies_id'),
        nullable=False)
    actors_id = db.Column(
        db.Integer,
        db.ForeignKey('actors.id')
    )


class Synopsis(db.Model):
    __tablename__ = 'synopsis'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.movies_id'),
        nullable=False)
    synopsis = db.Column(db.Text)


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String, unique=True)


class MovieGenre(db.Model):
    __tablename__ = 'moviegenre'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.movies_id'),
        nullable=False)
    genre_id = db.Column(
        db.Integer,
        db.ForeignKey('genre.genre_id')
    )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.String, unique=True)
    api_token = db.Column(db.String, unique=True)
    pref_model = db.relationship("User")


class UserViews(db.Model):
    __tablename__ = 'userviews'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    # start = db.Column(db.DateTime)
    # end = db.Column(db.DateTime)
    # duration = db.Column(db.Integer)


class UserPreference(db.Model):
    __tablename__ = 'userpref'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    model_path = db.Column(db.String, nullable=False)


class MovieProgress(db.Model):
    __tablename__ = 'movieprogress'
    id = db.Column(db.Integer, primary_key=True)
    cur_seg = db.Column(db.Integer)
    total_seg = db.Column(db.Integer)
    userview_id = db.Column(
        db.Integer,
        db.ForeignKey('userviews.id'),
        nullable=False
    )


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    amount = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class OrderType(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    type = db.Column(db.String, unique=True)


class OrderContent(db.Model):
    __tablename__ = 'ordercontent'
    id = db.Column(db.Integer)
    order_id = db.Column(
       db.Integer,
       db.ForeignKey('order.id'),
       nullable=False
    )
    movies_id = db.Column(
        db.Integer,
        db.ForeignKey('movies_id'),
        nullable=False
    )
    status = db.Column(db.Boolean)
    ordertype_id = db.Column(
        db.Integer,
        db.ForeignKey('ordertype.id')
    )
