from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from tooskie.user.models import BaseModel

class Recipe(BaseModel):
    name = models.CharField(max_length=1000, verbose_name=_('Name'))
    cooking_time = models.IntegerField(blank=True, null=True, verbose_name=_('Cooking time'))
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name=_('Preparation time'))


class RecipeSuggested(BaseModel):
    class Meta:
        verbose_name_plural = 'Recipes suggested'

    is_accepted = models.NullBooleanField(verbose_name=_('Recipe suggestion accepted'))
    rating = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name=_('Rating'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    
    # Relations

    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name=_('Suggested to user'))

# class CookedIt(BaseModel):
#     class Meta:
#         verbose_name_plural = 'Cooked it'

