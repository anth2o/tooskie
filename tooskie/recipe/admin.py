from django.contrib import admin
from .models import Recipe, RecipeSuggested

admin.site.register(Recipe)
admin.site.register(RecipeSuggested)