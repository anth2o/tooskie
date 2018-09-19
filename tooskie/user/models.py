from django.utils.translation import ugettext_lazy as _
from django.db import models

from tooskie.abstract.models import BaseModel, NameModel

import logging
logger = logging.getLogger(__name__)
#TODO: set logging level as an environment variable

class User(NameModel):
    first_name = models.CharField(max_length=1000, verbose_name=_('First name'))
    last_name = models.CharField(max_length=1000, verbose_name=_('Full name'))
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name=_('Date of birth'))

    # Relations
    recipe = models.ManyToManyField('recipe.Recipe', through='recipe.RecipeSuggested', verbose_name=_('Recipes suggested'))
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
