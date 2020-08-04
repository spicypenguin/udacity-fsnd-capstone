# Udacity's Got Talent - Casting Agency App 

Udacity's Got Talent is an app to allow Udacity to manage the allocation of our pool of talent (Actors) into upcoming Movie titles, providing visbilility into which actors are working on which projects. 

## Installation

If you have the pre-requisites installed, you can get started by running: 

```bash
./setup.sh
```

This requires `pyenv` to be installed to setup a virtualenvironment for your application.

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