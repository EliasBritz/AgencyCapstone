import unittest
from unittest.mock import patch, MagicMock
import json

from app import create_app
from model import Movies, Actors

class CreateAppTestCase(unittest.TestCase):
    """This class represents the create_app test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the context so it's available in tests

    # Index Route
    def test_index_route(self):
        """Test index route"""
        res = self.client.get("/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Welcome to Casting Agency")
        
    def test_index_route_failure(self):
        """Test index route failure"""
        res = self.client.post("/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"], "Method not allowed")

    # Get Actors
    @patch('model.Actors.get_all_actors',
           MagicMock(return_value=[Actors(name="John Doe", age=27, gender="male"),
                                   Actors(name="Jane Doe", age=54, gender="female")]))
    def test_get_actors(self):
        """Test get actors route"""
        res = self.client.get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
    
    @patch('model.Actors.get_actor', MagicMock(return_value=Actors(name="John Doe", age=27, gender="male")))
    def test_get_actor(self):
        """Test get actor by id route"""
        actor_id = 1
        res = self.client.get(f"/actors/{actor_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    @patch('model.Actors.get_actor', MagicMock(return_value=None))
    def test_get_actor_failure(self):
        """Test get actor by id route failure"""
        actor_id = 100
        res = self.client.get(f"/actors/{actor_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # Get Movies
    @patch('model.Movies.get_all_movies',
           MagicMock(return_value=[Movies(title="Movie Title", release_date="2022-01-01"),
                                   Movies(title="Movie Title 2", release_date="2022-02-01")]))
    def test_get_movies(self):
        """Test get movies route"""
        res = self.client.get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    @patch('model.Movies.get_movie', MagicMock(return_value=Movies(title="Movie Title", release_date="2022-01-01")))
    def test_get_movie(self):
        """Test get movie by id route"""
        movie_id = 1
        res = self.client.get(f"/movies/{movie_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    @patch('model.Movies.get_movie', MagicMock(return_value=None))
    def test_get_movie_failure(self):
        """Test get movie by id route failure"""
        movie_id = 100
        res = self.client.get(f"/movies/{movie_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # Post Actor
    @patch('model.Actors.insert', MagicMock(return_value=None))
    def test_create_actor(self):
        """Test create actor route"""
        actor_data = {
            "name": "John Doe",
            "age": 30,
            "gender": "Male"
        }
        res = self.client.post("/actors", json=actor_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    @patch('model.Actors.insert', MagicMock(return_value=None))
    def test_create_actor_failure(self):
        """Test create actor route failure"""
        actor_data = {
            "name": "John Doe",
            "age": 30,
        }
        res = self.client.post("/actors", json=actor_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")
        
    # Post Movie
    @patch('model.Movies.insert', MagicMock(return_value=None))
    def test_create_movie(self):
        """Test create movie route"""
        movie_data = {
            "title": "Movie Title",
            "release_date": "2022-01-01"
        }
        res = self.client.post("/movies", json=movie_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
    
    @patch('model.Movies.insert', MagicMock(return_value=None))
    def test_create_movie_failure(self):
        """Test create movie route failure"""
        movie_data = {
            "title": "Movie Title"
        }
        res = self.client.post("/movies", json=movie_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    # Patch Actor
    @patch('model.Actors.get_actor', MagicMock(return_value=Actors(name="John Doe", age=27, gender="male")))
    @patch('model.Actors.update', MagicMock(return_value=None))
    def test_update_actor(self):
        """Test update actor route"""
        actor_id = 1
        actor_data = {
            "name": "Updated Name"
        }
        res = self.client.patch(f"/actors/{actor_id}", json=actor_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    @patch('model.Actors.get_actor', MagicMock(return_value=None))
    @patch('model.Actors.update', MagicMock(return_value=None))
    def test_update_actor_failure(self):
        """Test update actor route failure"""
        actor_id = 100
        actor_data = {
            "name": "Updated Name"
        }
        res = self.client.patch(f"/actors/{actor_id}", json=actor_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # Patch Movie
    @patch('model.Movies.get_movie', MagicMock(return_value=Movies(title="Movie Title", release_date="2022-01-01")))
    @patch('model.Movies.update', MagicMock(return_value=None))
    def test_update_movie(self):
        """Test update movie route"""
        movie_id = 1
        movie_data = {
            "title": "Updated Title"
        }
        res = self.client.patch(f"/movies/{movie_id}", json=movie_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    @patch('model.Movies.get_movie', MagicMock(return_value=None))
    @patch('model.Movies.update', MagicMock(return_value=None))
    def test_update_movie_failure(self):
        """Test update movie route failure"""
        movie_id = 100
        movie_data = {
            "title": "Updated Title"
        }
        res = self.client.patch(f"/movies/{movie_id}", json=movie_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # Delete Actor
    @patch('model.Actors.get_actor', MagicMock(return_value=Actors(name="John Doe", age=27, gender="male")))
    @patch('model.Actors.delete', MagicMock(return_value=None))
    def test_delete_actor(self):
        """Test delete actor route"""
        actor_id = 1
        res = self.client.delete(f"/actors/{actor_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], actor_id)

    @patch('model.Actors.get_actor', MagicMock(return_value=None))
    @patch('model.Actors.delete', MagicMock(return_value=None))
    def test_delete_actor_failure(self):
        """Test delete actor route failure"""
        actor_id = 100
        res = self.client.delete(f"/actors/{actor_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    # Delete Movie
    @patch('model.Movies.get_movie', MagicMock(return_value=Movies(title="Movie Title", release_date="2022-01-01")))
    @patch('model.Movies.delete', MagicMock(return_value=None))
    def test_delete_movie(self):
        """Test delete movie route"""
        movie_id = 1
        res = self.client.delete(f"/movies/{movie_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], movie_id)

    @patch('model.Movies.get_movie', MagicMock(return_value=None))
    @patch('model.Movies.delete', MagicMock(return_value=None))
    def test_delete_movie_failure(self):
        """Test delete movie route failure"""
        movie_id = 100
        res = self.client.delete(f"/movies/{movie_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    @patch('model.Actors.create_association', MagicMock(return_value=None))
    @patch('model.Actors.get_actor', MagicMock(return_value=Actors(name="John Dot", age=35, gender="male")))
    @patch('model.Movies.get_movie', MagicMock(return_value=Movies(title="Movie Title Shark", release_date="2022-01-01")))
    def test_add_movie_to_actor(self):
        """Test create association route"""
        request_data = {
            "actor_id": 1,
            "movie_id": 6
        }
        res = self.client.post("/associate", json=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor_id"])
        self.assertTrue(data["movie_id"])

if __name__ == "__main__":
    unittest.main()
