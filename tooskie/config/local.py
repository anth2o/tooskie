import os
from os.path import join
from tooskie.config.common import Common

class Local(Common):
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

    ALLOWED_HOSTS = []

    # Database
    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tooskie',
            'USER': 'tooskie',
            'PASSWORD': 'tooskie',
            'HOST': 'db',
            'PORT': '',
        },
    }

    LOGGING = Common.LOGGING
    LOGGING['loggers'] = {
            'django': {
                'handlers': ['console'],
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
