# Take-Home Assignment

This is a prototype for the CTW take-home assignment. 

It is implemented in Python 3.11 and integrated with a MySQL 8.0 database.


## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/lo/) - A modern, fast (high-performance), web framework for building APIs. 
I chose it because it is easy to learn, fast to code, and good for prototyping. 
- [Uvicorn](https://www.uvicorn.org/) - An ASGI web server implementation for Python.
- [Pydantic](https://docs.pydantic.dev/latest/) - Data validation library. It is used for validating query parameters.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM toolkit for SQL. It can help me handle the interaction with the DB, 
allowing me to focus on business logic.

## Directory structure:
```
g123_python_assignment/
├── .env.example
├── get_raw_data.py
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── financial/
      └── database.py
      └── main.py
      └── model.py
      └── repository.py
      └── schema.py
      └── service.py
      └── validator.py
```
- database.py: sets up the configuration for connecting to a MySQL database
- main.py: implements a FastAPI application
- model.py: defines an SQLAlchemy model for storing financial data
- repository.py: provides a repository for the CRUD of financial data
- schema.py: defines the `FinancialData` model class using the Pydantic for validation
- validator.py: defines the validators for validating query parameters

I think the `model.py` is part of the implementation of the financial data API service, so
I put it in the `financial` folder instead of the project root directory, 
which is a little different from the assignment examples.

### Migration
We can use [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations. 
Alembic is a lightweight database migration tool for SQLAlchemy 
that allows you to track and apply changes to your database schema.

## Usage
This project was tested successfully on 
- Ubuntu 18.04.4 LTS
- Docker version 20.10.14, build a224086
- docker-compose version 1.29.2, build 5becea4c

You can run it on your local environment by following these steps:


1. Get an API key from [AlphaVantage](https://www.alphavantage.co/documentation/)
2. Clone this repo, copy the `.env.example` and rename it to `.env` and put it in the same directory of `.env.example`.
Fill in the config variable in the `.env`:
```
ALPHAVANTAGE_APIKEY: The API KEY you got from AlphaVantage in step one
MYSQL_PASSWORD: any value you preferred
MYSQL_ROOT_PASSWORD: any value you preferred
HTTP_PORT: port number for http service, you can use any available port on your local environment.
HTTP_PROXY/HTTPS_PROXY: Optional. Fill in it if you are behind a proxy.
```
You can also change the `MYSQL_USERNAME` to any other value you preferred.


3. Run the command
   ```
   docker-compose up -d
   ```
4. If all goes well, the app is ready now.
```shell
developer@hostname:/g123$ docker-compose ps

    Name                   Command                  State                      Ports
----------------------------------------------------------------------------------------------------
financial_app   uvicorn financial.main:app ...   Up             0.0.0.0:8000->80/tcp,:::8000->80/tcp
financial_db    docker-entrypoint.sh mysqld      Up (healthy)   3306/tcp, 33060/tcp
```


5. Get into the app container and fetch stock data to the local database.
   ```
   developer@hostname:/g123$ docker exec -it financial_app /bin/bash
   root@842a6381139f:/code# python get_raw_data.py
   ```
6. If all goes well, data is ready now, you can send requests from the browser or `curl`. 
You can also find the auto-generated API documentation on `http://{domain}:{port}/docs`
7. You can use `docker-compose down` to stop and remove the service
