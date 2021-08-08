import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.api import create_app
from src.database.models import setup_db, Movie, MovieGenre, Actor


database_name = "casting_agency_test"
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "pysql21", "localhost:5432", database_name)


class TemplateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = database_name
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "pysql21", "localhost:5432", self.database_name)
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
            genre_name="1"
        )

        self.correct_movie = dict(
            title="Mucize Doktor",
            release_date="04/12/2019",
        )

        self.incorrect_movie = dict(
            title="",
            release_date="2121/221212/321323",
            actors_id=["02a", "212132132132"]
        )

        actor = Actor(
            name="Scarlett Johanson",
            age=35,
            gender="woman"
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

        self.update_genre = dict(
            genre_name="historical"
        )
        self.update_actor = dict(
            name="Taner Olmez",
            age=30,
            gender="man"
        )
        self.update_movie = {
            "title": "The Pursuit of Happyness",
            "release_date": "01/01/2006"
        }

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
        return self.client.delete(*args, **kwargs, headers={
            "Authorization": f"Bearer {self.jwt}"
        })


class PublicEndpointsTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt = ""

    " PUBLIC /endpoints "

    def test_get_genres(self):
        result = self.get("/genres")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_actors(self):
        result = self.get("/actors")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_movies(self):
        result = self.get("/movies")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])

    " PRIVATE /endpoints > test for 401(unauthorized) "

    " PERMISSION <view:genres> "

    def test_get_genres_detail_for_401(self):
        result = self.get("/genres-detail")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <view:actors> "

    def test_get_actors_detail_for_401(self):
        result = self.get("/actors-detail")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <view:movies> "

    def test_get_movies_detail_for_401(self):
        result = self.get("/movies-detail")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


    " PERMISSION <view:actors> "

    def test_get_actors_for_401(self):
        actor = Actor.query.all()[-1]
        result = self.get("/actors/" + str(actor.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <view:genres> "

    def test_get_genres_for_401(self):
        genre = MovieGenre.query.all()[-1]
        result = self.get("/genres/" + str(genre.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <view:movies> "

    def test_get_movies_for_401(self):
        movie = Movie.query.all()[-1]
        result = self.get("/movies/" + str(movie.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


    " PERMISSION <add:actors> "

    def test_add_actors_for_401(self):
        result = self.post("/actors", json=self.correct_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


    " PERMISSION <add:genres> "
    
    def test_add_genres_for_401(self):
        result = self.post("/genres", json=self.correct_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


    " PERMISSION <add:movies> "
    
    def test_add_movies_for_401(self):
        result = self.post("/movies", json=self.correct_movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


    " PERMISSION <update:actors> "

    def test_update_actors_for_401(self):
        actor = Actor.query.all()[-1]
        result = self.patch("/actors/" + str(actor.id), json=self.update_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <update:genres> "

    def test_update_genres_for_401(self):
        genre = MovieGenre.query.all()[-1]
        result = self.patch("/genres/" + str(genre.id), json=self.update_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <update:movies> "

    def test_update_movies_for_401(self):
        movie = Movie.query.all()[-1]
        result = self.patch("/movies/" + str(movie.id), json=self.update_movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


    " PERMISSION <delete:actors> "

    def test_delete_actors_for_401(self):
        actor = Actor.query.all()[-1]
        result = self.delete("/actors/" + str(actor.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <delete:genres> "

    def test_delete_genres_for_401(self):
        genre = MovieGenre.query.all()[-1]
        result = self.delete("/genres/" + str(genre.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])

    " PERMISSION <delete:movies> "

    def test_delete_movies_for_401(self):
        movie = Movie.query.all()[-1]
        result = self.delete("/movies/" + str(movie.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertFalse(data["success"])


class CAAssitantTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJtUUdqVXlNMXRyYVRhU3pIQXpqWiJ9.eyJpc3MiOiJodHRwczovL2F1dGgwLXNlcnZpY2UudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmZjMjFlMjQ1NGYyMDA2YTIzOTNlMyIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjI4NDM2MDMyLCJleHAiOjE2Mjg0NDMyMzIsImF6cCI6ImtIamVFV2pla0ZrNWtlN3NGVTBsTHp2Q3NXRmFHQUtZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6Z2VucmVzIiwidmlldzptb3ZpZXMiXX0.KDKfNZOFiiRGc69T7bAjdbX89acBk4Qu-izSsD_6ymOr9LNu7REEPDSlzrYdtYCDTTaK_0e5hRRmDLupgeNHbROKkmp640PHauG8IpbCMWfrhMWqusl8TC-A45gEEzQq4VjkuIiV9ufEsUpInBOLGXZz4Hm6Abonp5qNAMKotXTIB6tq_Apkzx6B4wEEFIwGzNSACR4XUS7Y-95grCjgp9_ipA_dRpdYo0E6iM78I1-e5S38HmP3Z3nx8N6WoBE4jGX2I0apBOHvk-rNCFniNt6M-i8R-F7tTNvTXR5Bi48fbpDZbhQgt7SmI-0Mmx9nlN46n7cfW3Ufbyfrqf2tLg"

    " PUBLIC /endpoints "
    def test_get_genres(self):
        PublicEndpointsTestCase.test_get_genres(self)


    def test_get_actors(self):
        PublicEndpointsTestCase.test_get_actors(self)

    def test_get_movies(self):
        PublicEndpointsTestCase.test_get_movies(self)

    " PRIVATE /endpoints "

    " PERMISSION <view:genres> "

    def test_get_genres_detail(self):
        result = self.get("/genres-detail")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["genres"], list)

    " PERMISSION <view:actors> "

    def test_get_actors_detail(self):
        result = self.get("/actors-detail")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["actors"], list)

    " PERMISSION <view:movies> "

    def test_get_movies_detail(self):
        result = self.get("/movies-detail")
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["movies"], list)

    " PERMISSION <view:genres> "

    def test_get_single_genre_detail(self):
        genre = MovieGenre.query.first()
        result = self.get("/genres/" + str(genre.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["genre"], dict)
        self.assertEqual(data["genre"]["id"], genre.id)
        self.assertEqual(data["genre"]["genre_name"], genre.genre_name)

    def test_get_single_genre_detail_for_404(self):
        genre_id = "12211212"
        result = self.get("/genres/" + genre_id)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " PERMISSION <view:actors> "

    def test_get_single_actor_detail(self):
        actor = Actor.query.first()
        result = self.get("/actors/" + str(actor.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["actor"], dict)
        self.assertEqual(data["actor"]["id"], actor.id)
        self.assertEqual(data["actor"]["name"], actor.name)

    def test_get_single_actor_detail_for_404(self):
        actor_id = "1892883"
        result = self.get("/actor/" + actor_id)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " PERMISSION <view:movies> "

    def test_get_single_movie_detail(self):
        movie = Movie.query.first()
        result = self.get("/movies/" + str(movie.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsInstance(data["movie"], dict)
        self.assertEqual(data["movie"]["id"], movie.id)
        self.assertEqual(data["movie"]["title"], movie.title)

    def test_get_single_movie_detail_for_404(self):
        movie_id = "18928831234345"
        result = self.get("/actor/" + movie_id)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " Fobidden: Access Denied - 403 "

    " PERMISSION <add:genres> "

    def test_post_genres_for_403(self):
        result = self.post("/genres", json=self.correct_genre)
        self.access_denied(result)

    " PERMISSION <add:actors> "

    def test_post_actors_for_403(self):
        result = self.post("/actors", json=self.correct_actor)
        self.access_denied(result)

    " PERMISSION <add:movies> "

    def test_post_movies_for_403(self):
        result = self.post("/movies", json=self.correct_movie)
        self.access_denied(result)

    " PERMISSION <update:genres> "
    def test_update_genre_for_403(self):
        genre = MovieGenre.query.all()[-1]
        result = self.patch("/genres/" + str(genre.id), json=self.update_genre)
        self.access_denied(result)

    " PERMISSION <update:actors> "
    def test_update_actor_for_403(self):
        actor = Actor.query.first()
        result = self.patch("/actors/"+ str(actor.id), json=self.update_actor)
        self.access_denied(result)


    " PERMISSION <update:movies> "
    def test_update_movies_for_403(self):
        movie = Movie.query.first()
        result = self.patch("/movies/" + str(movie.id), json=self.update_movie)
        self.access_denied(result)


    " PERMISSION <delete:genres> "
    def test_delete_genres_for_403(self):
        genre = MovieGenre.query.all()[-1]
        result = self.delete("/genres/" + str(genre.id))
        self.access_denied(result)

    " PERMISSION <delete:actors> "
    def test_delete_actors_for_403(self):
        actor = Actor.query.all()[-1]
        result = self.delete("/actors/"+ str(actor.id))
        self.access_denied(result)


    " PERMISSION <delete:movies> "
    def test_delete_movies_for_403(self):
        movie = Movie.query.all()[-1]
        result = self.delete("/movies/" + str(movie.id))
        self.access_denied(result)

class CADirectorTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJtUUdqVXlNMXRyYVRhU3pIQXpqWiJ9.eyJpc3MiOiJodHRwczovL2F1dGgwLXNlcnZpY2UudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmZjMWU1ZTE2YjkxMDA2YWQzOTA4NCIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjI4NDM1OTEyLCJleHAiOjE2Mjg0NDMxMTIsImF6cCI6ImtIamVFV2pla0ZrNWtlN3NGVTBsTHp2Q3NXRmFHQUtZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6Z2VucmVzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzpnZW5yZXMiLCJ2aWV3Om1vdmllcyJdfQ.ZS6J_t4TO2r5hF2v1mnxurk3EhTnM3tDJjYh6stq-dDYolkeA8iu5LFZhCMALzF8JkhTjZRJ5GZuU-W7_lj-ljryWkTp8mC-5MI-5kqZbskF3e5frBkAcny0hdc2fRakkPh9hs3vu8kCqd3d5hhDCArd6sQe49IKyZ-NLGCjKmvvCXYfJ_aXopCqpAizGJTWmwKNTFUiNh5MiCBfrmHHWToGt-pIGCpvV-gzB_8FE8jOt9_PX208HcW2FfOYW36-3iA9c-T1GceZaybUiWXzHvBWjVHQak1dPsCTRFtg32efs4nvGqseLwDq2DXRvWe-ehDEgM45EPOTsjtl-fvw1g"

    " PUBLIC /endpoints "
    def test_get_genres(self):
        PublicEndpointsTestCase.test_get_genres(self)

    def test_get_actors(self):
        PublicEndpointsTestCase.test_get_actors(self)

    def test_get_movies(self):
        PublicEndpointsTestCase.test_get_movies(self)

    " PRIVATE /endpoints "

    " PERMISSION <view:genres> "

    def test_get_genres_detail(self):
        CAAssitantTestCase.test_get_genres_detail(self)

    " PERMISSION <view:actors> "

    def test_get_actors_detail(self):
        CAAssitantTestCase.test_get_actors_detail(self)

    " PERMISSION <view:movies> "

    def test_get_movies_detail(self):
        CAAssitantTestCase.test_get_movies_detail(self)

    " PERMISSION <view:genres> "

    def test_get_single_genre_detail(self):
        CAAssitantTestCase.test_get_single_genre_detail(self)

    def test_get_single_genre_detail_for_404(self):
        CAAssitantTestCase.test_get_single_genre_detail_for_404(self)   

    " PERMISSION <view:actors> "

    def test_get_single_actor_detail(self):
       CAAssitantTestCase.test_get_single_actor_detail(self)

    def test_get_single_actor_detail_for_404(self):
        CAAssitantTestCase.test_get_single_actor_detail_for_404(self)

    " PERMISSION <view:movies> "

    def test_get_single_movie_detail(self):
        CAAssitantTestCase.test_get_single_movie_detail(self)

    def test_get_single_movie_detail_for_404(self):
        CAAssitantTestCase.test_get_single_movie_detail_for_404(self)

    " PERMISSION <add:actors> "

    def test_add_actors(self):
        result = self.post("/actors", json=self.correct_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(data["actor"], dict)
        self.assertTrue(data["success"])

    " 400 - Bad request "

    def test_add_actors_for_400(self):
        result = self.post("/actors", json=self.incorrect_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"])

    " Fobidden: Access Denied - 403 "
    
    " PERMISSION <add:genres> "
    
    def test_post_genres_for_403(self):
        CAAssitantTestCase.test_post_genres_for_403(self)
    
    " PERMISSION <add:movies> "
    
    def test_post_movies_for_403(self):
        CAAssitantTestCase.test_post_movies_for_403(self)

    " PERMISSION <update:actors> "

    def test_update_actors(self):
        actor = Actor.query.all()[0]
        result = self.patch("/actors/" + str(actor.id), json=self.update_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["updated"])
        self.assertIsInstance(data["actor"], dict)
        self.assertEqual(data["actor"]["id"], actor.id)
        self.assertTrue(data["success"])

    " 400 - Bad request "

    def test_update_actors_for_400(self):
        actor = Actor.query.all()[0]
        result = self.patch("/actors/" + str(actor.id), json=self.incorrect_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"])

    " 404 - Not found "    

    def test_update_actors_for_404(self):
        actor = "28989231980021"
        result = self.patch("/actors/" + actor, json=self.update_actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " PERMISSION <update:genres> "

    def test_update_genres(self):
        genre = MovieGenre.query.all()[0]
        result = self.patch("/genres/" + str(genre.id), json=self.update_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["updated"])
        self.assertIsInstance(data["genre"], dict)
        self.assertEqual(data["genre"]["id"], genre.id)
        self.assertTrue(data["success"])

    " 400 - Bad request "

    def test_update_genres_for_400(self):
        genre = MovieGenre.query.all()[0]
        result = self.patch("/genres/" + str(genre.id), json=self.incorrect_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"])

    " 404 - Not found "

    def test_update_genres_for_404(self):
        genre = "239878912389"
        result = self.patch("/genres/" + genre, json=self.update_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " PERMISSION <update:movies> "

    def test_update_movies(self):
        movie = Movie.query.all()[0]
        result = self.patch("/movies/" + str(movie.id), json=self.update_movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data["updated"])
        self.assertIsInstance(data["movie"], dict)
        self.assertEqual(data["movie"]["id"], movie.id)
        self.assertTrue(data["success"])

    " 400 - Bad request "

    def test_update_movies_for_400(self):
        movie = Movie.query.all()[0]
        result = self.patch("/movies/" + str(movie.id), json=self.incorrect_movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"])

    " 404 - Not found "

    def test_update_movies_for_404(self):
        movie = "1212089089123089"
        result = self.patch("/movies/" + str(movie), json=self.update_movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " PERMISSION <delete:actors> "

    def test_delete_actors(self):
        actor = Actor.query.all()[-1]
        result = self.delete("/actors/" + str(actor.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["deleted_id"], actor.id)
        self.assertTrue(data["success"])

    " 404 - Not found "

    def test_delete_actors_for_404(self):
        actor = "123009890823890"
        result = self.delete("/actors/" + actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])


    " Fobidden: Access Denied - 403 "

    " PERMISSION <delete:genres> "

    def test_delete_genres_for_403(self):
        CAAssitantTestCase.test_delete_genres_for_403(self)

    " PERMISSION <delete:movies> "

    def test_delete_movies_for_403(self):
        CAAssitantTestCase.test_delete_movies_for_403(self)    


class CAPoducerTestCase(TemplateTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJtUUdqVXlNMXRyYVRhU3pIQXpqWiJ9.eyJpc3MiOiJodHRwczovL2F1dGgwLXNlcnZpY2UudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZmZjMTNhMzU4MmJjMDA2OTQ2NjQzNiIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjI4NDM2MDkzLCJleHAiOjE2Mjg0NDMyOTMsImF6cCI6ImtIamVFV2pla0ZrNWtlN3NGVTBsTHp2Q3NXRmFHQUtZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiYWRkOmdlbnJlcyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOmdlbnJlcyIsImRlbGV0ZTptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOmdlbnJlcyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6Z2VucmVzIiwidmlldzptb3ZpZXMiXX0.WBR480L6xPypvz73mjtSwsJ88ya2YAWAcDFTmSTL3KcYPjRwqrhujDLQyoiZG30uFe6myx8CUqMrYwli2TnhAgiwuaE5CXtzwl1_xUz6CoFAqYGDmXsRu4Gop0p97149fSrwpkG8QmiT6j0EAqFX2Sen4MQlA1emtG8CTtyOGGdlApjj_Cox2_2YRR0dd63ddxmm8SO8DkPs_T0jvlfUneoZz7ZHVQDGIWiQPNE0DnMmrtrYF-zAg4iPKkaL8dY4lePOSw2LhWaGu6E7NtnUzjecVpYHWZMZ7t65GwdHjsuZZFPwX0ausUQKhFa1Qjge15lx-qP8qunjezJ60lPVcg"

    " PUBLIC /endpoints "
    def test_get_genres(self):
        PublicEndpointsTestCase.test_get_genres(self)


    def test_get_actors(self):
        PublicEndpointsTestCase.test_get_actors(self)

    def test_get_movies(self):
        PublicEndpointsTestCase.test_get_movies(self)

    " PRIVATE /endpoints "

    " PERMISSION <view:genres> "

    def test_get_genres_detail(self):
        CAAssitantTestCase.test_get_genres_detail(self)

    " PERMISSION <view:actors> "

    def test_get_actors_detail(self):
        CAAssitantTestCase.test_get_actors_detail(self)

    " PERMISSION <view:movies> "

    def test_get_movies_detail(self):
        CAAssitantTestCase.test_get_movies_detail(self)

    " PERMISSION <view:genres> "

    def test_get_single_genre_detail(self):
        CAAssitantTestCase.test_get_single_genre_detail(self)

    def test_get_single_genre_detail_for_404(self):
        CAAssitantTestCase.test_get_single_genre_detail_for_404(self)   

    " PERMISSION <view:actors> "

    def test_get_single_actor_detail(self):
       CAAssitantTestCase.test_get_single_actor_detail(self)

    def test_get_single_actor_detail_for_404(self):
        CAAssitantTestCase.test_get_single_actor_detail_for_404(self)

    " PERMISSION <view:movies> "

    def test_get_single_movie_detail(self):
        CAAssitantTestCase.test_get_single_movie_detail(self)

    def test_get_single_movie_detail_for_404(self):
        CAAssitantTestCase.test_get_single_movie_detail_for_404(self)

    " PERMISSION <add:actors> "       
    def test_add_actors(self):
        CADirectorTestCase.test_add_actors(self)

    " 400 - bad request "

    def test_add_actors_for_400(self):
        CADirectorTestCase.test_add_actors_for_400(self)

    " PERMISSION <add:genres> "

    def test_add_genres(self):
        result = self.post("/genres", json=self.correct_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(data["genre"], dict)
        self.assertTrue(data["success"]) 

    " 400 - Bad request "

    def test_add_genres_for_400(self):
        result = self.post("/genres", json=self.incorrect_genre)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"]) 

    " PERMISSION <add:movies> "
    
    def test_add_movies(self):
        actor = Actor.query.first()
        genre = MovieGenre.query.first()
        movie = dict(
            title="Mucize Doktor",
            release_date="02/12/2019",
            actors_id=[actor.id],
            genres_id=[genre.id]
        )
        result = self.post("/movies", json=movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIsInstance(data["movie"], dict)
        self.assertTrue(data["success"]) 

    " 400 - Bad request "

    def test_add_movies_for_400(self):
        result = self.post("/movies", json=self.incorrect_movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data["success"]) 

    " PERMISSION <update:actors> "

    def test_update_actors(self):
        CADirectorTestCase.test_update_actors(self)

    " 400 - Bad request "

    def test_update_actors_for_400(self):
        CADirectorTestCase.test_update_actors_for_400(self)

    " 404 - Not found "

    def test_update_actors_for_404(self):
        CADirectorTestCase.test_update_actors_for_404(self)

    " PERMISSION <update:genres> "
    
    def test_update_genres(self):
        CADirectorTestCase.test_update_genres(self)

    " 400 - Bad request "

    def test_update_genres_for_400(self):
        CADirectorTestCase.test_update_genres_for_400(self)

    " 404 - Not found "

    def test_update_genres_for_404(self):
        CADirectorTestCase.test_update_genres_for_404(self)

    " PERMISSION <update:movies> "

    def test_update_movies(self):
        CADirectorTestCase.test_update_movies(self)      

    " 400 - Bad request "  
    
    def test_update_movies_for_400(self):
        CADirectorTestCase.test_update_movies_for_400(self)
    
    " 404 - Not found "  

    def test_update_movies_for_404(self):
        CADirectorTestCase.test_update_movies_for_404(self)

    " PERMISSION <delete:actors> "

    def test_delete_actors(self):
        CADirectorTestCase.test_delete_actors(self)

    " 404 - Not found "

    def test_delete_actors_for_404(self):
        CADirectorTestCase.test_delete_actors_for_404(self)

    " PERMISSION <delete:genres> "

    def test_delete_genres(self):
        genre = MovieGenre.query.all()[-1]
        result = self.delete("/genres/" + str(genre.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["deleted_id"], genre.id)
        self.assertTrue(data["success"])

    " 404 - Not found "

    def test_delete_genres_for_404(self):
        genre = "2123321321213213231231"
        result = self.delete("/genres/" + str(genre))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

    " PERMISSION <delete:movies> "

    def test_delete_movies(self):
        movie = Movie.query.all()[-1]
        result = self.delete("/movies/" + str(movie.id))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["deleted_id"], movie.id)
        self.assertTrue(data["success"])

    " 404 - Not found "

    def test_delete_movies_for_404(self):
        movie = "12098120981298"
        result = self.delete("/movies/" + str(movie))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data["success"])

if __name__ == "__main__":
    unittest.main()
