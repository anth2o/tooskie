from django.contrib import admin
import tooskie.recipe.models as models
import sys, inspect

for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        try:
            admin.site.register(obj)
        except Exception as e:
            print(e)