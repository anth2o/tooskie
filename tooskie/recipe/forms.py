from django import forms
from .models import Recipe

class RecipeForm(forms.Form):
    name = forms.CharField(label='Recipe name', max_length=100)
    
    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time',)