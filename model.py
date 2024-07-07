from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_PATH

db = SQLAlchemy()

def setup_db(app):
    """binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

class Movies(db.Model):
    """Movies Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship('Actors', secondary='movie_actors', back_populates='movies', lazy=True)

    # Functions for extra Layer of abstraction. More scalable
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def get_movie(movie_id: int):
        return db.session.get(Movies, movie_id)
    
    def get_all_movies():
        return db.session.query(Movies).all()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]
        }
    
class Actors(db.Model):
    """Actors Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    movies = db.relationship('Movies', secondary='movie_actors', back_populates='actors', lazy=True)

    # Functions for extra Layer of abstraction. More scalable
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def get_actor(actor_id: int):
        return db.session.get(Actors, actor_id)
    
    def get_all_actors():
        return db.session.query(Actors).all()
    
    def create_association(self, movie):
        self.movies.append(movie)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.title for movie in self.movies]
        }

# Define the secondary table
movie_actors = db.Table('movie_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)