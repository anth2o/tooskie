from tooskie.config.common import Common

class Local(Common):
    DEBUG = True

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'tooskie.recipe',
        'tooskie.user',
        'tooskie.utils'
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

    MEDIA_ROOT = './media/'