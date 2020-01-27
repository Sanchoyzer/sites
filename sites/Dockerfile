FROM python:3.7-alpine

RUN mkdir /srv/src
WORKDIR /srv/src

ADD manage.py /srv/src/
ADD requirements.txt /srv/src/
ADD sites/* /srv/src/sites/
ADD geobot/* /srv/src/geobot/

RUN \
 pip install --upgrade pip setuptools && \
 pip install -r requirements.txt

EXPOSE 12345
