# Udacity's Got Talent - Casting Agency App 

Udacity's Got Talent is an app to allow Udacity to manage the allocation of our pool of talent (Actors) into upcoming Movie titles, providing visbilility into which actors are working on which projects. 

We built this app as previously the matching of actors to movies was performed manually in a google sheets spreadsheet, which made maintenance difficult, and permissions were not able to be appropriately enforced on the system.

## Setup for local development

This project depends on the following system requirements:

* `python3.8.1`
* `pyenv` - used to manage python virtual environments
* `postgres` - must have a local version of postgres setup

Before you can run the setup script, you must also set the following environment variables:

* `DATABASE_USER` - user that will be used to access the database
* `DATABASE_PWD` - password for the user accessing the database
* `DATABASE_HOST` - host where the database is running (default: localhost)
* `DATABASE_PORT` - port where the database is exposed (default: 5432))
* `DATABASE_NAME` - name of the database that will be used for the app

If you have the pre-requisites installed, you can get started by running `./setup.sh`

Once this is complete, you can run the app by executing: `cd src && python app.py`

The application will be available at `localhost:9000`

## Hosted application

This application is deployed to Heroku at: [https://fatpenguin-casting.herokuapp.com/](https://fatpenguin-casting.herokuapp.com/)

## Deploying the hosted application

The application is setup to automatically deploy from Github to Heroku on successful merge to master.

If any changes are made to the database schema, the following command needs to be run manually after the master deploy has completed:

`heroku run sh -c 'cd ./src/ && flask db upgrade' --app fatpenguin-casting`

This will perform a flask DB migration on the heroku server, and restart the application.

## API specification

All endpoints require authentication, using a valid `Bearer` token from `Auth0`.
See [how to setup authentication](#how-to-setup-authentication) for details on this.

### Authentication

There are 3 different roles for accessing the Casting Agency app.
1. Casting assistant - Can view actors and movies
1. Casting director - Casting assistant, plus adding/deleting actors, and modifying actors/movies
1. Executive producer - Casting director, plus adding/deleting movies

In order to request any of the APIs noted below, you must authenticate your requests using a `Bearer` token in the headers of the request.

For testing purposes, you can login with the following username and pwd combinations:

* `Casting assistant`: `joff@fatpengu.in;abcdef12345!`
* `Casting director`: `jaff@fatpengu.in;abcdef12345!`
* `Executive producer`: `juff@fatpengu.in;abcdef12345!`

You can login with the following URL, and grab the required access token from the authenticated URL:

`https://fatpenguin-casting.us.auth0.com/authorize?response_type=token&client_id=KSbxknf2Lju1At5LcVsFvN26Jz2N1F2P&audience=casting-agency&redirect_uri=http://localhost:9000/login`

### Actors APIs

#### GET
`GET /actors`

**Response (`200 OK`)**
```json
{
    "success": true,
    "actors": [
        {
            "id": 1,
            "name": "Actor name",
            "date_of_birth": "YYYY-MM-DD",
            "age": 35,                      // Age in years, calculated at request time
            "gender": "male",
            "movies": [
                {
                    "title": "Movie title",
                    "release_date": "YYYY-MM-DD"
                }
            ]
        }
    ]
}
```

#### POST
`POST /actors`

**Request body**
```json
{
    "name": "Actor name",          // required
    "date_of_birth": "YYYY-MM-DD", // optional, date format enforced
    "gender": "male"               // optional, no validation performed
}
```

**Response (`200 OK`)**
```json
{
    "success": true,
    "actor": {
        "id": 1,
        "name": "Actor name",
        "date_of_birth": "YYYY-MM-DD",
        "age": 35, // Age in years, calculated at request time
        "gender": "male",
        "movies": [
            {
                "title": "Movie title",
                "release_date": "YYYY-MM-DD"
            }
        ]
    } 
}
```

#### PATCH
`PATCH /actors/<int:actor_id>`

**Request body**
At least one of the properties outlined in the payload below must be provided.
```json
{
    "name": "Actor name",          // optional
    "date_of_birth": "YYYY-MM-DD", // optional, date format enforced
    "gender": "male"               // optional, no validation performed
}
```

**Response (`200 OK`)**
```json
{
    "success": true,
    "actor": {
        "id": 1,
        "name": "Actor name",
        "date_of_birth": "YYYY-MM-DD",
        "age": 35, // Age in years, calculated at request time
        "gender": "male",
        "movies": [
            {
                "title": "Movie title",
                "release_date": "YYYY-MM-DD"
            }
        ]
    }   
}
```

#### DELETE
`DELETE /actors/<int:actor_id>`

**Response (`200 OK`)**
```json
{
    "success": true,
    "actor_id": 1
}
```


### Movies APIs

#### GET
`GET /movies`

**Response (`200 OK`)**
```json
{
    "success": true,
    "movies": [
        {
            "id": 1,
            "title": "Movie title",
            "release_date": "YYYY-MM-DD",
            "actors": [
                {
                    "name": "Actor name",
                    "date_of_birth": "YYYY-MM-DD",
                    "age": 35,
                    "gender": "male"
                }
            ]
        }
    ]
}
```

#### POST
`POST /movies`

**Request body**
```json
{
    "title": "Movie name",         // required
    "release_date": "YYYY-MM-DD"   // optional, date format enforced
}
```

**Response (`200 OK`)**
```json
{
    "success": true,
    "movie": {
        "id": 1,
        "title": "Movie title",
        "release_date": "YYYY-MM-DD",
        "actors": [
            {
                "name": "Actor name",
                "date_of_birth": "YYYY-MM-DD",
                "age": 35,
                "gender": "male"
            }
        ]
    }
}
```

#### PATCH
`PATCH /movies/<int:movie_id>`

**Request body**
At least one of the properties outlined in the payload below must be provided.
```json
{
    "title": "Movie name",         // optional
    "release_date": "YYYY-MM-DD"   // optional, date format enforced
}
```

**Response (`200 OK`)**
```json
{
    "success": true,
    "movie": {
        "id": 1,
        "title": "Movie title",
        "release_date": "YYYY-MM-DD",
        "actors": [
            {
                "name": "Actor name",
                "date_of_birth": "YYYY-MM-DD",
                "age": 35,
                "gender": "male"
            }
        ]
    }
}
```

#### DELETE
`DELETE /movies/<int:movie_id>`

**Response (`200 OK`)**
```json
{
    "success": true,
    "movie_id": 1
}
```

### Roles APIs

### POST
`POST /movies/<int:movie_id>/actors`

**Request body**
```json
{
    "actor_id": 1  // required
}
```

**Response (`200 OK`)**
```json
{
    "success": true,
    "movie": {
        "id": 1,
        "title": "Movie title",
        "release_date": "YYYY-MM-DD",
        "actors": [
            {
                "name": "Actor name",
                "date_of_birth": "YYYY-MM-DD",
                "age": 35,
                "gender": "male"
            }
        ]
    }
}
```

### DELETE
`DELETE /movies/<int:movie_id>/actors/<int:actor_id>`

**Response (`200 OK`)**
```json
{
    "success": true,
    "movie_id": 1,
    "actor_id": 1
}
```

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

### 403 FORBIDDEN

Expected to be seen if the validated token provided does not have access to the requested resources. 

```json
{
    "success": false,
    "status": 403,
    "message": "custom error message based on what caused the forbidden error to occur"
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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.