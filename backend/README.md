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
* Create database called `casting_agency` or something which you like. :
* Activate environment variables using following command:
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

1. Setup
2. Getting Started
3. Examples


## SetUp requirements





