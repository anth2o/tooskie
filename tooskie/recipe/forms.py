from django.forms.models import BaseInlineFormSet, inlineformset_factory, ModelForm, formset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Recipe, Step, UnitOfIngredient, IngredientInRecipe, Unit, Ingredient, NutritionalProperty, RecipeHasNutritionalProperty, Tag

import logging

logger = logging.getLogger("django")


RecipeStepsFormset = inlineformset_factory(
    Recipe,
    Step,
    fields=('description', 'time_start', 'picture'),
    extra=1,
    can_delete=True
)


class IngredientsForm(forms.Form):
    quantity = forms.FloatField(
        required=False, label=_('Quantity for one person'))
    unit = forms.ModelChoiceField(
        required=True, queryset=Unit.objects.order_by('name', 'name_fr'))
    ingredient = forms.ModelChoiceField(required=True, label=_(
        'Ingredient'), queryset=Ingredient.objects.order_by('name', 'name_fr'))

    def save(self, recipe, *args, **kwargs):
        logger.debug(self.cleaned_data)
        if not self.cleaned_data:
            return
        if self.cleaned_data['DELETE']:
            self.delete(recipe, *args, **kwargs)
            return
        unit_of_ingredient, created = UnitOfIngredient.objects.get_or_create(
            unit=self.cleaned_data['unit'], ingredient=self.cleaned_data['ingredient'])
        if created:
            unit_of_ingredient.save()
        ingredient_in_recipe, created = IngredientInRecipe.objects.get_or_create(
            unit_of_ingredient=unit_of_ingredient, recipe=recipe, quantity=self.cleaned_data['quantity'])
        if created:
            ingredient_in_recipe.save()

    def delete(self, recipe, *args, **kwargs):
        unit_of_ingredient, _ = UnitOfIngredient.objects.get_or_create(
            unit=self.cleaned_data['unit'], ingredient=self.cleaned_data['ingredient'])
        ingredient_in_recipe, ingredient_in_recipe_created = IngredientInRecipe.objects.get_or_create(
            unit_of_ingredient=unit_of_ingredient, recipe=recipe, quantity=self.cleaned_data['quantity'])
        if not ingredient_in_recipe_created:
            ingredient_in_recipe.delete()

IngredientsFormset = formset_factory(
    IngredientsForm,
    extra=1,
    can_delete=True
)


class NutritionalPropertiesForm(forms.Form):
    quantity = forms.FloatField(required=True, label=_('Amount for one person'))
    unit = forms.ModelChoiceField(required=True, queryset=Unit.objects.filter(
        for_nutritional_properties=True).order_by('name', 'name_fr'))
    nutritional_property = forms.ModelChoiceField(
        required=True, queryset=NutritionalProperty.objects.order_by('name', 'name_fr'))

    def save(self, recipe, *args, **kwargs):
        if not self.cleaned_data:
            return
        if self.cleaned_data['DELETE']:
            self.delete(recipe, *args, **kwargs)
            return
        recipe_has_nutritional_properties, created = RecipeHasNutritionalProperty.objects.get_or_create(
            recipe=recipe, nutritional_property=self.cleaned_data['nutritional_property'], unit_of_nutritional_property=self.cleaned_data['unit'], quantity=self.cleaned_data['quantity'])
        if created:
            recipe_has_nutritional_properties.save()
    
    def delete(self, recipe, *args, **kwargs):
        recipe_has_nutritional_properties, _ = RecipeHasNutritionalProperty.objects.get_or_create(
            recipe=recipe, nutritional_property=self.cleaned_data['nutritional_property'], unit_of_nutritional_property=self.cleaned_data['unit'], quantity=self.cleaned_data['quantity'])
        recipe_has_nutritional_properties.delete()

NutritionalPropertiesFormset = formset_factory(
    NutritionalPropertiesForm,
    extra=1,
    can_delete=True
)

class RecipeForm(forms.Form):
    recipe = forms.ModelChoiceField(required=True, queryset=Recipe.objects.order_by('name', 'name_fr'))

    def save(self, tag, *args, **kwargs):
        if not self.cleaned_data:
            return
        if self.cleaned_data['DELETE']:
            self.delete(tag, *args, **kwargs)
            return
        self.cleaned_data['recipe'].tag.add(tag)
    
    def delete(self, tag, *args, **kwargs):
        self.cleaned_data['recipe'].tag.remove(tag)

TagRecipesFormset = formset_factory(
    RecipeForm,
    extra=1,
    can_delete=True
)