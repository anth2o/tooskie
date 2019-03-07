from django.forms.models import BaseInlineFormSet, inlineformset_factory, ModelForm, formset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Product, Shop
from tooskie.recipe.models import Unit, Ingredient, UnitOfIngredient

import logging

logger = logging.getLogger("django")


class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name']

    price = forms.FloatField(required=True)
    ingredient = forms.ModelChoiceField(required=True, queryset=Ingredient.objects.order_by('name', 'name_fr'))
    unit = forms.ModelChoiceField(required=True, queryset=Unit.objects.order_by('name', 'name_fr'))
    shop = forms.ModelChoiceField(required=True, queryset=Shop.objects.order_by('name', 'name_fr'))

    def save(self, *args, **kwargs):
        if not self.cleaned_data:
            return
        logger.debug(self.cleaned_data)
        self.instance.difficulty_level = self.cleaned_data['difficulty_level']
        self.instance.budget_level = self.cleaned_data['budget_level']
        self.instance.save()
        for tag in self.cleaned_data['tags']:
            logger.debug(tag)
            self.instance.tag.add(tag)
        logger.debug(self.instance)
