# FastAPI introduction

## Stack used :

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" height=80 /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" height=80 /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" height=90/>

## Project with

1. Connection to Postgres
1. JWT for authentication and authorization
1. Alembic for DB migrations

## Steps for a new migration

1. Install alembic
```
pip install alembic
```

1. Alembic revision
Here we add the DB updates
```
alembic revision -m "<message>"
```

1. Alembic upgrade
Here we add the DB updates
```
alembic upgrade <revision id>
```

1. Alembic downgrade
Here we add the DB updates
```
alembic downgrade -1
```