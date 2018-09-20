from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


from tooskie.abstract.models import BaseModel, NameModel
from tooskie import choices
from tooskie.constants import *

class Recipe(NameModel):
    name = models.CharField(max_length=1000, verbose_name=_('Name'))
    cooking_time = models.IntegerField(blank=True, null=True, verbose_name=_('Cooking time'))
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name=_('Preparation time'))
    
    # Relations
    level = models.ForeignKey('DifficultyLevel', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Difficulty level'))
    ustensil = models.ManyToManyField('Ustensil', through='UstensilInRecipe', verbose_name=_('Ustensil(s) used'))
    measure_of_ingredient = models.ManyToManyField('MeasureOfIngredient', through='IngredientInRecipe', verbose_name=_('Ingredient(s) in recipe'))

class Step(BaseModel):
    step_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'))

    def __str__(self):
        return str(self.recipe) + LINK_WORD + str(self.step_number)

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
        return str(self.ustensil) + LINK_WORD + str(self.recipe)

class Ingredient(NameModel):
    # average conservation time in hours
    conservation_time = models.PositiveIntegerField(blank=True, null=True)

    # Relations
    measurement = models.ManyToManyField('Measurement', through='MeasureOfIngredient')
    special_diet = models.ManyToManyField('SpecialDiet', through='IngredientCompatbibleWithDiet')

class IngredientInRecipe(BaseModel):
    class Meta:
        verbose_name_plural = 'Ingredient in recipe'

    quantity = models.FloatField(blank=True, null=True)

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    measure_of_ingredient = models.ForeignKey('MeasureOfIngredient', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.measure_of_ingredient) + LINK_WORD + str(self.recipe)

class MeasureOfIngredient(BaseModel):
    average_price = models.FloatField(blank=True, null=True)

    # Relations
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ingredient) + LINK_WORD + str(self.measurement)

class Measurement(NameModel):
    unit = models.CharField(max_length=1000, choices=choices.unit_choices)

    def save(self, *args, **kwargs):
        self.permaname = slugify(self.name + LINK_WORD + self.unit)
        super(Measurement, self).save(*args, **kwargs)

class NutritionalProperty(NameModel):
    class Meta:
        verbose_name_plural = 'Nutritional Properties'

    description = models.TextField(blank=True)

class MeasureOfNutritionalProperty(BaseModel):
    class Meta:
        verbose_name_plural = 'Measure of nutritional properties'

    # Relations
    nutritional_property = models.ForeignKey('NutritionalProperty', on_delete=models.CASCADE)
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nutritional_property) + LINK_WORD + str(self.measurement)

class HasProperties(BaseModel):
    class Meta:
        verbose_name_plural = 'Has properties'

    nutritional_quantity = models.FloatField(blank=True, null=True, verbose_name=_('Nutritional quantity for one measure of ingredient'))

    # Relations
    measure_of_ingredient = models.ForeignKey('MeasureOfIngredient', on_delete=models.CASCADE, verbose_name=_('One measure of ingredient'))
    measure_of_nutritional_property = models.ForeignKey('MeasureOfNutritionalProperty', on_delete=models.CASCADE, verbose_name=_('The nutritional quantity in this measure'))

    def __str__(self):
        return str(self.measure_of_ingredient) + LINK_WORD + str(self.measure_of_nutritional_property)


class CanReplace(BaseModel):
    class Meta:
        verbose_name_plural = 'Can replace'

    score = models.FloatField(default=0, verbose_name=_('A score representing how well this ingredient can replace an other'))
    new_quantity = models.FloatField(blank=True, null=True, verbose_name=_('The quantity of the new ingredient'))

    # Relations
    new_measure_of_ingredient = models.ForeignKey('MeasureOfIngredient', on_delete=models.CASCADE)
    ingredient_in_recipe = models.ForeignKey('IngredientInRecipe', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.new_measure_of_ingredient) + '-replaces-' + str(self.ingredient_in_recipe)

class SpecialDiet(NameModel):
    description = models.TextField(blank=True)


class IngredientCompatbibleWithDiet(BaseModel):
    class Meta:
        verbose_name_plural = 'Ingredient compatible with diet'

    is_compatible = models.NullBooleanField()

    # Relations
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    special_diet = models.ForeignKey('SpecialDiet', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ingredient) + LINK_WORD + str(self.special_diet)