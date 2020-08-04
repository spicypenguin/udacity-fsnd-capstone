
from flask_sqlalchemy import SQLAlchemy
from helpers.dates import years_since_date

from os import getenv
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def setup_db(app, db_name=None):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db_user = getenv('DATABASE_USER')
    db_pwd = getenv('DATABASE_PWD')
    db_host = getenv('DATABASE_HOST')
    db_port = getenv('DATABASE_PORT')
    if not db_name:
        db_name = getenv('DATABASE_USER')

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
    db.app = app
    db.init_app(app)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.String)
    gender = db.Column(db.String(10))

    movies = db.relationship('Movie', secondary='roles')

    def __repr__(self):
        return f'<Actor {self.id} - {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'age': years_since_date(self.date_of_birth),
            'gender': self.gender,
            'movies': [m.format_self() for m in self.movies]
        }

    def format_self(self):
        return {
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'age': years_since_date(self.date_of_birth),
            'gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.String)

    actors = db.relationship('Actor', secondary='roles')

    def __repr__(self):
        return f'<Movie {self.id} - {self.title}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [a.format_self() for a in self.actors]
        }

    def format_self(self):
        return {
            'title': self.title,
            'release_date': self.release_date,
        }


class Role(db.Model):
    __tablename__ = 'roles'

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey('actors.id'),
        primary_key=True
    )
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'),
        primary_key=True
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
