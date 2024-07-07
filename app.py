from flask import Flask, abort, jsonify, request
from flask_migrate import Migrate

from flask_cors import CORS
from auth import requires_auth, AuthError
from model import Actors, Movies, setup_db, db

def create_app(test_config=False):
    """Create and configure an instance of the Flask application."""
    # Create and Configure
    app = Flask(__name__)

    setup_db(app)

    migrate = Migrate(app, db)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Welcome to Casting Agency'
        })
        
    ## ROUTES GET /actors and /movies
    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors', Test_config=test_config)
    def get_actors(payload):
        actors = Actors.get_all_actors()
        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies', Test_config=test_config)
    def get_movies(payload):
        movies = Movies.get_all_movies()
        formatted_movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        })
    
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth(permission='get:actors', Test_config=test_config)
    def get_actor(payload, actor_id):
        actor = Actors.get_actor(actor_id)
        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth(permission='get:movies', Test_config=test_config)
    def get_movie(payload, movie_id):
        movie = Movies.get_movie(movie_id)
        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    
    ## ROUTES POST /actors and /movies
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors', Test_config=test_config)
    def create_actor(payload):
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name is None or age is None or gender is None:
            abort(400)
        try:
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies', Test_config=test_config)
    def create_movie(payload):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')

        if title is None or release_date is None:
            abort(400)
        try:
            movie = Movies(title=title, release_date=release_date)
            movie.insert()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    
    ## ROUTES PATCH /actors and /movies
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors', Test_config=test_config)
    def update_actor(payload, actor_id):
        actor = Actors.get_actor(actor_id)
        if actor is None:
            abort(404)
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name is not None:
            actor.name = name
        if age is not None:
            actor.age = age
        if gender is not None:
            actor.gender = gender
        try:
            actor.update()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies', Test_config=test_config)
    def update_movie(payload, movie_id):
        movie = Movies.get_movie(movie_id)
        if movie is None:
            abort(404)
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')

        if title is not None:
            movie.title = title
        if release_date is not None:
            movie.release_date = release_date
        try:
            movie.update()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    
    ## ROUTES DELETE /actors and /movies
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors', Test_config=test_config)
    def delete_actor(payload, actor_id):
        actor = Actors.get_actor(actor_id)
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'delete': actor_id
        })
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies', Test_config=test_config)
    def delete_movie(payload, movie_id):
        movie = Movies.get_movie(movie_id)
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except:
            abort(422)
        return jsonify({
            'success': True,
            'delete': movie_id
        })
    
    ## Associations
    @app.route('/associate', methods=['POST'])
    @requires_auth(permission='post:movies', Test_config=test_config)
    def add_movie_to_actor(payload):
        """
        Add a movie to an actor. But will also work for adding an actor to a movie.
        """
        data = request.get_json()
        actor_id = data.get('actor_id')
        movie_id = data.get('movie_id')

        actor = Actors.get_actor(actor_id)
        movie = Movies.get_movie(movie_id)
        if actor and movie:
            actor.create_association(movie)
            return jsonify({
                'success': True,
                'actor_id': actor_id,
                'movie_id': movie_id
            }), 200
        else:
            abort(404)

    ## Error Handling
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405
    
    return app

app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run('localhost', port=8080)