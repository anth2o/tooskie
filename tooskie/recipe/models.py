from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from tooskie.abstract.models import BaseModel, NameModel

class Recipe(NameModel):
    name = models.CharField(max_length=1000, verbose_name=_('Name'))
    cooking_time = models.IntegerField(blank=True, null=True, verbose_name=_('Cooking time'))
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name=_('Preparation time'))
    
    # Relations
    level = models.ForeignKey('DifficultyLevel', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Difficulty level'))
    ustensil = models.ManyToManyField('Ustensil', through='UstensilInRecipe', verbose_name=_('Ustensil(s) used'))

class Step(BaseModel):
    step_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'))

    def __str__(self):
        return str(self.recipe) + '-' + str(self.step_number)

class DifficultyLevel(BaseModel):
    level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()

    def __str__(self):
        return str(self.level)

class Ustensil(NameModel):
    picture = models.ImageField(blank=True)

class UstensilInRecipe(BaseModel):
    quantity = models.PositiveIntegerField()

    # Relations
    ustensil = models.ForeignKey('Ustensil', on_delete=models.CASCADE, verbose_name=_('Ustensil'))
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'))

    def __str__(self):
        return str(self.ustensil) + '-in-' + str(self.recipe)

class Ingredient(NameModel):
    # average price in Euros
    average_price = models.PositiveIntegerField(blank=True, null=True)
    # average conservation time in hours
    conservation_time = models.PositiveIntegerField(blank=True, null=True)

class RecipeSuggested(BaseModel):
    class Meta:
        verbose_name_plural = 'Recipes suggested'

    is_accepted = models.NullBooleanField(verbose_name=_('Recipe suggestion accepted'))
    rating = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name=_('Rating'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    
    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name=_('Suggested to user'))

    def __str__(self):
        return str(self.recipe) + '-to-' + str(self.user) + '-' + str(self.created_at)

    def save(self, *args, **kwargs):
        if not self.is_accepted and self.rating:
            raise ValidationError("You can't post a rating if you declined the suggestion")
        super(RecipeSuggested, self).save(*args, **kwargs)

class Picture(BaseModel):
    picture = models.ImageField(verbose_name=_('Picture'))

    recipe_suggested = models.ForeignKey('RecipeSuggested', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))
