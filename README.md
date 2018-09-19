# TOOSKIE

## Description

Tooskie was a project aiming to create an application capable of giving you ideas on what to cook depending on what's in your fridge.

## Launch the Django server on Docker

If you wanna try the latest version, make sure you're pulling dev branch.

```sh
docker-compose up
```

## Create a superuser

This is mandatory to access the django admin interface

```sh
docker exec -it tooskie_web_1 python manage.py createsuperuser
```

Follow the instructions

## Access the django admin

In your browser go to localhost/admin and enter your credentials

## Apply migrations

If you've just made a modifcation on the models, you need to apply those migrations

```sh
docker exec tooskie_web_1 python manage.py makemigrations

docker exec tooskie_web_1 python manage.py migrate
```
