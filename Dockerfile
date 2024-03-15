FROM python:3.12.1-alpine
 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
 
ENV DB_USER=lordran_dev
ENV DB_PASSWORD=lordran_dev
ENV DB_HOST=localhost
ENV DB_PORT=5433
ENV DB_NAME=fastapi_db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]