FROM python:3.8.12-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./

#RUN pip install --upgrade pip
# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt
