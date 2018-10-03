from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


from tooskie.utils.models import BaseModel, NameModel
from tooskie.recipe.models import Ingredient, UnitOfIngredient, Unit
from tooskie import choices
from tooskie.constants import LINK_WORD
from tooskie.helpers import get_or_create


class Pantry(NameModel):
    class Meta:
        verbose_name_plural = 'Pantries'

    has_freezer = models.NullBooleanField()
    has_fridge = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Relations
    shopping_list = models.ManyToManyField('shop.ShoppingList', through='Receipt')

    def add_ingredients(self, ingredients, pantry):
        # ingredients is a list of dict as :
        #     "ingredients": [
        #        {
        #            "id": 1,
        #            "name": "Poulet",
        #        },
        #        ...
        #    ]
        default_unit_model = Unit.objects.get_or_create(permaname='default')
        default_unit_model.name = 'Default'
        default_unit_model.save()
        for ingredient in ingredients:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            default_ingredient_unit_model = UnitOfIngredient.objects.get_or_create(slugify(ingredient['name'] + LINK_WORD + 'default'))
            default_ingredient_unit_model.unit = default_unit_model
            default_ingredient_unit_model.ingredient = ingredient_model
            default_ingredient_unit_model.save()
            ingredient_in_pantry_model = IngredientInPantry.get_or_create(slugify(default_ingredient_unit_model.permaname + LINK_WORD + pantry.permaname))
            ingredient_in_pantry_model.unit_of_ingredient = default_ingredient_unit_model
            ingredient_in_pantry_model.pantry = pantry
            ingredient_in_pantry_model.save()

class IngredientInPantry(NameModel):
    quantity = models.FloatField(blank=True, null=True)

    # Relations
    pantry = models.ForeignKey('Pantry', on_delete=models.CASCADE)
    unit_of_ingredient = models.ForeignKey('recipe.UnitOfIngredient', on_delete=models.CASCADE)

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
    shopping_list = models.ForeignKey('shop.ShoppingList', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.pantry) + LINK_WORD + str(self.shopping_list)

class PayReceipt(BaseModel):
    coeff = models.FloatField(default=1)

    # Relations
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
