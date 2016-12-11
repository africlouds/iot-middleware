FROM resin/raspberrypi-python:2.7
#FROM python:2.7

MAINTAINER Africlouds Ltd <arwema@africlouds.com>

RUN apt-get update \
&& pip install flask requests\
&& pip install flask-httpauth\
&& pip install simplejson\
&& pip install flask-jsonpify\
&& pip install Flask-SQLAlchemy


EXPOSE 5000


ADD . /src
WORKDIR /src
CMD python app.py
