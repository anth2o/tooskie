FROM python:3.6

ENV PYTHONUNBUFFERED 1

# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt

# set working directory to /app/
WORKDIR /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /app

RUN mkdir /app/logs || true
