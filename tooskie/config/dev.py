import os
from os.path import join
from tooskie.config.common import Common

class Dev(Common):
    DEBUG = True

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'rest_framework',
        'autoslug',
        
        'tooskie.recipe',
        'tooskie.user',
        'tooskie.utils',
        'tooskie.pantry',
        'tooskie.shop'
    ]

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'x4mjy^)4_!4v9bx1#vas9tgw%ds044d2@ht=a=z43m@*ae4ujb'

    ALLOWED_HOSTS = ['ec2-52-47-135-186.eu-west-3.compute.amazonaws.com']

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tooskie',
            'USER': 'tooskie',
            'PASSWORD': 'tooskie_DB_dev',
            'HOST': 'tooskie.c19qlgqvcgnf.eu-west-3.rds.amazonaws.com',
            'PORT': '5432',
        },
    }

    REST_FRAMEWORK = {

        'DEFAULT_RENDERER_CLASSES': (
            'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        ),

        'DEFAULT_PARSER_CLASSES': (
            'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        ),
    }

    MEDIA_ROOT = join(os.path.dirname(Common.BASE_DIR), 'media')
    MEDIA_URL = '/media/'
