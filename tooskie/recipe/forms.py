from django.forms.models import BaseInlineFormSet, inlineformset_factory, ModelForm
from django import forms
from .models import Recipe, Step, UnitOfIngredient, IngredientInRecipe




RecipeStepsFormset = inlineformset_factory(
                                Recipe,
                                Step,
                                fields=('description', 'time_start', 'picture'),
                                extra=1,
                                can_delete=False
                            )
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time')
