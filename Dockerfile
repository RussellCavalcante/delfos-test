FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH='/'

# COPY ./venv /
COPY ./requirements.txt /

RUN apt-get update -y && apt-get install curl -y \
&& pip install -r ./requirements.txt \
&& apt-get remove curl -y

COPY ./app /app
WORKDIR /app
