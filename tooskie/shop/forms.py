from django.forms.models import BaseInlineFormSet, inlineformset_factory, ModelForm, formset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Product, Shop, ProductPrice
from tooskie.recipe.models import Unit, Ingredient, UnitOfIngredient

import logging

logger = logging.getLogger("django")


class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'picture', 'quantity']

    ingredient = forms.ModelChoiceField(required=True, queryset=Ingredient.objects.order_by('name', 'name_fr'), widget=forms.HiddenInput())
    quantity = forms.FloatField(required=True)
    unit = forms.ModelChoiceField(required=True, queryset=Unit.objects.order_by('name', 'name_fr'))

    def save(self, *args, **kwargs):
        if not self.cleaned_data:
            return
        logger.debug(self.cleaned_data)
        unit_of_ingredient, _ = UnitOfIngredient.objects.get_or_create(unit=self.cleaned_data['unit'], ingredient=self.cleaned_data['ingredient'])
        self.instance.unit_of_ingredient = unit_of_ingredient
        self.instance.save()

class ProductPriceModelForm(ModelForm):
    class Meta:
        model = ProductPrice
        fields = ['price',]

    shop = forms.ModelChoiceField(required=True, queryset=Shop.objects.order_by('name', 'name_fr'))

    def save(self, product, *args, **kwargs):
        if not self.cleaned_data:
            return
        product_price, _ = ProductPrice.objects.get_or_create(shop=self.cleaned_data['shop'], product=self.instance, price=self.cleaned_data['price'], quantity=self.cleaned_data['quantity'], unit_of_ingredient=product.unit_of_ingredient)

    
    def delete(self, tag, *args, **kwargs):
        self.cleaned_data['recipe'].tag.remove(tag)

ProductPriceFormset = formset_factory(
    ProductPriceModelForm,
    extra=1,
    can_delete=True
)

