from django.contrib import admin
import tooskie.recipe.models as models
import sys, inspect


class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tag', )

admin.site.register(models.Recipe, RecipeAdmin)

for name, obj in inspect.getmembers(models):
    if inspect.isclass(obj):
        try:
            admin.site.register(obj)
        # Exception if the model is abstract
        except:
            pass

