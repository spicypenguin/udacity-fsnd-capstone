from dotenv import load_dotenv
from os import getenv

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, setup_db, Actor, Movie, Role
from helpers.dates import convert_date_to_dateobj
from auth.auth import requires_auth


load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    migrate = Migrate(app, db)

    return app


APP = create_app()


########
# Actor endpoints
# /actors
########

@APP.route('/actors')
@requires_auth('read:actors')
def get_actors():
    """Return a list of all actors"""

    return jsonify({
        'success': True,
        'actors': [a.format() for a in Actor.query.all()]
    })


@APP.route('/actors', methods=['POST'])
@requires_auth('create:actors')
def create_actor():
    """Add a new actor to the database

    Payload parameters:
    name -- the name of the actor (required)
    date_of_birth -- the date of birth of the actor in YYYY-MM-DD format (optional)
    gender -- the gender of the actor (optional)

    Returns an object, with the newly persisted actor if successful.
    """

    data = request.get_json()
    if not data or not data.get('name'):
        abort(400, description='`name` attribute must be specified')

    if data.get('date_of_birth') and convert_date_to_dateobj(data['date_of_birth']) == None:
        abort(400, description="`date_of_birth` must be in format YYYY-MM-DD")

    actor = Actor(name=data['name'])

    if data.get('date_of_birth'):
        actor.date_of_birth = data['date_of_birth']

    if data.get('gender'):
        actor.gender = data['gender']

    actor.insert()

    return jsonify({
        'success': True,
        'actor': actor.format()
    })


@APP.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('update:actors')
def update_actor(actor_id):
    """Updates an existing actor's information in the database

    Payload parameters:
    name -- the name of the actor (optional)
    date_of_birth -- the date of birth of the actor in YYYY-MM-DD format (optional)
    gender -- the gender of the actor (optional)

    At least one of the parameters above must be specified, or the call will fail with a 400 error.
    Returns an object, with the updated actor metadata if successful.
    """

    data = request.get_json()
    if not data or not (data.get('name') or data.get('date_of_birth') or data.get('gender')):
        abort(400, description='At least one of `name`, `date_of_birth`, or `gender` must be provided.')

    if data.get('date_of_birth') and convert_date_to_dateobj(data['date_of_birth']) == None:
        abort(400, description="`date_of_birth` must be in format YYYY-MM-DD")

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(
            404, description=f'Actor with actor_id {actor_id} was not found.')

    if data.get('name'):
        actor.name = data['name']

    if data.get('date_of_birth'):
        actor.date_of_birth = data['date_of_birth']

    if data.get('gender'):
        actor.gender = data['gender']

    actor.update()

    return jsonify({
        'success': True,
        'actor': actor.format()
    })


@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(actor_id):
    """Deletes an existing actor from the database

    Returns an object, with the actor_id that was removed if successful.
    """

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(
            404, description=f'Actor with actor_id {actor_id} was not found.')

    actor.delete()

    return jsonify({
        'success': True,
        'actor_id': actor_id
    })


########
# Movie endpoints
# /movies
########

@APP.route('/movies')
@requires_auth('read:movies')
def get_movies():
    """Return a list of all movies"""

    return jsonify({
        'success': True,
        'movies': [m.format() for m in Movie.query.all()]
    })


@APP.route('/movies', methods=['POST'])
@requires_auth('create:movies')
def create_movie():
    """Add a new movie to the database

    Payload parameters:
    title -- the name of the movie (required)
    release_date -- the date that the movie will be released in YYYY-MM-DD format (optional)

    Returns an object, with the newly persisted movie if successful.
    """

    data = request.get_json()
    if not data or not data.get('title'):
        abort(400, description='`title` attribute must be provided.')

    if data.get('release_date') and convert_date_to_dateobj(data['release_date']) == None:
        abort(400, description='`release_date` must be in format YYYY-MM-DD')

    movie = Movie(title=data['title'])
    if data.get('release_date'):
        movie.release_date = data['release_date']

    movie.insert()

    return jsonify({
        'success': True,
        'movie': movie.format()
    })


@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('update:movies')
def update_movie(movie_id):
    """Updates an existing movie's information in the database

    Payload parameters:
    title -- the name of the movie (required)
    release_date -- the date that the movie will be released in YYYY-MM-DD format (optional)

    At least one of the parameters above must be specified, or the call will fail with a 400 error.
    Returns an object, with the updated movie metadata if successful.
    """

    data = request.get_json()
    if not data or not (data.get('title') or data.get('release_date')):
        abort(
            400, description='Either `title` or `release_date` attribute must be specified')

    if data.get('release_date') and convert_date_to_dateobj(data['release_date']) == None:
        abort(400, description='`release_date` must be in format YYYY-MM-DD')

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(
            404, description=f'Unable to find the specified movie_id: {movie_id}')

    if data.get('title'):
        movie.title = data['title']

    if data.get('release_date'):
        movie.release_date = data['release_date']

    movie.update()

    return jsonify({
        'success': True,
        'movie': movie.format()
    })


@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    """Deletes an existing movie from the database

    Returns an object, with the movie_id that was removed if successful.
    """

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(
            404, description=f'Unable to find the specified movie_id: {movie_id}')

    movie.delete()

    return jsonify({
        'success': True,
        'movie_id': movie_id
    })


@APP.route('/movies/<int:movie_id>/actors', methods=['POST'])
@requires_auth('create:role')
def add_actor_to_movie(movie_id):
    """Add an actor to a movie in the database

    Payload parameters:
    actor_id -- the id of the actor being added to the movie (required)

    Returns an object, with the movie that the actor was added to if successful.
    """

    data = request.get_json()
    if not data or not data.get('actor_id'):
        abort(400, description='`actor_id` attribute must be specified')

    actor_id = data['actor_id']

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(
            404, description=f'Unable to find the specified movie_id: {movie_id}')

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(
            404, description=f'Unable to find the specified actor_id: {actor_id}')

    existing_role = Role.query.filter(
        Role.movie_id == movie_id and Role.actor_id == actor_id).one_or_none()
    if existing_role:
        abort(
            409, description=f'`actor_id`: {actor_id} already has a role in `movie_id`: {movie_id}')

    role = Role(movie_id=movie_id, actor_id=actor_id)
    role.insert()

    return jsonify({
        'success': True,
        'movie': movie.format()
    })


@APP.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:role')
def remove_actor_from_movie(movie_id, actor_id):
    """Remove an actor from a movie in the database

    Returns an object, with the movie_id and actor_id that was deleted if successful.
    """

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(
            404, description=f'Unable to find the specified movie_id: {movie_id}')

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(
            404, description=f'Unable to find the specified actor_id: {actor_id}')

    role = Role.query.filter(
        Role.movie_id == movie_id and Role.actor_id == actor_id).one_or_none()

    if not role:
        abort(
            409, description=f'`actor_id`: {actor_id} is not currently listed as having a role in `movie_id`: {movie_id}')

    role.delete()

    return jsonify({
        'success': True,
        'movie_id': movie_id,
        'actor_id': actor_id
    })


########
# Error handlers
########

@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'status': 400,
        'message': error.description
    }), 400


@APP.errorhandler(401)
def not_authorized(error):
    return jsonify({
        'success': False,
        'status': 401,
        'message': error.description,
    }), 401


@APP.errorhandler(403)
def access_forbidden(error):
    return jsonify({
        'success': False,
        'status': 403,
        'message': error.description,
    }), 403


@APP.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'status': 404,
        'message': error.description,
    }), 404


@APP.errorhandler(409)
def resource_conflict(error):
    return jsonify({
        'success': False,
        'status': 409,
        'message': error.description,
    }), 409


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=9000, debug=True)
