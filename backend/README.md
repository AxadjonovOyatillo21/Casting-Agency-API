# Casting Agency 🔥
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.
This is a Restful API written in Flask micro-framework.

# Introduction


## Tech Stack
------------------------------------------------------------------------------
|    Language    | Framework |  Database  | Tools for testting | Auth System |
|----------------|-----------|------------|--------------------|-------------|
| Python(v3.x.x) |   Flask   | Postgresql |  Unittest&Postman  |    Auth0    |


# SetUp database
* Create database called `casting_agency` or something which you like.
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
### To `login/signup` you should go to the page: https://auth0-service.us.auth0.com/authorize?response_type=token&audience=casting_agency&client_id=kHjeEWjekFk5ke7sFU0lLzvCsWFaGAKY&redirect_uri=http://127.0.0.1:8100
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
  - This endpoint does'nt raise any errors


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
  - This endpoint does'nt raise any errors

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
  - This endpoint does'nt raise any errors

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



