FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .
COPY app .

RUN pip3 install -r requirements.txt