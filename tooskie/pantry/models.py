import logging

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from tooskie.constants import LINK_WORD
from tooskie.helpers import get_or_create
from tooskie.recipe.models import Ingredient, Unit, UnitOfIngredient
from tooskie.utils.models import BaseModel, NameModel

logger = logging.getLogger(__name__)


class Pantry(NameModel):
    class Meta:
        verbose_name_plural = 'Pantries'

    has_freezer = models.NullBooleanField()
    has_fridge = models.NullBooleanField()
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)

    # Relations
    shopping_list = models.ManyToManyField(
        'shop.ShoppingList', through='Receipt')

    @property
    def ingredients(self):
        ingredients = []
        for ingredient_in_pantry in self.ingredients_in_pantry.all():
            ingredients.append(
                ingredient_in_pantry.unit_of_ingredient.ingredient)
        return ingredients

    def add_ingredients(self, ingredients, pantry):
        # ingredients is a list of dict as :
        #     "ingredients": [
        #        {
        #            "id": 1,
        #            "name": "Poulet",
        #        },
        #        ...
        #    ]
        default_unit_model, _ = Unit.objects.get_or_create(permaname='default')
        default_unit_model.name = 'Default'
        default_unit_model.save()
        for current_ingredient in self.ingredients:
            was_present = False
            for new_ingredient in ingredients:
                if current_ingredient.name == new_ingredient["name"]:
                    was_present = True
                    break
            if not was_present:
                current_ingredient.delete()
                logger.debug("Deleting " + str(current_ingredient) + " from pantry " + str(self.permaname))
                
        for ingredient in ingredients:
            try:
                ingredient_model = Ingredient.objects.get(
                    permaname=slugify(ingredient))
            except Exception:
                raise ValueError(ingredient + " isn't a valid ingredient")
            default_ingredient_unit_model, _ = UnitOfIngredient.objects.get_or_create(
                unit=default_unit_model, ingredient=ingredient_model)
            IngredientInPantry.objects.get_or_create(
                unit_of_ingredient=default_ingredient_unit_model, pantry=pantry)


class IngredientInPantry(NameModel):
    quantity = models.FloatField(blank=True, null=True)

    # Relations
    pantry = models.ForeignKey(
        'Pantry', on_delete=models.CASCADE, related_name='ingredients_in_pantry')
    unit_of_ingredient = models.ForeignKey(
        'recipe.UnitOfIngredient', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.unit_of_ingredient.name + LINK_WORD + self.pantry.name.lower()
        super(IngredientInPantry, self).save(*args, **kwargs)


class UstensilInPantry(BaseModel):
    quantity = models.FloatField(blank=True, null=True)

    # Relations
    pantry = models.ForeignKey('Pantry', on_delete=models.CASCADE)
    ustensil = models.ForeignKey('recipe.Ustensil', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ustensil) + LINK_WORD + str(self.pantry)


class Receipt(BaseModel):
    # There is no picture if the pantry is filled manually
    picture = models.ImageField(blank=True, null=True)

    # Relations
    pantry = models.ForeignKey('Pantry', on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(
        'shop.ShoppingList', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.pantry) + LINK_WORD + str(self.shopping_list)


class PayReceipt(BaseModel):
    coeff = models.FloatField(default=1)

    # Relations
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
