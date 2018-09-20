from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


from tooskie.utils.models import BaseModel, NameModel
from tooskie import choices
from tooskie.constants import LINK_WORD

class ShoppingList(BaseModel):
    # Relations
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.user)) + LINK_WORD + str(self.created_at)

class IsInShoppingList(BaseModel):
    quantity = models.FloatField(blank=True, null=True)

    #Relations
    shopping_list = models.ForeignKey('ShoppingList', on_delete=models.CASCADE)
    measure_of_ingredient = models.ForeignKey('recipe.MeasureOfIngredient', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.measure_of_ingredient) + LINK_WORD + str(self.shopping_list)

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
    measure_of_ingredient = models.ForeignKey('recipe.MeasureOfIngredient', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.measure_of_ingredient) + LINK_WORD + str(self.shop)