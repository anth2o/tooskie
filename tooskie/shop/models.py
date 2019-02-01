from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from tooskie.utils.models import BaseModel, NameModel
from tooskie import choices
from tooskie.constants import LINK_WORD, LOGGING_CONFIG

import logging
logger = logging.getLogger("django")

class ShoppingList(NameModel):
    # Relations
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        super(ShoppingList, self).save(*args, **kwargs)

    def get_name(self):
        return self.user.name + str(self.created_at)

class IsInShoppingList(BaseModel):
    quantity = models.FloatField(blank=True, null=True)
    is_bought = models.BooleanField(default=False)
    quantity_bought = models.FloatField(blank=True, null=True)

    #Relations
    shopping_list = models.ForeignKey('ShoppingList', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('recipe.Ingredient', on_delete=models.CASCADE)
    unit = models.ForeignKey('recipe.Unit', on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient.name + LINK_WORD + self.shopping_list.name.lower()

    def save(self, *args, **kwargs):
        logger.debug(self.is_bought)
        logger.debug(self.quantity)
        logger.debug(self.quantity_bought)
        if self.is_bought and self.quantity_bought is None and self.quantity is not None:
            self.quantity_bought = self.quantity
        super(IsInShoppingList, self).save(*args, **kwargs)

class Brand(NameModel):
    description = models.TextField(blank=True)
    is_partner = models.NullBooleanField()

class Shop(NameModel):
    description = models.TextField(blank=True)
    is_partner = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Relations
    brand = models.ForeignKey('Brand', on_delete=models.DO_NOTHING, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.permaname = slugify(str(self.name) + '-lat-' + str(self.latitude) + '-lon-' + str(self.longitude))
        super(Shop, self).save(*args, **kwargs)


class IsInShop(BaseModel):
    price = models.FloatField(blank=True, null=True)

    # Relations
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    unit_of_ingredient = models.ForeignKey('recipe.UnitOfIngredient', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.unit_of_ingredient) + LINK_WORD + str(self.shop)