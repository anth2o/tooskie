FROM python:3.6
ENV PYTHONUNBUFFERED 1

# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt
# ADD run_celery.sh /app/run_celery.sh
# ADD run_web.sh /app/run_web.sh

# set working directory to /app/
WORKDIR /app/

# install python dependencies
RUN pip install -r requirements.txt

# create unprivileged user

RUN adduser --disabled-password --gecos '' django_user


ADD . /app/