from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


from tooskie.utils.models import BaseModel, NameModel
from tooskie import choices
from tooskie.constants import LINK_WORD


class Pantry(NameModel):
    has_freezer = models.NullBooleanField()
    has_fridge = models.NullBooleanField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

class IngredientInPantry(BaseModel):
    quantity = models.FloatField(blank=True, null=True)

    # Relations
    pantry = models.ForeignKey('Pantry', on_delete=models.CASCADE)
    measure_of_ingredient = models.ForeignKey('recipe.MeasureOfIngredient', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.measure_of_ingredient) + LINK_WORD + str(self.pantry)

