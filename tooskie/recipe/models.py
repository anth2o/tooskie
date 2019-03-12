import logging

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from tooskie.constants import LINK_WORD, LOGGING_CONFIG, NONE_UNIT
from tooskie.helpers import remove_useless_spaces
from tooskie.utils.models import LevelModel, NameModel, PictureModel

logger = logging.getLogger("django")

class Recipe(NameModel, PictureModel):
    # time is in minutes
    cooking_time = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Cooking time (min.)'))
    preparation_time = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Preparation time (min.)'))
    url = models.URLField(blank=True)
    to_display = models.BooleanField(default=False)

    # Relations
    difficulty_level = models.ForeignKey('DifficultyLevel', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Difficulty level'))
    budget_level = models.ForeignKey('BudgetLevel', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Budget level'))
    ustensil = models.ManyToManyField('Ustensil', through='UstensilInRecipe', verbose_name=_('Ustensil(s) used'))
    unit_of_ingredient = models.ManyToManyField('UnitOfIngredient', through='IngredientInRecipe', verbose_name=_('Ingredient(s) in recipe'))
    tag = models.ManyToManyField('Tag', blank=True, related_name="recipes_not_filtered")

    def get_absolute_url(self):
        return reverse('recipe:recipe_detail', kwargs={'pk': self.pk})

    @property
    def tag_displayed(self):
        return self.tag.filter(to_display=True)
        
class Tag(NameModel, PictureModel):
    class Meta:
        ordering = ['name', 'name_fr']
        
    to_display = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    @property
    def recipes(self):
        return self.recipes_not_filtered.filter(to_display=True)
    
    def get_absolute_url(self):
        return reverse('recipe:tag_detail', kwargs={'pk': self.pk})

class Step(NameModel, PictureModel):
    class Meta:
        ordering = ['recipe', 'step_number']
    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    step_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()
    time_start = models.IntegerField(blank=True, null=True, verbose_name=_('Time start of the step (min.)'))

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='steps', verbose_name=_('Recipe'))

    def save(self, *args, **kwargs):
        if self.step_number is None:
            steps = Step.objects.filter(recipe=self.recipe).order_by('-step_number')
            if len(steps) == 0:
                self.step_number = 1
            else:
                self.step_number = steps[0].step_number + 1
        self.name = self.get_name()
        super(Step, self).save(*args, **kwargs)

    def get_name(self):
        return self.recipe.name + ' step ' + str(self.step_number)

class DifficultyLevel(LevelModel):
    class Meta:
        ordering = ['level',]
    pass

class BudgetLevel(LevelModel):
    class Meta:
        ordering = ['level',]
    pass

class Ustensil(NameModel, PictureModel):
    name_plural = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)

class UstensilInRecipe(NameModel):
    class Meta:
        verbose_name_plural = 'Ustensils in recipe'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    quantity = models.PositiveIntegerField(blank=True)

    # Relations
    ustensil = models.ForeignKey('Ustensil', on_delete=models.CASCADE, verbose_name=_('Ustensil'))
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe'), related_name='ustensil_in_recipe')

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        super(UstensilInRecipe, self).save(*args, **kwargs)

    def get_name(self):
        return self.ustensil.name + LINK_WORD + self.recipe.name.lower()

class Ingredient(NameModel, PictureModel):
    # average conservation time in hours
    conservation_time = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Conservation time in hours'))
    name_plural = models.CharField(max_length=1000, blank=True)

    # Relations
    special_diet = models.ManyToManyField('SpecialDiet', through='IngredientCompatbibleWithDiet')

    @property
    def has_products(self):
        print('has products')
        for unit_of_ingredient in self.unit_of_ingredient.all():
            if len(unit_of_ingredient.product.all()) > 0:
                return True
        return False

    def get_absolute_url(self):
        return reverse('recipe:ingredient_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name_plural = remove_useless_spaces(self.name_plural)
        super(Ingredient, self).save(*args, **kwargs)

class IngredientInRecipe(NameModel):
    # Is through M2M Recipe - UnitOfIngredient
    class Meta:
        verbose_name_plural = 'Ingredients in recipe'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    quantity = models.FloatField(blank=True, null=True)
    complement = models.CharField(max_length=1000, blank=True)
    complement_plural = models.CharField(max_length=1000, blank=True)
    is_essential = models.BooleanField(default=True)

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredients')
    unit_of_ingredient = models.ForeignKey('UnitOfIngredient', on_delete=models.CASCADE, related_name='in_recipe')

    @property
    def picture(self):
        return self.unit_of_ingredient.ingredient.absolute_picture

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        self.complement = remove_useless_spaces(self.complement)
        self.complement_plural = remove_useless_spaces(self.complement_plural)
        super(IngredientInRecipe, self).save(*args, **kwargs)

    def get_name(self):
        pref = ''
        if self.quantity is not None:
            pref = str(self.quantity) + ' '
        return  pref + self.unit_of_ingredient.name.lower() + LINK_WORD + self.recipe.name.lower()

class UnitOfIngredient(NameModel):
    class Meta:
        verbose_name_plural = 'Unit of ingredients'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    average_price = models.FloatField(blank=True, null=True, verbose_name=_('Average price for one unit'))
    linking_word = models.CharField(max_length=1000, blank=True)
    linking_word_plural = models.CharField(max_length=1000, blank=True)
    is_indivisible = models.BooleanField(default=False)

    # Relations
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name="unit_of_ingredient")
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name="unit_of_ingredient")
    product = models.ManyToManyField('shop.Product', through='shop.QuantityInProduct')

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        super(UnitOfIngredient, self).save(*args, **kwargs)

    def get_name(self):
        pref = ''
        pref2 = ''
        if self.unit.name.lower() != 'none':
            pref = self.unit.name.lower() + ' '
        if self.linking_word != '':
            pref2 = self.linking_word + ' '
        return pref + pref2 + self.ingredient.name.lower()

class UnitOfIngredientHasNutrionalProperty(NameModel):
    class Meta:
        verbose_name_plural = 'Unit of ingredients has nutritional properties'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    quantity_of_nutritional_property =  models.FloatField(blank=True, null=True)

    # Relations
    unit_of_ingredient = models.ForeignKey('UnitOfIngredient', on_delete=models.CASCADE)
    nutritional_property = models.ForeignKey('NutritionalProperty', on_delete=models.CASCADE)
    unit_of_nutritional_property = models.ForeignKey('Unit', on_delete=models.CASCADE)

class RecipeHasNutritionalProperty(NameModel):
    class Meta:
        verbose_name_plural = 'Recipes has nutritional properties'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    quantity = models.PositiveIntegerField()

    # Relations
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='nutritional_properties')
    nutritional_property = models.ForeignKey('NutritionalProperty', on_delete=models.CASCADE)
    unit_of_nutritional_property = models.ForeignKey('Unit', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        super(RecipeHasNutritionalProperty, self).save(*args, **kwargs)

    def get_name(self):
        return str(self.quantity) + ' ' + str(self.unit_of_nutritional_property) + ' of ' + str(self.nutritional_property) + LINK_WORD + str(self.recipe)

class Unit(NameModel):
    name_plural = models.CharField(max_length=1000, blank=True)
    for_nutritional_properties = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (not self.name or self.name == ''):
            if not self.permaname or self.permaname == '':
                self.name = NONE_UNIT
            else:
                self.name = self.permaname.capitalize()
        super(Unit, self).save(*args, **kwargs)

class NutritionalProperty(NameModel):
    class Meta:
        verbose_name_plural = 'Nutritional Properties'

    description = models.TextField(blank=True)

class CanReplace(NameModel):
    class Meta:
        verbose_name_plural = 'Can replace'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    score = models.FloatField(default=0, verbose_name=_('A score representing how well this ingredient can replace an other'))
    new_quantity = models.FloatField(blank=True, null=True, verbose_name=_('The quantity of the new ingredient'))

    # Relations
    new_ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    unit_of_new_ingredient = models.ForeignKey('Unit', on_delete=models.CASCADE)
    ingredient_in_recipe = models.ForeignKey('IngredientInRecipe', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        super(CanReplace, self).save(*args, **kwargs)

    def get_name(self):
        return self.new_ingredient.name + LINK_WORD + self.unit_of_new_ingredient.name.lower() + ' can replace ' + self.ingredient_in_recipe.name.lower()

class SpecialDiet(NameModel):
    description = models.TextField(blank=True)

class IngredientCompatbibleWithDiet(NameModel):
    class Meta:
        verbose_name_plural = 'Ingredients compatible with diet'

    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'), blank=True)
    is_compatible = models.NullBooleanField()

    # Relations
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    special_diet = models.ForeignKey('SpecialDiet', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.get_name()
        super(IngredientCompatbibleWithDiet, self).save(*args, **kwargs)

    def get_name(self):
        temp = ''
        if not self.is_compatible:
            temp = 'not'
        return self.ingredient.name + ' is {} compatible with '.format(temp) + self.special_diet.name.lower()
