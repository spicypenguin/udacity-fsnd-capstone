# Udacity's Got Talent - Casting Agency App 

Udacity's Got Talent is an app to allow Udacity to manage the allocation of our pool of talent (Actors) into upcoming Movie titles, providing visbilility into which actors are working on which projects. 

We built this app as previously the matching of actors to movies was performed manually in a google sheets spreadsheet, which made maintenance difficult, and permissions were not able to be appropriately enforced on the system.

## Installation for local development

This project depends on the following system requirements:

* `python3.8.1`
* `pyenv` - used to manage python virtual environments
* `postgres` - must have a local version of postgres setup

Before you can run the setup script, you must also:

* Create a database named `castingagency`
* Create a user named `castingagency`
* Create a `.env` file in the `src/` folder that contains an appropriate connection string to your postgres installation

If you have the pre-requisites installed, you can get started by running `./setup.sh`

Once this is complete, you can run the app by executing: `python app.py`

The application will be available at `localhost:9000`

## Hosted application

This application is deployed to Heroku at: https://<appnamehere>


## API specification

All endpoints require authentication, using a valid `Bearer` token from `Auth0`.
See [how to setup authentication](#how-to-setup-authentication) for details on this.

### Authentication

TBC

### Actors APIs

#### GET
`GET /actors`

#### POST
`POST /actors`

#### PATCH
`PATCH /actors/<int:actor_id>`

#### DELETE
`DELETE /actors/<int:actor_id>`


### Movies APIs

#### GET
`GET /movies`

#### POST
`POST /movies`

#### PATCH
`PATCH /movies/<int:movie_id>`

#### DELETE
`DELETE /movies/<int:movie_id>`


### Roles APIs

### POST
`POST /movies/<int:movie_id>/actors`

### DELETE
`DELETE /movies/<int:movie_id>/actors/<int:actor_id>`

### Error cases

You can expect to see the following errors thrown by the application.

### 400 BAD REQUEST

Expected to be seen if the data provided in the request was invalid based on the type of request being performed.

```json
{
    "success": false,
    "status": 400,
    "message": "custom error message based on what part of the request was unexpected"
}
```

### 401 UNAUTHORIZED

Expected to be seen if there was a problem validating the authentication headers of a request.

```json
{
    "success": false,
    "status": 401,
    "message": "custom error message based on what caused the unauthorized error to occur"
}
```

### 404 RESOURCE NOT FOUND

Expected to be seen if a request is processed against an actor_id or movie_id that does not exist.

```json
{
    "success": false,
    "status": 404,
    "message": "custom error message based on what resource was not found"
}
```

### 409 RESOURCE CONFLICT

Expected to be seen if an actor is attempted to be added to a movie, but they are already listed in a role on the same movie (duplicate data entry).

```json
{
    "success": false,
    "status": 409,
    "message": "custom error message based on what caused the conflict to occur"
}
```

## Local development

```bash
cd src\
python app.py
```

App will be running at `localhost:9000`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.