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
* Activate environment variables using following commands:
    ```bash
        cd backend
        source setup.sh
        pip install -r requirements.txt
        export DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name>"
    ```
* Create database for API testing and change database_path on ` test_app.py ` file
* To setup models and fill database run following command:
    ```bash
        python3 manage.py setup_database
    ```


# Run application
* ⚠ Firstly you should setup database
* Windows using Git Bash:
    ```bash
        cd backend
        source setup.sh
        pip install -r requirements.txt
        export DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name>"
        python manage.py runserver
    ```
* MacOS/Linux:
    ```bash
        cd backend
        source setup.sh
        pip install -r requirements.txt
        export DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name>"
        python3 manage.py runserver
    ```

### Authentication:
  - This API requires auth, and uses auth0 authentication system
  - **Auth type🔐**: JWT
  - This API supports RBAC 🔐
  - There are 3 roles for management:
    ```code
        - Assistant🔎
        - Director🔎♻
        - Executive Producer🔎♻🎥
    ```


  - Permissions:
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


  - To testing API, I`ve prepared three accounts:
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
  - Login to accounts:
    - To `login/signup` you should got to the page: https://auth0-service.us.auth0.com/authorize?response_type=token&audience=casting_agency&client_id=kHjeEWjekFk5ke7sFU0lLzvCsWFaGAKY&redirect_uri=http://127.0.0.1:8100
    - After login/signup get token from url, this token is used to send requests to API endpoints



# Testing
* ⚠ Firstly you should create database for API testing and change database_path on ` test_app.py ` file, and setup environment variables
## First method: unittest
**Run the following comands:**
```bash
        cd backend
        source setup.sh
        export TEST_DATABASE_URL="postgresql://<username>:<password>@localhost:5432/<your_db_name_for_testing>"
        export ASSISTANT_TOKEN="<assitant_token>"
        export DIRECTOR_TOKEN="<director_token>"
        export PRODUCER_TOKEN="<producer_token>"
        python3 manage.py runtests
```


> ![CURL](./screenshots/unittestTests.PNG)

## Second method: Postman
1. Open your postman app, and import postman collection
2. Then setUp environment variables(global)
> ![CURL](./screenshots/setUp.PNG)







