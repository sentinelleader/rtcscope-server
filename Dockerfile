From debian:jessie

MAINTAINER rtcscope <rtcscope@rtcscope.io>

EXPOSE 8000

RUN apt-get update

RUN apt-get -y install supervisor wget

RUN wget http://influxdb.s3.amazonaws.com/influxdb_0.9.1_amd64.deb -O /tmp/influxdb_0.9.1_amd64.deb

RUN dpkg -i /tmp/influxdb_0.9.1_amd64.deb

COPY config/influxdb.conf /etc/opt/influxdb/influxdb.conf

RUN mkdir -p /opt/rtcscope-server/static

COPY app.py /opt/rtcscope-server/

COPY static /opt/rtcscope-server/static/

COPY config/supervisor/influxdb.conf /etc/supervisor/conf.d/

COPY config/supervisor/rtcscope-server.conf /etc/supervisor/conf.d/

RUN apt-get -y install python-pip

RUN pip install flask

RUN pip install influxdb

RUN apt-get clean

CMD ["/usr/bin/supervisord", "-n"]
