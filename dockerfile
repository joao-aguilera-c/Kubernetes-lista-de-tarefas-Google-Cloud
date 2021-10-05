FROM python:alpine

RUN mkdir -p /app
WORKDIR /app

COPY ./src/requirements.txt /app/requirements.txt

RUN apk add build-base


RUN pip install -r requirements.txt

COPY ./src/ /app/
ENV FLASK_APP=app.py

CMD flask run -h 0.0.0.0 -p 8080