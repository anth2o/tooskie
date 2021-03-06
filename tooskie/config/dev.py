import os
from os.path import join
from tooskie.config.common import Common

class Dev(Common):
    DEBUG = True

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'x4mjy^)4_!4v9bx1#vas9tgw%ds044d2@ht=a=z43m@*ae4ujb'

    ALLOWED_HOSTS = ['ec2-35-180-98-224.eu-west-3.compute.amazonaws.com']

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tooskie_dev',
            'USER': 'tooskie',
            'PASSWORD': 'tooskie_DB_dev',
            'HOST': 'tooskie-dev.c19qlgqvcgnf.eu-west-3.rds.amazonaws.com',
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

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[{asctime}] [{levelname}] : {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'logs/dev.log',
                'formatter': 'default'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'logs/error.log',
                'formatter': 'default'
            },
            'null': {
                'level': 'DEBUG',
                'class':'logging.NullHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'console', 'error'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['null'],  # Quiet by default!
                'propagate': False,
                'level':'DEBUG',
            },
            'django.template': {
                'handlers': ['null'],  # Quiet by default!
                'propagate': False,
                'level':'DEBUG',
            }
        }
    }
