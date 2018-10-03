from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from autoslug import AutoSlugField

from tooskie.helpers import remove_useless_spaces
from tooskie.constants import LOGGING_LEVEL
from tooskie.choices import model_tagged_choices

import logging
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] : %(message)s', level=logging.getLevelName(LOGGING_LEVEL), datefmt='%d/%b/%Y %H:%M:%S')

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Last updated at'))
    
    class Meta:
        abstract = True

class NameModel(models.Model):
    name = models.CharField(max_length=1000, unique=True, verbose_name=_('Name'))
    permaname = AutoSlugField(always_update=False, populate_from='name')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Last updated at'))

    def __str__(self):
        return str(self.permaname)

    def save(self, *args, **kwargs):
        if self.name == '':
            raise ValidationError('This model must have a non-empty name')
        self.name = self.name.capitalize()
        self.name = remove_useless_spaces(self.name)
        logging.debug(self.name)
        try:
            super(NameModel, self).save(*args, **kwargs)
        except Exception as e:
            raise e

    class Meta:
        abstract = True

class LevelModel(NameModel):
    level = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

class Tag(NameModel):
    model_tagged = models.CharField(max_length=255, blank=True, choices=model_tagged_choices)
