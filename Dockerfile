# syntax=docker/dockerfile:1
FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

ENV USERNAME=app \
    GROUPNAME=app \
    APP_HOME=/home/app/code/

RUN adduser -D $USERNAME && \
    mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 psycopg2-binary \
    && apk del build-deps

COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt

COPY . $APP_HOME
RUN chown -R $USERNAME:$GROUPNAME $APP_HOME
USER $USERNAME

CMD gunicorn webdocs.wsgi:application --bind 0.0.0.0:$PORT

