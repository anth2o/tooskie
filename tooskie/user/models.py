from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from tooskie.abstract.models import BaseModel, NameModel
from tooskie.constants import LINK_WORD

class User(NameModel):
    first_name = models.CharField(max_length=1000, verbose_name=_('First name'))
    last_name = models.CharField(max_length=1000, verbose_name=_('Full name'))
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name=_('Date of birth'))

    # Relations
    recipe = models.ManyToManyField('recipe.Recipe', through='RecipeSuggested', verbose_name=_('Recipes suggested'))
    status = models.ForeignKey('Status', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Status'))

    def save(self, *args, **kwargs):
        self.name = self.first_name + ' ' + self.last_name
        try:
            super(User, self).save(*args, **kwargs)
        except Exception as e:
            raise e            

class Status(NameModel):
    class Meta:
        verbose_name_plural = 'Status'

class RecipeSuggested(BaseModel):
    class Meta:
        verbose_name_plural = 'Recipes suggested'

    is_accepted = models.NullBooleanField(verbose_name=_('Recipe suggestion accepted'))
    is_declined = models.NullBooleanField(verbose_name=_('Recipe suggestion declined'))
    # If the two previous bool are false, it means "not today"
    rating = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name=_('Rating'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    
    # Relations
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('Suggested to user'))

    def __str__(self):
        return str(self.recipe) + LINK_WORD + str(self.user) + LINK_WORD + str(self.created_at)

    def save(self, *args, **kwargs):
        if not self.is_accepted and self.rating:
            raise ValidationError("You can't post a rating if you declined the suggestion")
        super(RecipeSuggested, self).save(*args, **kwargs)

class Picture(BaseModel):
    picture = models.ImageField(verbose_name=_('Picture'))
    
    # Relations
    recipe_suggested = models.ForeignKey('RecipeSuggested', on_delete=models.CASCADE, verbose_name=_('Recipe suggested'))

    def __str__(self):
        return str(self.recipe_suggested)