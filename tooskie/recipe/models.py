from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from tooskie.utils.models import BaseModel, NameModel, LevelModel
from tooskie import choices
from tooskie.constants import LINK_WORD, LOGGING_CONFIG, NONE_UNIT

import logging
logging.basicConfig(**LOGGING_CONFIG)

class Recipe(NameModel):
    # time is in minutes
    cooking_time = models.IntegerField(blank=True, null=True, verbose_name=_('Cooking time'))
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name=_('Preparation time'))
    url = models.URLField(blank=True)
    picture = models.ImageField(blank=True, null=True)
    
    # Relations
    difficulty_level = models.ForeignKey('DifficultyLevel', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Difficulty level'))
    budget_level = models.ForeignKey('BudgetLevel', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Budget level'))
    ustensil = models.ManyToManyField('Ustensil', through='UstensilInRecipe', verbose_name=_('Ustensil(s) used'))
    unit_of_ingredient = models.ManyToManyField('UnitOfIngredient', through='IngredientInRecipe', verbose_name=_('Ingredient(s) in recipe'))
    tag = models.ManyToManyField('utils.Tag')

class Step(NameModel):
    name = models.CharField(max_length=1000, blank=True, unique=True, verbose_name=_('Name'))
    step_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()
    picture = models.ImageField(blank=True, null=True)

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'))

    def save(self, *args, **kwargs):
        self.name = self.recipe.name + ' ' + str(self.step_number)
        super(Step, self).save(*args, **kwargs)

class DifficultyLevel(LevelModel):
    pass

class BudgetLevel(LevelModel):
    pass

class Ustensil(NameModel):
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank=True)

class UstensilInRecipe(NameModel):
    name = models.CharField(max_length=1000, blank=True, unique=True, verbose_name=_('Name'))
    quantity = models.PositiveIntegerField(blank=True)

    # Relations
    ustensil = models.ForeignKey('Ustensil', on_delete=models.CASCADE, verbose_name=_('Ustensil'))
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'))

    def save(self, *args, **kwargs):
        self.name = self.ustensil.name + LINK_WORD + self.recipe.name.lower()
        super(UstensilInRecipe, self).save(*args, **kwargs)

class Ingredient(NameModel):
    # average conservation time in hours
    conservation_time = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Conservation time in hours'))
    picture = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=1000, verbose_name=_('Name'))
    name_plural = models.CharField(max_length=1000, blank=True)
    complement = models.CharField(max_length=1000, blank=True)
    complement_plural = models.CharField(max_length=1000, blank=True)

    # Relations
    unit = models.ManyToManyField('Unit', through='UnitOfIngredient')
    special_diet = models.ManyToManyField('SpecialDiet', through='IngredientCompatbibleWithDiet')
   
    def save(self, *args, **kwargs):
        if self.complement != '':
            self.permaname = slugify(self.name + ' ' + self.complement)
        else:
            self.permaname = slugify(self.name)
        super(Ingredient, self).save(*args, **kwargs)

class IngredientInRecipe(NameModel):
    class Meta:
        verbose_name_plural = 'Ingredient in recipe'

    quantity = models.FloatField(blank=True, null=True)

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    unit_of_ingredient = models.ForeignKey('UnitOfIngredient', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.unit_of_ingredient.name + LINK_WORD + self.recipe.name.lower()
        super(IngredientInRecipe, self).save(*args, **kwargs)

class UnitOfIngredient(NameModel):
    average_price = models.FloatField(blank=True, null=True, verbose_name=_('Average price for one unit'))
    linking_word = models.CharField(max_length=1000, blank=True)
    linking_word_plural = models.CharField(max_length=1000, blank=True)

    # Relations
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.ingredient.name + LINK_WORD + self.unit.name.lower()
        super(UnitOfIngredient, self).save(*args, **kwargs)

class Unit(NameModel):
    name_plural = models.CharField(max_length=1000, blank=True)

    def save(self, *args, **kwargs):
        if not self.name or self.name == '':
            self.name = NONE_UNIT
        if self.name_plural:
            self.name_plural = self.name_plural.capitalize()
        super(Unit, self).save(*args, **kwargs)

class NutritionalProperty(NameModel):
    class Meta:
        verbose_name_plural = 'Nutritional Properties'

    description = models.TextField(blank=True)

class UnitOfNutritionalProperty(NameModel):
    class Meta:
        verbose_name_plural = 'Unit of nutritional properties'

    # Relations
    nutritional_property = models.ForeignKey('NutritionalProperty', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name =  self.nutritional_property.name + LINK_WORD + self.unit.name.lower()
        super(UnitOfNutritionalProperty, self).save(*args, **kwargs)

class HasProperties(NameModel):
    class Meta:
        verbose_name_plural = 'Has properties'

    nutritional_quantity = models.FloatField(blank=True, null=True, verbose_name=_('Nutritional quantity for one unit of ingredient'))

    # Relations
    unit_of_ingredient = models.ForeignKey('UnitOfIngredient', on_delete=models.CASCADE, verbose_name=_('One unit of ingredient'))
    unit_of_nutritional_property = models.ForeignKey('UnitOfNutritionalProperty', on_delete=models.CASCADE, verbose_name=_('The nutritional quantity in this unit'))

    def save(self, *args, **kwargs):
        self.name =  self.unit_of_nutritional_property.name + LINK_WORD + self.unit_of_ingredient.name.lower()
        super(HasProperties, self).save(*args, **kwargs)


class CanReplace(NameModel):
    class Meta:
        verbose_name_plural = 'Can replace'

    score = models.FloatField(default=0, verbose_name=_('A score representing how well this ingredient can replace an other'))
    new_quantity = models.FloatField(blank=True, null=True, verbose_name=_('The quantity of the new ingredient'))

    # Relations
    new_unit_of_ingredient = models.ForeignKey('UnitOfIngredient', on_delete=models.CASCADE)
    ingredient_in_recipe = models.ForeignKey('IngredientInRecipe', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name =  self.new_unit_of_ingredient.name + ' can replace ' + self.ingredient_in_recipe.name.lower()
        super(CanReplace, self).save(*args, **kwargs)

class SpecialDiet(NameModel):
    description = models.TextField(blank=True)


class IngredientCompatbibleWithDiet(NameModel):
    class Meta:
        verbose_name_plural = 'Ingredient compatible with diet'

    is_compatible = models.NullBooleanField()

    # Relations
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    special_diet = models.ForeignKey('SpecialDiet', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name =  self.ingredient.name + ' is compatible with ' + self.special_diet.name.lower()
        super(IngredientCompatbibleWithDiet, self).save(*args, **kwargs)