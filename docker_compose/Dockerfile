FROM python:3
MAINTAINER dangvv
ENV PYTHONUNBUFFERD 1
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/
RUN mkdir /home/osticket
WORKDIR /home/osticket
ADD requirements.txt /home/osticket/
RUN pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]
