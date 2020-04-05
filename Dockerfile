FROM python:3.7-alpine

WORKDIR /srv/app

ENV JAVA_HOME /usr
ENV PYTHONPATH /srv/app/src

COPY . .

RUN apk add -Uv \
  bash \
  openjdk9-jre-headless

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN chmod +x \
  /usr/local/lib/python3.7/site-packages/pyspark/bin/*
