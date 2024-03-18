# FastAPI MVC

For REST FastAPI go to 'rest' branch

## Stack used :

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" height=80 /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" height=80 /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" height=90/>

## Project with

1. Connection to Postgres
1. JWT for authentication and authorization
1. Alembic for DB migrations

## Running the project

### Dev mode

1. Install dependencies
```
pip install --no-cache-dir --upgrade -r requirements.txt
```

2. Run docker compose
Here we initialize the Postgres image with a pgAdmin GUI
```
docker compose up
```

3. Run uvicorn server
Here we start our uvicorn server in port 8000
```
uvicorn app.main:app --reload
```

### Production mode

1. Build docker image
```
docker build -t fastapi-initialization .
```

2. Pull image
```
docker pull fastapi-initialization
```

3. Run image
```
docker run -e DB_HOST=your_db_host -e DB_USER=your_db_user -e DB_PASSWORD=your_db_pass -e DB_NAME=your_db_name -e DB_PORT=your_db_port -p 80:80 fastapi-initialization
```

## Steps for a new migration

1. Install alembic
```
pip install alembic
```

2. Alembic revision
Here we add the DB updates
```
alembic revision -m "<message>"
```

3. Alembic upgrade
Here we add the DB updates
```
alembic upgrade <revision id>
```

4. Alembic downgrade
Here we add the DB updates
```
alembic downgrade -1
```