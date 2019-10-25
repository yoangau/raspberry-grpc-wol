FROM python:alpine
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' SERVERPATH='/usr/src/app'
RUN apk update && apk upgrade
RUN apk add build-base
RUN pip install pycryptodome grpcio grpcio-tools RPi.GPIO
RUN apk add --no-cache bash