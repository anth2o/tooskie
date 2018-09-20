from django.contrib import admin
import tooskie.user.models as models
import sys, inspect

for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        try:
            admin.site.register(obj)
        # Exception if the model is abstract
        except:
            pass