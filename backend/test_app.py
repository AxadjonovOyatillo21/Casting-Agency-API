import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.api import create_app
from src.database.models import setup_db, Movie, MovieGenre, Actor


database_name = "casting_agency_test"
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "pysql", "localhost:5432", database_name)


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = database_name
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "pysql", "localhost:5432", self.database_name)
        self.db = setup_db(self.app, self.database_path)
        self.db.drop_all()
        self.db.create_all()

        self.correct_actor = dict(
            name="Simple Actor",
            age=35,
            gender="man"
        )

        self.incorrect_actor = dict(
            name="",
            age="2a",
            gender="this is an alien😂"
        )

        self.correct_genre = dict(
            genre_name="adventure"
        )

        self.incorrect_genre = dict(
            genre_name=""
        )

        self.correct_movie = dict(
            title="Mucize Doktor",
            release_date="04/12/2019",
            actors_id=["0", "1"],
            genres_id=["0"]
        )

        self.incorrect_movie = dict(
            title="",
            release_date="2121/221212/321323",
            actors_id=["02a", "212132132132"]
        )

        actor = Actor(
            name="Taner Olmez",
            age=30,
            gender="man"
        )
        actor.insert()

        actor_2 = Actor(
            name="Sinem Unsal",
            age=29,
            gender="woman"
        )
        actor_2.insert()

        genre = MovieGenre(genre_name="science-fiction")
        genre.insert()

        movie = Movie(
            title="Lucy",
            release_date="04/12/2014"
        )
        movie.insert()

    def tearDown(self):
        " Executed after all tests "
        pass

    def access_denied(self, result):
        data=  json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertFalse(data["success"])

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })

    def post(self, *args, **kwargs):
        return self.client.post(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })

    def patch(self, *args, **kwargs):
        return self.client.patch(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })

    def delete(self, *args, **kwargs):
        return self.client.get(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })


# class PublicEndpointsTestCase(TemplateTestCase):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.jwt = ""

#     " PUBLIC /endpoints "

#     def test_get_genres(self):
#         result = self.get("/api/genres")
#         data = json.loads(result.data)
#         self.assertEqual(result.status_code, 200)
#         self.assertTrue(data["success"])

#     def test_get_actors(self):
#         result = self.get("/api/actors")
#         data = json.loads(result.data)
#         self.assertEqual(result.status_code, 200)
#         self.assertTrue(data["success"])

#     def test_get_movies(self):
#         result = self.get("/api/movies")
#         data = json.loads(result.data)
#         self.assertEqual(result.status_code, 200)
#         self.assertTrue(data["success"])

#     " PRIVATE /endpoints > test for 401(unauthorized) "

#     " PERMISSION <view:genres> "

#     def test_get_genres_detail_for_401(self):
#         result = self.get("/api/genres-detail")
#         data = json.loads(result.data)
#         self.assertEqual(result.status_code, 401)
#         self.assertFalse(data["success"])

#     " PERMISSION <view:actors> "

#     def test_get_actors_detail_for_401(self):
#         result = self.get("/api/actors-detail")
#         data = json.loads(result.data)
#         self.assertEqual(result.status_code, 401)
#         self.assertFalse(data["success"])

#     " PERMISSION <view:movies> "

#     def test_get_movies_detail_for_401(self):
#         result = self.get("/api/movies-detail")
#         data = json.loads(result.data)
#         self.assertEqual(result.status_code, 401)
#         self.assertFalse(data["success"])


class CAAssitantTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJtUUdqVXlNMXRyYVRhU3pIQXpqWiJ9.eyJpc3MiOiJodHRwczovL2F1dGgwLXNlcnZpY2UudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmZjMjFlMjQ1NGYyMDA2YTIzOTNlMyIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjI3ODg2MDE0LCJleHAiOjE2Mjc4OTMyMTQsImF6cCI6ImtIamVFV2pla0ZrNWtlN3NGVTBsTHp2Q3NXRmFHQUtZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6Z2VucmVzIiwidmlldzptb3ZpZXMiXX0.oUa9IAS_Gr8cu5j74Zp8IxQEJjTFYbenKUGC7lKE8jZZwONp1nlnYiO1JIOyrnBu4eziWk2Um87WMeXHTlHyHNteC8TpL-4JHqg-_UEynJBG0bjOE_WML9ZP99FXizpUpIkZQKNiXpbLYMgjOApV1XuZfat1Q2HFyl4xCCvEDVHI8jEsyvnhWf2VVYZB93y76tAkl6ZTlTHFVPPMN-_mndz9Sqysff71KVIY2fRZIPpWKpU-Aebj7N2Nv2mjv3ASmAPaF4F3mhnVYVp4gvZykZi9htg3WwFh306ejAIdKfJJuTslVMvkVXvfTn_yUlzR0nzzeF7aDCbj2kN_NWbgww"

    def test_get(self):
        result = self.client.get("/api")
        print(result)

    # " PUBLIC /endpoints "
    # def test_get_genres(self):
    #     PublicEndpointsTestCase.test_get_genres(self)


    # def test_get_actors(self):
    #     PublicEndpointsTestCase.test_get_actors(self)

    # def test_get_movies(self):
    #     PublicEndpointsTestCase.test_get_movies(self)

    # " PRIVATE /endpoints "

    # " PERMISSION <view:genres> "

    # def test_get_genres_detail(self):
    #     result = self.get("/api/genres-detail")
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIsInstance(data["genres"], list)

    # " PERMISSION <view:actors> "

    # def test_get_actors_detail(self):
    #     result = self.get("/api/actors-detail")
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIsInstance(data["actors"], list)

    # " PERMISSION <view:movies> "

    # def test_get_movies_detail(self):
    #     result = self.get("/api/movies-detail")
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIsInstance(data["movies"], list)

    # " PERMISSION <view:genres> "

    # def test_get_single_genre_detail(self):
    #     genre = MovieGenre.query.first()
    #     result = self.get("/api/genres/" + str(genre.id))
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIsInstance(data["genre"], dict)
    #     self.assertEqual(data["genre"]["id"], genre.id)
    #     self.assertEqual(data["genre"]["genre_name"], genre.genre_name)

    # def test_get_single_genre_detail_for_404(self):
    #     genre_id = "12211212"
    #     result = self.get("/api/genres" + genre_id)
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 404)
    #     self.assertFalse(data["success"])

    # " PERMISSION <view:actors> "

    # def test_get_single_actor_detail(self):
    #     actor = Actor.query.first()
    #     result = self.get("/api/actors/" + str(actor.id))
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIsInstance(data["actor"], dict)
    #     self.assertEqual(data["actor"]["id"], actor.id)
    #     self.assertEqual(data["actor"]["name"], actor.name)

    # def test_get_single_actor_detail_for_404(self):
    #     actor_id = "1892883"
    #     result = self.get("/api/actor" + actor_id)
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 404)
    #     self.assertFalse(data["success"])

    # " PERMISSION <view:genres> "

    # def test_get_single_movie_detail(self):
    #     movie = Movie.query.first()
    #     result = self.get("/api/movies/" + str(movie.id))
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIsInstance(data["movie"], dict)
    #     self.assertEqual(data["movie"]["id"], movie.id)
    #     self.assertEqual(data["movie"]["title"], movie.title)

    # def test_get_single_movie_detail_for_404(self):
    #     movie_id = "18928831234345"
    #     result = self.get("/api/actor" + movie_id)
    #     data = json.loads(result.data)
    #     self.assertEqual(result.status_code, 404)
    #     self.assertFalse(data["success"])



if __name__ == "__main__":
    unittest.main()
