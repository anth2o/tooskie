from django.contrib import admin
import tooskie.utils.models as models
import sys, inspect

from tooskie.constants import LOGGING_CONFIG
import logging
logging.basicConfig(**LOGGING_CONFIG)

for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        try:
            admin.site.register(obj)
        # Exception if the model is abstract
        except:
            pass