# Casting Agency 🔥
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.
This is a Restful API written in Flask micro-framework.

# Introduction

## API deployed to heroku: https://casting-agency-api-v1.herokuapp.com/

## Tech Stack
------------------------------------------------------------------------------
|    Language    | Framework |  Database  | Tools for testing | Auth System |
|----------------|-----------|------------|--------------------|-------------|
| Python(v3.x.x) |   Flask   | Postgresql |  Unittest&Postman  |    Auth0    |


# SetUp database
* Create database called `casting_agency`.
* Create database for API testing and change database_path on ` test_app.py ` file



# Run application(run)
* ⚠ Firstly you should setup database
* Windows using Git Bash:
    ```bash
        cd backend
        python -m venv env
        source env/scripts/activate
        source setup.sh
        pip install -r requirements.txt
        export DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name>"
        export TEST_DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name_for_testing>"
        export ASSISTANT_TOKEN="<assitant_token>"
        export DIRECTOR_TOKEN="<director_token>"
        export PRODUCER_TOKEN="<producer_token>"
        python manage.py runserver
    ```
* MacOS/Linux:
    ```bash
        cd backend
        python3 -m venv env
        source env/bin/activate
        source setup.sh
        pip3 install -r requirements.txt
        export DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name>"
        export TEST_DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name_for_testing>"
        export ASSISTANT_TOKEN="<assitant_token>"
        export DIRECTOR_TOKEN="<director_token>"
        export PRODUCER_TOKEN="<producer_token>"
        python3 manage.py runserver
    ```
> ![CURL](./screenshots/runApp1.png)
> ![CURL](./screenshots/runApp2.png)
* To setup models and fill database run following command:
    ```bash
        python3 manage.py setup_db
    ```
> ![CURL](./screenshots/fill.png)


# Authentication
### This API requires auth, and uses auth0 authentication system
### **Auth type🔐**: JWT
### This API supports RBAC 🔐

**There are 3 roles for management**:
  ```code
    - Assistant🔎
    - Director🔎♻
    - Executive Producer🔎♻🎥
  ```

**Permissions**:
  ```code
    - Assitant:
        - `view:genres`
        - `view:actors`
        - `view:movies`
    - Director:
        - All permissions of assistant
        -  `add:actors`
        -  `delete:actors`
        -  `patch:actors`
        -  `patch:actors`
        -  `patch:actors`
    - Executive Producer:
        - All permissions of director
        - `add:genres`
        - `add:movies`
        - `delete:genres`
        - `delete:movies`
  ```

**To testing API, I`ve prepared three accounts**:
  ```code
    - Assistant account:
        - **email📫**: caAssistant@gmail.com
    - Director account:
        - **email📫**: caDirector@gmail.com
    - Executive Producer:
        - **email📫**: caProducer@gmail.com
    - Password🔑:
        - **casting_agency123**
  ```
## Login🔐 to accounts*:
### To `login/signup` you should go to the page: [login/signup](https://auth0-service.us.auth0.com/authorize?response_type=token&audience=casting_agency&client_id=kHjeEWjekFk5ke7sFU0lLzvCsWFaGAKY&redirect_uri=http://127.0.0.1:8100)
> ![CURL](./screenshots/login.PNG)

### After `login/signup` get token from url, this token is used to send requests to API endpoints
> ![CURL](./screenshots/loginResults.PNG)

### Let's decode jwt, to decode jwt navigate to jwt.io website
> ![CURL](./screenshots/jwtio.PNG)

### To logout, naviagte to page: https://auth0-service.us.auth0.com/logout
> ![CURL](./screenshots/logout.PNG)

# Testing
* ⚠ First of all ran all commands in Run application section!
* ⚠ Firstly you should create database for API testing and change database_path on ` test_app.py ` file, and setup environment variables
## First method: unittest
1. **Run the following comands:**
```bash
        python3 manage.py runtests
```
> ![CURL](./screenshots/unittestTests.png)
2. **Success🎉**

## Second method: Postman
1. Open your postman app, and import postman collection
2. Then setUp environment variables(global)
> ![CURL](./screenshots/setUp.png)
3. Run the following commands:
```bash
    python3 manage.py setup_db
    python3 manage.py runserver
```
> ![CURL](./screenshots/fill.png)
4. Run collection
> ![CURL](./screenshots/postman1.png)
> ![CURL](./screenshots/postman2.png)
> ![CURL](./screenshots/postman3.png)

# API Errors

-----------------------------------
| Error |  Description            |
|-------|-------------------------|
|  400  |  Bad request            |
|  401  |  Unauthorized           |
|  403  |  Access Denied          |
|  404  |  Not found              |
|  405  |  Method not allowed     |
|  422  |  Unprocessable Entity   |
|  500  |  Internal Server Error  |

## Example:
  - 400:
  ```json
    {
        "error_code": 400,
        "error_message": "Bad Request",
        "success": false
    }
  ```


# API reference

## Authentication🔐
  In this API authentication is **required**, and it uses JWT tokens for auth, but it contains **public** endpoints too

# Endpoints
To send requests we use curl, another tool is - Postman :)
Let's SetUp our curl to send requests
```bash
    host=127.0.0.1:5000
    token=<jwt_token>
```

# GET /
### General:
  - **Home Page😃**

### Permission:
  - This endpoint is public

### Example📋:
  - Request: ` curl $host `

  - Response:
    ```json
        {
            "message": "Casting agency is running 🚀🎉",
            "success": true
        }
    ```
### Errors🐞
  - This endpoint doesn't raise any errors


# GET /genres
### General:
  - Get Movie Genres. Returns short information about genres

### Permission:
  - This endpoint is public

### Example📋:
  - Request: ` curl $host/genres `

  - Response:
    ```json
        {
            "genres": [
                {
                    "genre_name": "science-fiction",
                    "id": 2
                },
                {
                    "genre_name": "lorem ipsum",
                    "id": 3
                }
            ],
            "success": true,
            "total_genres": 2
        }
    ```
### Errors🐞
  - This endpoint does'nt raise any errors

# GET /actors
### General:
  - Get Actors. Returns short information about actors

### Permission:
  - This endpoint is public

### Example📋:
  - Request: ` curl $host/actors `

  - Response:
    ```json
        {
            "actors": [
                {
                    "id": 3,
                    "name": "Taner Olmez"
                },
                {
                    "id": 4,
                    "name": "Onur Tuna"
                }
            ],
            "success": true,
            "total_actors": 2
        }
    ```
### Errors🐞
  - This endpoint doesn't raise any errors

# GET /movies
### General:
  - Get Movies. Returns short information about movies

### Permission:
  - This endpoint is public

### Example📋:
  - Request: ` curl $host/movies `

  - Response:
    ```json
        {
            "movies": [
                {
                    "id": 2,
                    "title": "Lucy"
                },
                {
                    "id": 3,
                    "title": "Iron Man"
                }
            ],
            "success": true,
            "total_movies": 2
        }
    ```
### Errors🐞
  - This endpoint doesn't raise any errors

# GET /genres-detail
### General:
  - Get Genres. Returns full information about genres

### Permission:
  - ` view:genres `

### Example📋:
  - Request:
    ```bash
        curl $host/genres-detail \
        -H "Authorization: Bearer $token"
    ```

  - Response:
    ```json
        {
            "genres": [
                {
                    "genre_name": "science-fiction",
                    "id": 2,
                    "movies_in_this_genre": [
                        {
                        "id": 2,
                        "title": "Lucy"
                        }
                    ]
                },
                {
                    "genre_name": "lorem ipsum",
                    "id": 3,
                    "movies_in_this_genre": []
                }
            ],
            "success": true,
            "total_genres": 2
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.

# GET /actors-detail
### General:
  - Get Actors. Returns full information about actors

### Permission:
  - ` view:actors `

### Example📋:
  - Request:
    ```bash
        curl $host/actors-detail \
        -H "Authorization: Bearer $token"
    ```

  - Response:
    ```json
        {
            "actors": [
                {
                    "age": 33,
                    "gender": "woman",
                    "id": 3,
                    "movies": [
                        {
                            "id": 2,
                            "title": "Lucy"
                        }
                    ],
                    "name": "Scarlet Johansson"
                },
                {
                    "age": 33,
                    "gender": "man",
                    "id": 4,
                    "movies": [],
                    "name": "Onur Tuna"
                }
            ],
            "success": true,
            "total_actors": 2
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.

# GET /movies-detail
### General:
  - Get Movies. Returns full information about movies

### Permission:
  - ` view:movies `

### Example📋:
  - Request:
    ```bash
        curl $host/movies-detail \
        -H "Authorization: Bearer $token"
    ```

  - Response:
    ```json
        {
            "movies": [
                {
                    "id": 2,
                    "movie_actors": [
                        {
                        "id": 3,
                        "name": "Onur Tuna"
                        }
                    ],
                    "movie_genres": [
                        {
                        "genre_name": "science-fiction",
                        "id": 2
                        }
                    ],
                    "release_date": "12/12/2006",
                    "title": "Lucy"
                },
                {
                    "id": 3,
                    "movie_actors": [],
                    "movie_genres": [],
                    "release_date": "11/12/2007",
                    "title": "Iron Man"
                }
            ],
            "success": true,
            "total_movies": 2
        }

    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.



# GET /genres/<genre_id>
### General:
  - Get Single Genre. Returns genre with given id

### Permission:
  - ` view:genres `

### Example📋:
  - Request:
    ```bash
        curl $host/genres/2 \
        -H "Authorization: Bearer $token"
    ```

  - Response:
    ```json
        {
            "genre": {
                "genre_name": "science-fiction",
                "id": 2,
                "movies_in_this_genre": [
                    {
                        "id": 2,
                        "title": "Lucy"
                    }
                ]
            },
            "success": true,
            "total_genres": 2
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **404** error, if genre with given id doesn't exixsts in database.



# GET /actors/<actor_id>
### General:
  - Get Single Actor. Returns actor with given id

### Permission:
  - ` view:actors `

### Example📋:
  - Request:
    ```bash
        curl $host/actors/3 \
        -H "Authorization: Bearer $token"
    ```

  - Response:
    ```json
        {
            "actor": {
                "age": 33,
                "gender": "woman",
                "id": 3,
                "movies": [
                    {
                        "id": 2,
                        "title": "Lucy"
                    }
                ],
                "name": "Scarlett Johansson"
            },
            "success": true,
            "total_actors": 2
        }

    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **404** error, if actor with given id doesn't exixsts in database.


# GET /movies/<movie_id>
### General:
  - Get Single Movie. Returns movie with given id

### Permission:
  - ` view:movies `

### Example📋:
  - Request:
    ```bash
        curl $host/movies/2 \
        -H "Authorization: Bearer $token"
    ```

  - Response:
    ```json
        {
            "movie": {
                "id": 2,
                "movie_actors": [
                    {
                        "id": 3,
                        "name": "Scarlett Johansson"
                    }
                ],
                "movie_genres": [
                    {
                        "genre_name": "science-fiction",
                        "id": 2
                    }
                ],
                "release_date": "12/12/2006",
                "title": "Lucy"
            },
            "success": true,
            "total_movies": 2
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **404** error, if movie with given id doesn't exixsts in database.


# `POST` /genres
### General:
  - Add new genre.
  - The request must contain JSON data.
  - JSON data must contain key:
    -------------------------------
    |  key       |  type          |
    |------------|----------------|
    | genre_name | String(Unique) |

### Permissions:
  - ` add:genres `

### Example📋:
  - Request:
    ```bash
        curl $host/genres \
        -X POST \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --DATA '{"genre_name": "scientific"}'
    ```

  - Response:
    ```json
        {
            "created": true,
            "genre": {
                "genre_name": "scientific",
                "id": 5,
                "movies_in_this_genre": []
            },
            "success": true,
            "total_genres": 4
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **400** error, if required json data incorrect or json data empty or new ` genre_name ` exists in ` database `
  - This endpoint raises **404** error, if genre with given id doesn't exists in database
  - This endpoint raises **422** error, if inserting was unsuccessfull

# `POST` /actors
### General:
  - Add new actor.
  - The request must contain JSON data.
  - JSON data must contain keys:
    ---------------------------------------------------------------------------------------------------------------------------
    | key       | type                                     | isRequired | Description                                         |
    |-----------|------------------------------------------|------------|-----------------------------------------------------|
    | name      | String                                   |  required  | full name of actor                                  |
    | age       | Integer                                  |  required  | age of actor                                        |
    | gender    | String(values must be: `man` or `woman`) |  required  | gender                                              |
    | movies_id | Array with integer values                |  optional  | an array of movies id, where this actor played role |

### Permissions:
  - ` add:actors `

### Example📋:
  - Request:
    ```bash
        curl $host/actors \
        -X POST \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --data-raw '{
            "name": "Tony Stark",
            "age": 30,
            "gender": "man",
            "movies_id": [3]
        }'
    ```

  - Response:
    ```json
        {
            "actor": {
                "id": 5,
                "name": "Tony Stark"
            },
            "created": true,
            "success": true,
            "total_actors": 3
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **400** error:
    - If name length < 3
    - If age:
      - equals to 0, or less than 0
      - if string
    - if gender incorrect, correct data: "man"/"woman"
    - if movies_id not an array or does'nt include integer values, or movie doesn't exists in database with given id on array
    - This endpoint raises **404** error, if actor with given id doesn't exists in database
    - This endpoint raises **422** error, if inserting was unsuccessfull

    Example:
      - Request:
        ```bash
            curl $host/actors \
            -X POST \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            --data-raw '{
                "name": "To",
                "age": "a23",
                "gender": "mannn",
                "movies_id": ["lorem"]
            }'
        ```
      - Response:
       ```json
            {
                "error_code": 400,
                "error_message": "Bad Request",
                "success": false
            }
        ```


# `POST` /movies
### General:
  - Add new movies.
  - The request must contain JSON data.
  - JSON data must contain keys:
    ------------------------------------------------------------------------------------------------------------------------------
    | key          | type                                     | isRequired | Description                                         |
    |--------------|------------------------------------------|------------|-----------------------------------------------------|
    | title        | String(Unique)                           |  required  | full name of actor                                  |
    | release_date | String, pattern="DD/MM/YY"               |  required  | release date                                        |
    | actors_id    | Array with integer values                |  optional  | an array of movie actors id                         |
    | genres_id    | Array with integer values                |  optional  | an array of movies genres id                        |

### Permissions:
  - ` add:movies `

### Example📋:
  - Request:
    ```bash
        curl $host/movies \
        -X POST \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --data-raw '{
            "title": "Mucize Doktor",
            "release_date": "12/12/2019",
            "genres_id": [2, 5],
            "actors_id": [5, 7]
        }'
    ```

  - Response:
    ```json
        {
            "created": true,
            "movie": {
                "id": 4,
                "title": "Mucize Doktor"
            },
            "success": true,
            "total_movies": 3
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **400** error:
    - if title length < 3 or empty
    - if movie with given title exists in database
    - if release date incorrect
      - "DD/MM/YY" -> "DD" musn't be > 31 and < 0, "MM" musn't be > 12 and < 0
    - if gender incorrect, correct data: "man"/"woman"
    - if actors_id not an array or does'nt include integer values, or actor doesn't exists in database with given id on array
    - if genres_id not an array or does'nt include integer values, or genre doesn't exists in database with given id on array
    - This endpoint raises **404** error, if movie with given id doesn't exists in database
    - This endpoint raises **422** error, if inserting was unsuccessfull

    Example:
      - Request:
        ```bash
            curl $host/movies \
            -X POST \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            --data-raw '{
                "title": "",
                "release_date": "12213/-1000/2019",
                "genres_id": ["adasd", 123213213213],
                "actors_id": [890089089321123]
            }'
        ```
      - Response:
       ```json
            {
                "error_code": 400,
                "error_message": "Bad Request",
                "success": false
            }
        ```


# `PATCH` /genres/<genre_id>
### General:
  - Update genre.
  - The request must contain JSON data.
  - JSON data must contain key:
    -------------------------------
    |  key       |  type          |
    |------------|----------------|
    | genre_name | String(Unique) |

### Permissions:
  - ` update:genres `

### Example📋:
  - Request:
    ```bash
        curl $host/genres/2 \
        -X PATCH \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --DATA '{"genre_name": "medicine"}'
    ```

  - Response:
    ```json
        {
            "genre": {
                "genre_name": "medicine",
                "id": 2
            },
            "success": true,
            "total_genres": 4,
            "updated": true
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **400** error, if json data empty, or len of value `genre_name` < 3
  - This endpoint doesn't raise **400** error, if you give empty value to `genre_name` key
  - This endpoint raises **404** error, if genre with given id doesn't exists in database
  - This endpoint raises **422** error, if updating was unsuccessfull


# `PATCH` /actors/<actor_id>
### General:
  - Update actor.
  - The request must contain JSON data.
  - JSON data must contain keys:
    ----------------------------------------------------------------------------------------------------------------------------------
    | key              | type                                     | isRequired | Description                                         |
    |------------------|------------------------------------------|------------|-----------------------------------------------------|
    | name             | String                                   |  required  | full name of actor                                  |
    | age              | Integer                                  |  required  | age of actor                                        |
    | gender           | String(values must be: `man` or `woman`) |  required  | gender                                              |
    | movies_id        | Array with integer values                |  optional  | an array of movies id, where this actor played role |
    | remove_movies_id | Array with integer values                |  optional  | an array of movies id, which will be removed        |
  - You can update one parameter or all :)

### Permissions:
  - ` update:actors `

### Example📋:
  - Request:
    ```bash
        curl $host/actors/5 \
        -X PATCH \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --data-raw '{
            "name": "Lorem Stark",
            "age": 33,
            "remove_movies_id": [3]
        }'
    ```

  - Response:
    ```json
        {
            "actor": {
                "id": 5,
                "name": "Lorem Stark"
            },
            "success": true,
            "total_actors": 8,
            "updated": true
        }
    ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **400** error:
    - If name length < 3
    - If age:
      - equals to 0, or less than 0
      - if string
    - if gender incorrect, correct data: "man"/"woman"
    - if movies_id not an array or does'nt include integer values, or movie doesn't exists in database with given id on array
    - if remove_movies_id not an array or does'nt include integer values, or movie doesn't exists in database with given id on array
    - This endpoint doesn't raise **400** error, if json data empty looks like: {}
    - This endpoint raises **404** error, if actor with given id doesn't exists in database
    - This endpoint raises **422** error, if updating was unsuccessfull


# `PATCH` /movies/<movie_id>
### General:
  - Update movie.
  - The request must contain JSON data.
  - JSON data must contain keys:
    ----------------------------------------------------------------------------------------------------------------------------------
    | key              | type                                     | isRequired | Description                                         |
    |------------------|------------------------------------------|------------|-----------------------------------------------------|
    | title            | String(Unique)                           |  optional  | full name of actor                                  |
    | release_date     | String, pattern="DD/MM/YY"               |  optional  | release date                                        |
    | actors_id        | Array with integer values                |  optional  | an array of movie actors id                         |
    | genres_id        | Array with integer values                |  optional  | an array of movies genres id                        |
    | remove_actors_id | Array with integer values                |  optional  | an array of actors id which will be removed         |
    | remove_genres_id | Array with integer values                |  optional  | an array of genres id which will be removed         |
  - You can update one parameter or all :)

### Permissions:
  - ` update:movies `

### Example📋:
  - Request:
    ```bash
        curl $host/movies/4 \
        -X POST \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        --data-raw '{
            "title": "Good Doctor",
            "remove_genres_id": [2],
            "remove_actors_id": [5, 7]
        }'
    ```
  - Response:
    ```json
        {
            "movie": {
                "id": 4,
                "title": "Good Doctor"
            },
            "success": true,
            "total_movies": 4,
            "updated": true
        }
    ```

### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **400** error:
    - if title length < 3 or empty
    - if movie with given title exists in database
    - if release date incorrect
      - "DD/MM/YY" -> "DD" musn't be > 31 and < 0, "MM" musn't be > 12 and < 0
    - if gender incorrect, correct data: "man"/"woman"
    - if actors_id not an array or does'nt include integer values, or actor doesn't exists in database with given id on array
    - if genres_id not an array or does'nt include integer values, or genre doesn't exists in database with given id on array
    - if remove_actors_id not an array or does'nt include integer values, or actor doesn't exists in database with given id on array
    - if remove_genres_id not an array or does'nt include integer values, or genre doesn't exists in database with given id on array
    - This endpoint doesn't raise **400** error, if json data empty looks like: {}
    - This endpoint raises **404** error, if movie with given id doesn't exists in database
    - This endpoint raises **422** error, if updating was unsuccessfull



# `DELETE` /genres/<genre_id>
### General:
    - Delete genre with given id.

### Permissions:
    - ` delete:genres `

### Example📋:
    - Request:
      ```bash
        curl $host/genres/2 \
        -X DELETE \
        -H "Authorization: Bearer $token"
      ```
    - Response:
      ```json
        {
            "deleted_id": 2,
            "success": true,
            "total_genres": 3
        }
      ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **404** error, if genre with given id doesn't exists in database
  - This endpoint raises **422** error, if deleting was unsuccessfull


# `DELETE` /actors/<actor_id>
### General:
    - Delete actor with given id.

### Permissions:
    - ` delete:actors `

### Example📋:
    - Request:
      ```bash
        curl $host/actors/5 \
        -X DELETE \
        -H "Authorization: Bearer $token"
      ```
    - Response:
      ```json
        {
            "deleted_id": 5,
            "success": true,
            "total_actors": 7
        }
      ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **404** error, if actor with given id doesn't exists in database
  - This endpoint raises **422** error, if deleting was unsuccessfull

# `DELETE` /movies/<movie_id>
### General:
    - Delete movie with given id.

### Permissions:
    - ` delete:movies `

### Example📋:
    - Request:
      ```bash
        curl $host/movies/4 \
        -X DELETE \
        -H "Authorization: Bearer $token"
      ```
    - Response:
      ```json
        {
            "deleted_id": 4,
            "success": true,
            "total_movies": 3
        }
      ```
### Errors🐞
  - This endpoint raises **401** error, if request doesn't contains jwt token or token expired.
  - This endpoint raises **403** error, if required permission not in jwt.
  - This endpoint raises **404** error, if movie with given id doesn't exists in database
  - This endpoint raises **422** error, if deleting was unsuccessfull

> [!CURL](./screenshots/deployed.png)

Author 👨🏻‍💻: Axadjonov Oyatillo | Uzbekistan 🇺🇿

