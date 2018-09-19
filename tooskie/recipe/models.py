from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from tooskie.user.models import BaseModel

class Recipe(BaseModel):
    name = models.CharField(max_length=1000, verbose_name=_('Name'))
    cooking_time = models.IntegerField(blank=True, null=True, verbose_name=_('Cooking time'))
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name=_('Preparation time'))
    
    # Relations
    level = models.ForeignKey('DifficultyLevel', on_delete=models.CASCADE, verbose_name=_('Difficulty level'))

class Step(BaseModel):
    step_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'))

class DifficultyLevel(BaseModel):
    level = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()

class RecipeSuggested(BaseModel):
    class Meta:
        verbose_name_plural = 'Recipes suggested'

    is_accepted = models.NullBooleanField(verbose_name=_('Recipe suggestion accepted'))
    rating = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name=_('Rating'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    
    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name=_('Suggested to user'))

class Picture(BaseModel):
    picture = models.ImageField(verbose_name=_('Picture'))

    recipe_suggested = models.ForeignKey('RecipeSuggested', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))
