# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1

ENV USERNAME=app \
    GROUPNAME=app \
    APP_HOME=/home/app/code/

RUN groupadd -r $USERNAME && \
    useradd -g $GROUPNAME -r $USERNAME && \
    mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt

COPY . $APP_HOME
RUN chown -R $USERNAME:$GROUPNAME $APP_HOME
USER $USERNAME
