from os import getenv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
database_path = getenv("DATABASE_URL")
database_path = (database_path.replace("postgres", "postgresql") if database_path.split(
    ":")[0] == "postgres" else database_path) if database_path else None
now = datetime.now()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path or "sqlite:///database/database.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.app = app
    return db

def append_data():
    actor1 = Actor(name="Taner Olmez", age=30, gender="man")
    actor2 = Actor(name="Sinem Unsal", age=29, gender="woman")
    genre1 = MovieGenre(genre_name="adventure")
    genre2 = MovieGenre(genre_name="science-fiction")
    movie1 = Movie(title="Mucize Doktor", release_date="12/12/2019")
    movie2 = Movie(title="Lucy", release_date="12/12/2006")
    actor1.insert(), actor2.insert()
    genre1.insert(), genre2.insert()
    movie1.insert(), movie2.insert()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# =================== #
# Association Tables  #
# =================== #


movie_genres = db.Table("movie_genres",
                        db.Column("movie_id", db.Integer, db.ForeignKey(
                            "movies.id"), primary_key=True),
                        db.Column("genre_id", db.Integer, db.ForeignKey(
                            "genres.id"), primary_key=True)
                        )

movie_actors = db.Table("movie_actors",
                        db.Column("movie_id", db.Integer, db.ForeignKey(
                            "movies.id"), primary_key=True),
                        db.Column("actor_id", db.Integer, db.ForeignKey(
                            "actors.id"), primary_key=True)
                        )

# =========== #
# Movie Model #
# =========== #


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.String(), nullable=False,
                             default=now.strftime("%d/%m/%Y"))
    genres = db.relationship("MovieGenre", secondary=movie_genres, backref=db.backref(
        "related_movies", lazy="joined"))
    related_actors = db.relationship(
        "Actor", secondary=movie_actors, backref=db.backref("related_movies", lazy="joined"))

    def __init__(self, title, release_date=datetime.today()):
        self.title = title
        self.release_date = release_date

    def short(self):
        return {
            "id": self.id,
            "title": self.title
        }

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "movie_genres": [genre.short() for genre in self.genres],
            "movie_actors": [actor.short() for actor in self.related_actors]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<{}>".format(self.title)

# ================== #
# Movie Genre Model  #
# ================== #


class MovieGenre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(), nullable=False, unique=True)

    def __init__(self, genre_name):
        self.genre_name = genre_name

    def short(self):
        return {
            "id": self.id,
            "genre_name": self.genre_name
        }

    def format(self):
        return {
            "id": self.id,
            "genre_name": self.genre_name,
            "movies_in_this_genre": [movie.short() for movie in self.related_movies]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# =========== #
# Actor Model #
# =========== #


class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movies": [movie.short() for movie in self.related_movies]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<{}>".format(self.name)
