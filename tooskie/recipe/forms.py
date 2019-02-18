from django.forms.models import BaseInlineFormSet, inlineformset_factory, ModelForm, formset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Recipe, Step, UnitOfIngredient, IngredientInRecipe, Unit, Ingredient

import logging

logger = logging.getLogger("django")


RecipeStepsFormset = inlineformset_factory(
                                Recipe,
                                Step,
                                fields=('description', 'time_start', 'picture'),
                                extra=1,
                                can_delete=False
                            )

class IngredientsForm(forms.Form):
    quantity = forms.IntegerField(required=False, label=_('Quantity for one person'))
    unit = forms.ModelChoiceField(required=True, queryset=Unit.objects.order_by('name', 'name_fr'))
    ingredient = forms.ModelChoiceField(required=True, label=_('Ingredient'), queryset=Ingredient.objects.order_by('name', 'name_fr'))

    def save(self, recipe, *args, **kwargs):
        unit_of_ingredient, created = UnitOfIngredient.objects.get_or_create(unit=self.cleaned_data['unit'], ingredient=self.cleaned_data['ingredient'])
        if created:
            unit_of_ingredient.save()
        ingredient_in_recipe, created = IngredientInRecipe.objects.get_or_create(unit_of_ingredient=unit_of_ingredient, recipe=recipe, quantity=self.cleaned_data['quantity'])
        if created:
            ingredient_in_recipe.save() 
        
IngredientsFormset = formset_factory(
                                IngredientsForm,
                                extra=1,
                                can_delete=False
                            )

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time')
