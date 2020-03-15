import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models.models import setup_db, Actors, Movies


class CapStoneTestCase(unittest.TestCase):
    """This class represents the CAPSTONE test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('CAPSTONE_TEST_DB')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor(self):
        new_actor = {
            'name': 'Mark',
            'age': '18',
            'gender': 'male'
        }
        res = self.client().post('/actors', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_400_no_body(self):

        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_create_actor_400_missing_fields(self):
        new_actor = {
            'name': 'Salem',
            'age': '18'
        }
        res = self.client().post('/actors', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_delete_actor(self):
        actor = Actors.query.all()[-1]
        res = self.client().delete(f'/actors/{actor.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['Deleted Actor'], actor.id)

    def test_delete_actor_404_no_match_actor(self):
        actor_id = 10000

        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_actor(self):
        actor_id = 2
        updated_actor = {
            'age': '22'
        }

        res = self.client().patch(f'/actors/{actor_id}', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor_404_no_match_actor(self):
        actor_id = 2673348
        updated_actor = {
            'name': 'Omar'
        }

        res = self.client().patch(f'/actors/{actor_id}', json=updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_actor_400_no_body(self):
        actor_id = 1

        res = self.client().patch(f'/actors/{actor_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_get_movies(self):

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie(self):
        new_movie = {
            'title': 'TestMovie',
            'release_date': '2020-03-10 15:30:00'
        }
        res = self.client().post('/movies', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_400_no_body(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_create_movie_400_missing_fields(self):
        new_actor = {
            'title': 'Mark101'
        }
        res = self.client().post('/movies', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_delete_movie(self):
        movie = Movies.query.all()[-1]
        res = self.client().delete(f'/movies/{movie.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['Deleted Movie'], movie.id)

    def test_delete_movie_404_no_match_movie(self):
        movie_id = 10000

        res = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_movie(self):
        movie_id = 2
        updated_movie = {
            'release_date': '2020-04-01 17:00:00'
        }

        res = self.client().patch(f'/movies/{movie_id}', json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie_404_no_match_movie(self):
        movie_id = 2673348
        updated_movie = {
            'title': 'Mark101'
        }

        res = self.client().patch(f'/movies/{movie_id}', json=updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_movie_400_no_body(self):
        movie_id = 1

        res = self.client().patch(f'/movies/{movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


if __name__ == "__main__":
    unittest.main()
