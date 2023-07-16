FROM alpine:latest
MAINTAINER tonylehnert.de

ENV PYTHONUNBUFFERED=1

#Install perequisites
RUN apk add --no-cache socat python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

#Install Python modules
#we do this because of AttributeError module 'serial' has no attribute 'Serial'
RUN pip --no-cache-dir --disable-pip-version-check uninstall serial pyserial
RUN pip --no-cache-dir --disable-pip-version-check install pyserial requests paho-mqtt pyMeterBus

#Set cronjob for pollucom.py, needs to run at least once an hour
RUN crontab -l | { cat; echo "*/55    *       *       *       *       /usr/bin/python3 /usr/sbin/pollucom.py"; } | crontab -

COPY pollucom.py /usr/sbin/

CMD tail -f /dev/null