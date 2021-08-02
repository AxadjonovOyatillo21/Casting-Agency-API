import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.api import create_app
from src.database import setup_db, Movie, MovieGenre, Actor
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.absolute()))

database_name = "casting_agency_test"
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "pysql", "localhost:5432", database_name)


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        " Initialize Template Test Case "
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = database_name
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "pysql", "localhost:5432", self.database_name)
        self.db = setup_db(self.app, self.database_path)
        self.db.drop_all()
        self.db.create_all()

        self.correct_actor = dict(
            name="Sinem Unsal",
            age=29,
            gender="woman"
        )

        self.imporer_actor = dict(
            name="",
            age="aa2",
            gender="this is alien😂"
        )

        self.correct_movie = dict(
            title="Mucize Doctor",
            release_date="07/12/2019",
            actors_id=["0"],
            genres_id=[MovieGenre.query.first().id]
        )

        self.additional_movie = dict(
            title="Lorem Ipsum",
            release_date="04/04/2004"
        )

        self.imporer_movie = dict(
            title="0",
            release_date="223/aa/lorem",
            actors_id=["a0"]
        )

        actor = Actor(
            name="Taner O'lmez",
            age=30,
            gender="man"
        )
        actor.insert()

        actor_2 = Actor(
            name="Onur Tuna",
            age=35,
            gender="man"
        )
        actor_2.insert()

        movie = Movie(
            title="Lucy",
            release_date="21/06/2014"
        )
        movie.insert()

        genre = MovieGenre(
            genre_name="science-fiction"
        )
        genre.insert()

        genre_2 = MovieGenre(
            genre_name="adventure"
        )

        genre_2.insert()

    def tearDown(self):
        " Executed after all tests "
        pass

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })

    def post(self, *args, **kwargs):
        return self.post(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })

    def patch(self, *args, **kwargs):
        return self.client.patch(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })

    def delete(self, *args, **kwargs):
        return self.delete(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })


class PublicEndpointsTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt = ''

    "PUBLIC endpoints"

    def test_get_genres(self):
        result = self.get("api/genres")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["genres"], list)

    def test_get_actors(self):
        result = self.get("api/actors")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["actors"], list)

    def test_get_movies(self):
        result = self.get("api/movies")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["movies"], list)

    def test_get_genres_detail_for_401(self):
        result = self.get('/api/genres-detail')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_actors_detail_for_401(self):
        result = self.get('/api/actors-detail')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_movies_detail_for_401(self):
        result = self.get('/api/movies-detail')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_single_genre_for_401(self):
        genre = MovieGenre.query.first()
        result = self.get("api/genres/{}".format(genre.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_single_actor_for_401(self):
        actor = Actor.query.first()
        result = self.get("api/actors/{}".format(actor.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_single_movie_401(self):
        movie = Movie.query.first()
        result = self.get("api/movies/{}".format(movie.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


class CastingAgencyAssistantTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJtUUdqVXlNMXRyYVRhU3pIQXpqWiJ9.eyJpc3MiOiJodHRwczovL2F1dGgwLXNlcnZpY2UudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmZjMjFlMjQ1NGYyMDA2YTIzOTNlMyIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjI3ODI2MjIwLCJleHAiOjE2Mjc4MzM0MjAsImF6cCI6ImtIamVFV2pla0ZrNWtlN3NGVTBsTHp2Q3NXRmFHQUtZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6Z2VucmVzIiwidmlldzptb3ZpZXMiXX0.MR6_XtpP-JBpHMnIIu0D4xehoKetFt1iytw-n9qljKiy9vUaUOGMlj7MQ9P-f_nBUuDrLEvibUdCCxoJNpBe2jsI9YmPE5PSkyscShb0gS0b-r8e4BtjMFEtwOLtr7bOCdltuQ5gx9dgSxZn_y9vXUujzsrCOSi44LoUGBJfW-isWPFKGjFW6kS0mjGU0f8xGbyPNXA3-Eg5U9x49eeO0ICPsmsbhNjRBht0ZOgNgnjYcLT9C8wFu0VOKFE4lk1G0ZyTf16cIcp--3b4KplVakea82xlKWLdDikI9_MY_vfyTqvVVyikILl15nLg0pePw1PgR4JSxvgw7rT9eAsw-w"

    "PUBLIC endpoints"

    def test_get_genres(self):
        PublicEndpointsTestCase.test_get_genres(self)

    def test_get_actors(self):
        PublicEndpointsTestCase.test_get_actors(self)

    def test_get_movies(self):
        PublicEndpointsTestCase.test_get_movies(self)

    "PRIVATE endpoints"

    # Permission => view:genres
    def test_get_genres_detail(self):
        result = self.get('/api/genres-detail')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["genres"], list)

    # Permission => view:actors
    def test_get_actors_detail(self):
        result = self.get('/api/actors-detail')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["actors"], list)

    # Permission => view:movies
    def test_get_movies_detail(self):
        result = self.get('/api/movies-detail')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["movies"], list)

    def test_get_single_genre(self):
        genre = MovieGenre.query.first()
        result = self.get("api/genres/{}".format(genre.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance

    def test_get_single_actor(self):
        actor = Actor.query.first()
        result = self.get("api/actors/{}".format(actor.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertTrue(data["success"])

    def test_get_single_movie(self):
        movie = Movie.query.first()
        result = self.get("api/movies/{}".format(movie.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertTrue(data["success"])

if __name__ == "__main__":
    unittest.main()
