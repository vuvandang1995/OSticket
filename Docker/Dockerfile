FROM ubuntu:16.04
MAINTAINER dangvv
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev nginx python3.5-dev libmysqlclient-dev redis-server
RUN pip3 install --upgrade pip
RUN pip install virtualenv
RUN mkdir /home/osticket
ADD ./osticket /home/osticket/
COPY ./gunicorn.service /etc/systemd/system/
COPY ./daphne.service /etc/systemd/system/
COPY ./redis.conf /etc/redis/
COPY ./default /etc/nginx/sites-available/