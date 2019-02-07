from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import Recipe, Step

RecipeForm = modelformset_factory(Recipe, fields=('name', 'cooking_time',))
StepFormset = inlineformset_factory(Recipe, Step, fields=('name', 'description', ), extra=1)
