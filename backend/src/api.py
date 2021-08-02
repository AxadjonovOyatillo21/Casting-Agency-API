import re
import os
from flask import (
    Flask,
    jsonify,
    request,
    abort
)
from flask_cors import CORS
import flask_cors.decorator as decorator
from sqlalchemy.exc import SQLAlchemyError
from .database.models import (
    Actor,
    MovieGenre,
    Movie,
    db,
    setup_db
)
from .auth import (
    AUTH0_DOMAIN,
    API_AUDIENCE,
    AuthError,
    requires_auth)
from .utils import (
    check_actor,
    check_movie,
    string_validator,
    age_validator,
    id_validator,
    man_or_woman,
    date_validator,
    paginate_data,
    check_genre,
    DataBaseError
)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KET"] = os.urandom(50)
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
    setup_db(app)

    @app.after_request
    def after_reuqest(response):
        header = response.headers
        header["Access-Control-Allow-Origins"] = "*"
        header["Access-Control-Allosw-Methods"] = "GET, POST, PATCH, DELETE"
        header["Server"] = "Casting Agency"
        return response

    #========#
    # Routes #
    #========#

    @app.route('/api')
    @decorator.cross_origin()
    def home_page():
        return jsonify({
            "success": True,
            "message": "Casting agency is running 🚀✨"
        })

    @app.route('/api/actors')
    @decorator.cross_origin()
    def get_actors():
        actors = [actor.short()
                  for actor in Actor.query.order_by(Actor.id).all()]
        current_actors = paginate_data(request, actors)
        return jsonify({
            "success": True,
            "actors": current_actors,
            "total_actors": len(current_actors)
        })

    @app.route('/api/movies')
    @decorator.cross_origin()
    def get_movies():
        movies = [movie.short()
                  for movie in Movie.query.order_by(Movie.id).all()]
        current_movies = paginate_data(request, movies)
        return jsonify({
            "success": True,
            "movies": current_movies,
            "total_movies": len(current_movies)
        })

    @app.route('/api/genres')
    @decorator.cross_origin()
    def get_genres():
        genres = [genre.short()
                  for genre in MovieGenre.query.order_by(MovieGenre.id).all()]
        current_genres = paginate_data(request, genres)
        return jsonify({
            "success": True,
            "genres": current_genres,
            "total_genres": len(current_genres)
        })

    @app.route('/api/actors-detail')
    @decorator.cross_origin()
    @requires_auth("view:actors")
    def get_actors_detail(payload):
        actors = [actor.format()
                  for actor in Actor.query.order_by(Actor.id).all()]
        current_actors = paginate_data(request, actors)
        return jsonify({
            "success": True,
            "actors": current_actors,
            "total_actors": len(current_actors)
        })

    @app.route("/api/movies-detail")
    @decorator.cross_origin()
    @requires_auth("view:movies")
    def get_movies_detail(payload):
        movies = [movie.format()
                  for movie in Movie.query.order_by(Movie.id).all()]
        current_movies = paginate_data(request, movies)
        return jsonify({
            "success": True,
            "movies": current_movies,
            "total_movies": len(current_movies)
        })

    @app.route('/api/genres-detail')
    @decorator.cross_origin()
    @requires_auth("view:genres")
    def get_genres_detail(payload):
        genres = [genre.format()
                  for genre in MovieGenre.query.order_by(MovieGenre.id).all()]
        current_genres = paginate_data(request, genres)
        return jsonify({
            "success": True,
            "genres": current_genres,
            "total_genres": len(MovieGenre.query.all())
        })

    @app.route('/api/genres', methods=["POST"])
    @decorator.cross_origin()
    @requires_auth("add:genres")
    def add_genre(payload):
        data = request.get_json() or abort(400)
        genre_name = data.get("genre_name", None) or abort(400)

        if string_validator(genre_name):
            try:
                genre = MovieGenre(genre_name=genre_name)
                genre.insert()
                return jsonify({
                    "success": True,
                    "created": True,
                    "genre": genre.format(),
                    "total_genres": len(MovieGenre.query.all())
                })
            except SQLAlchemyError:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()
        else:
            abort(400)


    @app.route("/api/genres/<int:genre_id>")
    @decorator.cross_origin()
    @requires_auth("view:genres")
    def get_single_genre(payload, genre_id: int):
        genre = MovieGenre.query.get(genre_id)
        check_genre(genre, genre_id)

        return jsonify({
            "success": True,
            "genre": genre.format(),
            "total_genres": len(MovieGenre.query.all())
        })

    @app.route("/api/genres/<int:genre_id>", methods=["PATCH"])
    @decorator.cross_origin()
    @requires_auth("update:genres")
    def update_genre(payload, genre_id: int):
        genre = MovieGenre.query.get(genre_id)
        check_genre(genre, genre_id)
        data = request.get_json() or {}
        genre_name = data.get("genre_name", None)

        if string_validator(genre_name):
            genre.genre_name = genre_name

        try:
            genre.update()
            return jsonify({
                "success": True,
                "updated": True,
                "genre": genre.short(),
                "total_genres": len(MovieGenre.query.all())
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route("/api/genres/<int:genre_id>", methods=["DELETE"])
    @decorator.cross_origin()
    @requires_auth("delete:genres")
    def delete(payload, genre_id: int):
        genre = MovieGenre.query.get(genre_id)
        check_genre(genre, genre_id)

        try:
            genre.delete()
            return jsonify({
                "success": True,
                "deleted_id": genre.id,
                "total_genres": len(MovieGenre.query.all())
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route("/api/actors", methods=["POST"])
    @decorator.cross_origin()
    @requires_auth("add:actors")
    def add_actors(payload):
        data = request.get_json() or abort(400)
        name = data.get("name", None) or abort(400)
        age = data.get("age", 0) or abort(400)
        gender = data.get("gender", None) or abort(400)
        movies_id = data.get("movies_id", None)

        if string_validator(name) and age_validator(age) and man_or_woman(gender):
            try:
                actor = Actor(name=name, age=age, gender=gender)
                if id_validator(movies_id):
                    for movie_id in movies_id:
                        movie_id = int(movie_id)
                        movie = Movie.query.get(movie_id) or abort(400)
                        if movie not in actor.related_movies:
                            actor.related_movies.append(movie)
                actor.insert()
                return jsonify({
                    "success": True,
                    "created": True,
                    "actor": actor.short(),
                    "total_actors": len(Actor.query.all())
                })
            except SQLAlchemyError:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()
        else:
            abort(400)



    @app.route("/api/actors/<int:actor_id>")
    @decorator.cross_origin()
    @requires_auth("view:actors")
    def get_single_actor(payload, actor_id: int):
        actor = Actor.query.get(actor_id)
        check_actor(actor, actor_id)

        return jsonify({
            "success": True,
            "actor": actor.format(),
            "total_actors": len(Actor.query.all())
        })

    @app.route("/api/actors/<int:actor_id>", methods=['DELETE'])
    @decorator.cross_origin()
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id: int):
        actor = Actor.query.get(actor_id)
        check_actor(actor, actor_id)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted_id": actor.id,
                "total_actors": len(Actor.query.all())
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route("/api/actors/<int:actor_id>", methods=["PATCH"])
    @decorator.cross_origin()
    @requires_auth("update:actors")
    def update_actor(payload, actor_id: int):
        actor = Actor.query.get(actor_id)
        check_actor(actor, actor_id)
        data = request.get_json() or {}
        name = data.get("name", None)
        age = data.get("age", 0)
        gender = data.get("gender", None)
        movies_id = data.get("movies_id", None)
        remove_movies_id = data.get("remove_movies_id", None)

        if string_validator(name):
            actor.name = name
        if age_validator(age):
            actor.age = age
        if man_or_woman(gender):
            actor.gender = gender
        if id_validator(movies_id):
            for movie_id in movies_id:
                movie_id = int(movie_id)
                movie = Movie.query.get(movie_id) or abort(400)
                if movie not in actor.related_movies:
                    actor.related_movies.append(movie)
        if id_validator(remove_movies_id):
            for remove_movie_id in remove_movies_id:
                remove_movie_id = int(remove_movie_id)
                remove_movie = Movie.query.get(remove_movie_id) or abort(400)
                if remove_movie in actor.related_movies:
                    actor.related_movies.remove(remove_movie)

        try:
            actor.update()
            return jsonify({
                "success": True,
                "updated": True,
                "actor": actor.short(),
                "total_actors": len(Actor.query.all())
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()



    @app.route("/api/movies", methods=["POST"])
    @decorator.cross_origin()
    @requires_auth("add:movies")
    def add_movie(payload):
        data = request.get_json() or abort(400)
        title = data.get("title", None) or abort(400)
        release_date = data.get("release_date", None) or abort(400)
        actors_id = data.get("actors_id", None)
        genres_id = data.get("genres_id", None)

        if string_validator(title) and date_validator(release_date):
            try:
                movie = Movie(title=title, release_date=release_date)
                if id_validator(actors_id):
                    for actor_id in actors_id:
                        actor_id = int(actor_id)
                        actor = Actor.query.get(actor_id) or abort(400)
                        if actor not in movie.related_actors:
                            movie.related_actors.append(actor)
                if id_validator(genres_id):
                    for genre_id in genres_id:
                        genre_id = int(genre_id)
                        genre = MovieGenre.query.get(genre_id) or abort(400)
                        if genre not in movie.genres:
                            movie.genres.append(genre)
                movie.insert()
                return jsonify({
                    "success": True,
                    "created": True,
                    "movie": movie.short(),
                    "total_movies": len(Movie.query.all())
                })
            except SQLAlchemyError:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()
        else:
            abort(400)



    @app.route("/api/movies/<int:movie_id>")
    @decorator.cross_origin()
    @requires_auth("view:movies")
    def get_single_movie(payload, movie_id: int):
        movie = Movie.query.get(movie_id)
        check_movie(movie, movie_id)
        return jsonify({
            "success": True,
            "movie": movie.format(),
            "total_movies": len(Movie.query.all())
        })

    @app.route("/api/movies/<int:movie_id>", methods=["PATCH"])
    @decorator.cross_origin()
    @requires_auth("update:movies")
    def update_movies(payload, movie_id: int):
        movie = Movie.query.get(movie_id)
        check_movie(movie, movie_id)
        data = request.get_json() or {}
        title = data.get("title", None)
        release_date = data.get("release_date", None)
        actors_id = data.get("actors_id", None)
        genres_id = data.get("genres_id", None)
        remove_actors_id = data.get("remove_actors_id", None)
        remove_genres_id = data.get("remove_genres_id", None)

        if string_validator(title):
            movie.title = title

        if date_validator(release_date):
            movie.release_date = release_date

        if id_validator(actors_id):
            for actor_id in actors_id:
                actor_id = int(actor_id)
                actor = Actor.query.get(actor_id) or abort(400)
                if actor not in movie.related_actors:
                    movie.related_actors.append(actor)

        if id_validator(remove_actors_id):
            for remove_actor_id in remove_actors_id:
                remove_actor_id = int(remove_actor_id)
                remove_actor = Actor.query.get(remove_actor_id) or abort(400)
                if remove_actor in movie.related_actors:
                    movie.related_actors.remove(remove_actor)

        if id_validator(genres_id):
            for genre_id in genres_id:
                genre_id = int(genre_id)
                genre = MovieGenre.query.get(genre_id) or abort(400)
                if genre not in movie.genres:
                    movie.genres.append(genre)

        if id_validator(remove_genres_id):
            for remove_genre_id in remove_genres_id:
                remove_genre_id = int(remove_genre_id)
                remove_genre = MovieGenre.query.get(
                    remove_genre_id) or abort(400)
                if remove_genre in movie.genres:
                    movie.genres.remove(remove_genre)

        try:
            movie.update()
            return jsonify({
                "succes": True,
                "updated": True,
                "movie": movie.short(),
                "total_movies": len(Movie.query.all())
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()



    @app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
    @decorator.cross_origin()
    @requires_auth("delete:movies")
    def delete_movies(payload, movie_id: int):
        movie = Movie.query.get(movie_id)
        check_movie(movie, movie_id)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted_id": movie.id,
                "total_movies": len(Movie.query.all())
            })
        except SQLAlchemyError:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()



    #====================#
    #                    #
    # API error handlers #
    #                    #
    #====================#

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "success": False,
            "error_code": 400,
            "error_message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({
            "success": False,
            "error_code": 401,
            "error_message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({
            "success": False,
            "error_code": 403,
            "error_message": "Access Denied"
        }), 403

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({
            "success": False,
            "error_code": 404,
            "error_message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "success": False,
            "error_code": 405,
            "error_message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify({
            "success": False,
            "error_code": 422,
            "error_message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            "success": False,
            "error_code": 500,
            "error_message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def authentication_error(e: AuthError):
        return jsonify({
            "success": False,
            "error_code": e.status_code,
            "erorr_message": e.error["description"]
        }), e.status_code

    @app.errorhandler(DataBaseError)
    def database_error(e: DataBaseError):
        return jsonify({
            "success": False,
            "error_code": e.status_code,
            "error_message": e.error["message"]
        }), e.status_code

    return app


app = create_app()
