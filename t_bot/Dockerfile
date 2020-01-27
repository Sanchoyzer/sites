FROM python:3.7-alpine

RUN mkdir /srv/src
WORKDIR /srv/src

ADD __init__.py /srv/src/
ADD .env /srv/src/
ADD requirements.txt /srv/src/
ADD main.py /srv/src/
ADD controller.py /srv/src/
ADD cert/* /srv/src/cert/

RUN \
 pip install --upgrade pip setuptools && \
 pip install -r requirements.txt

EXPOSE 443

# ENTRYPOINT ["python3", "main.py"]
