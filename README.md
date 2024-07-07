# Casting Agency
The Casting Agency project is a straightforward and efficient web application designed to facilitate basic CRUD (Create, Read, Update, Delete) operations for a casting agency's core activities. This application models a company that specializes in creating movies and managing the assignment of actors to those movies. With a focus on simplicity and user-friendliness, the system aims to streamline the process of movie and actor management, making it easier for casting agencies to organize their projects and talent. 

# Setup for local developement
## Install requirements
To install the reuqirements run:
```bash
pip install -r requirements.txt
```
*I would recommend using an virtual enviroment*

## Setting up the Enviroment
To run the app create a .env file with following contents:
```env
DATABASE_PATH = 'Database Path'
TEST_DATABASE_PATH = 'Test Database Path'

AUTH_DOMAIN = 'Your Auth0 Domain'
ALGORITHMS = ['Your Algorithm']
API_AUDIENCE = 'Your API Audience'
CLIENT_ID = 'Your Client ID'
CALLBACK_URI = 'https://localhost:8080/login-results'

FLASK_APP='app.py'
FLASK_ENV='development'
FLASK_RUN_PORT=8080
FLASK_RUN_HOST="localhost"
```
Additionally you may need to run following command:
```bash
export PYTHONPATH=$(pwd)
```
*For the Reviewers: I will provide the correct Auth0 specifications in the text field*

## Flask Migrate
To set up your database using flask migrate run the following commands:
```bash
flask db init
flask db migrate -m "initial migration message"
flask db upgrade
```
This will set up the database of the provided DATABASE_PATH.

## Run the Application locally
To run your application run either:
```bash
flask run --reload
```
*The --reload flag reloads your application when you make changes to the code, wihtout restarting it (its handy for developement)*

or:
```bash
python3 flask_app.py
```

## Unittesting
For Unittesting run:
```bash
python3 -m unittest test_app.py
```

# API Endpoints Documentation
## General
- ```GET /```

Description: Welcome message for the Casting Agency API.

Example Request:
```bash
curl http://localhost:8080/
```

Example Response:
```json
{
  "message": "Welcome to the Casting Agency API."
}
```
## Actors
- ```GET /actors```

Required Permission: ```get:actors```

Description: Retrieves a list of all actors.

Example Request:
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8080/actors
```

Example Response:
```json
{
  "actors": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "gender": "Male"
    },
    {
      "id": 2,
      "name": "Jane Doe",
      "age": 25,
      "gender": "Female"
    }
  ],
  "success": true
}
```

- ```POST /actors```

Required Permission: ```post:actors```

Request Body: Requires name, age, and gender.

Description: Creates a new actor with the provided details.

Example Request:
```bash
curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"name":"Emily Clark", "age":28, "gender":"Female"}' http://localhost:8080/actors
```

Example Response:
```json
{
  "actor": {
    "id": 3,
    "name": "Emily Clark",
    "age": 28,
    "gender": "Female"
  },
  "success": true
}
```

- ```PATCH /actors/int:actor_id```

Required Permission: ```patch:actors```

Request Parameters: actor_id (URL parameter)

Request Body: Can include name, age, and/or gender.

Description: Updates an existing actor identified by actor_id with provided details.

Example Request:
```bash
curl -X PATCH -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"name":"Emily Clarke", "age":29}' http://localhost:8080/actors/3
```

Example Response:
```json
{
  "actor": {
    "id": 3,
    "name": "Emily Clarke",
    "age": 29,
    "gender": "Female"
  },
  "success": true
}
```

- ```DELETE /actors/int:actor_id```

Required Permission: ```delete:actors```

Request Parameters: actor_id (URL parameter)

Description: Deletes an actor identified by actor_id.

Example Request:
```bash
curl -X DELETE -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8080/actors/2
```

Example Response:
```json
{
  "deleted": 2,
  "success": true
}
```

## Movies
- ```GET /movies```

Required Permission: ```get:movies```

Description: Retrieves a list of all movies.

Example Request:
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8080/movies
```

Example Response:
```json
{
  "movies": [
    {
      "id": 1,
      "title": "Inception",
      "release_date": "2010-07-16"
    },
    {
      "id": 2,
      "title": "The Matrix",
      "release_date": "1999-03-31"
    }
  ],
  "success": true
}
```


- ```POST /movies```

Required Permission: ```post:movies```

Request Body: Requires title and release_date.

Description: Creates a new movie with the provided details.

Example Request:
```bash
curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"title":"Interstellar", "release_date":"2014-11-07"}' http://localhost:8080/movies
```

Example Response:
```json
{
  "movie": {
    "id": 3,
    "title": "Interstellar",
    "release_date": "2014-11-07"
  },
  "success": true
}
```

- ```PATCH /movies/int:movie_id```

Required Permission: ```patch:movies```

Request Parameters: movie_id (URL parameter)

Request Body: Can include title and/or release_date.

Description: Updates an existing movie identified by movie_id with provided details.

Example Request:
```bash
curl -X PATCH -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"title":"Interstellar Updated", "release_date":"2014-11-07"}' http://localhost:8080/movies/3
```

Example Response:
```json
{
  "movie": {
    "id": 3,
    "title": "Interstellar Updated",
    "release_date": "2014-11-07"
  },
  "success": true
}
```

- ```DELETE /movies/int:movie_id```

Required Permission: ```delete:movies```

Request Parameters: movie_id (URL parameter)

Description: Deletes a movie identified by movie_id.

Example Request:
```bash
curl -X DELETE -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8080/movies/3
```

Example Response:
```json
{
  "deleted": 3,
  "success": true
}
```
## Association
- ```POST /associate/```

Required Permission: ```post:movies```

Request Body: includes movie and actor id.

Description: Creates and association between an actor and a movie based on their id.

Example Request:
```bash
curl -X POST http://localhost:8080/associate -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"actor_id": 1, "movie_id": 2}'
```

Example Response:
```json
{
  "success": true,
  "actor_id": 1,
  "movie_id": 2
}
```
## Error Handling
Common error codes include:

- 400: Bad Request

Example Response:
```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```
- 404: Resource Not Found

Example Response:
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```
- 422: Unprocessable Entity

Example Response:
```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable"
}
```
- 500: Internal Server Error

Example Response:
```json
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```

# Authentication
## Authentication and Permissions
Auth0 is used for Third-Party Authentication. There are 3 different roles each with its own set of permissions:
- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

## Auth0 Role Assignement
Roles will be assigned via the Auth0 Dashboard.\
*For the Reviewers: I will provide login data for test purposes in the text field*

You can login here and retrieve a JWT for further testing and working with the API:
```URL
https://dev-testeb.eu.auth0.com/authorize?audience=agency&response_type=token&client_id=xrwwXDF6z3xAq2R3jS1dCQo5iTCfze2y&redirect_uri=https://localhost:8080/login-results
```
*You'll have to manually extract the access-token from the URL*

## Testing Authentication with Postman
### Setup DB for Testing
To run your Postman-Tests first create a test database and run the init_test_db.sql file
(replace username with your corresponding database username):
```bash
psql -U username -c "DROP DATABASE IF EXISTS agencytest;"
psql -U username -c "CREATE DATABASE agencytest;"
psql -U username -d agencytest -f init_test_db.sql
```
Put the corresponding Database Path into your .env file as TEST_DATABASE_PATH.
Change the config.py file to retrieve TEST_DATABASE_PATH instead of DATABASE_PATH.

Once you've done that you can run your application using:
```bash
flask run --reload
```
*Don't forget to change back your config.py file once you are done testing*

### Send Requests
Once your retrieved an access token for each Role you can import the given
postman_collection.json into Postman and change the URL and Token variables with
the correct values for your application.

Once you have run the Tests and would like to repeat it, you'll have to run the init_test_db.sql script again:
```bash
psql -U username -d agencytest -f init_test_db.sql
```
*Notice: The Postman Tests don't request every Endpoint, since we only test the authentication mechanism here.*
# Dockerization and Local Deployment
To dockerize the application simply run:
```bash
docker build . -t ImageName
```
To run your image as a container run:
```bash
docker run -p 8080:8080 ImageName
```

# Deployment and Hosting
The Application will be deployed on Render Cloud. The Application run on an free instance, which may cause delays by 50 seconds or more, because it will spin down with inactivity. So don't despair!

Application URL: https://agencycapstone.onrender.com

To request the API you can use the Access-Token from before, aslong as its not expired. If so you would need to login again and retrieve a access token. *Refer: Auth0 Role Assignement*

