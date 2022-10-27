# Python API using FastAPI
## Introduction
In this project a fully functiong API for a simple social media app is created.

## Installation
### Virtual Environment
Create a virtaul environment using your preffered name <venv>:
    
    py -3 -m venv <venv>
### Activate venv (Windows)
    
    > venv\Scripts\activate

### Install the FastAPI libraries
    
    > pip install fastapi[all]

### Install the PostGres Communication Library
This is the driver for the communication with the PostGres SQL database. 

    > pip install psycopg2

### Install SQLAlchemy which is an ORM
Instead of using using psycopg2 as a direct communication tool with the database, you can use and Object Relational Mapper as bridge between Python commands and the database commands. psycopg2 executes SQL commands directly in python, but SQLAlchemy uses a python model for simulating the database and executes the SQL commands itself. Even if you are using SQLAlchemy, psycopg2 must be installed because this the driver to talk to the database, and SQLAlchemy also uses this driver. 

    > pip install sqlalchemy

### Install Passlibe with bcrypt algorithm
This is for hashing the password for the storage in database.

    > pip install passlib[bcrypt]


## Running the Server

    > uvicorn app.main:app --reload


## API Documentation
The API documentation is generated automatically. Once the server is running just enter the following in your browser:

    http://127.0.0.1:8000/docs
