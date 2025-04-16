# Description: Dockerfile for ForgettingWeb.
FROM python:3.11-slim-buster

# gcc compiler and opencv prerequisites
# RUN apt-get update && apt-get upgrade 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_DEBUG=1

COPY ForgettingWeb ForgettingWeb
COPY Procfile Procfile
# WORKDIR ForgettingWeb/visualisation

CMD gunicorn --bind 0.0.0.0:8000 ForgettingWeb.visualisation.app:server