from django.utils.translation import ugettext_lazy as _
from django.db import models

import logging
logger = logging.getLogger(__name__)
#TODO: set logging level as an environment variable

class BaseModel(models.Model):
    permaname = models.SlugField(max_length=1000, unique=True, verbose_name=_('Permaname'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Last updated at'))

    def __str__(self):
        return str(self.permaname)

    class Meta:
        abstract = True

class User(BaseModel):
    first_name = models.CharField(max_length=1000, verbose_name=_('First name'))
    full_name = models.CharField(max_length=1000, verbose_name=_('Full name'))
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name=_('Date of birth'))

    # Relations

    recipe_id = models.ManyToManyField('recipe.Recipe', through='recipe.RecipeSuggested', verbose_name=_('Recipes suggested'))

