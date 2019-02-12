from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from autoslug import AutoSlugField

from tooskie.helpers import remove_useless_spaces
from tooskie.constants import LOGGING_CONFIG

import logging
logger = logging.getLogger("django")

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Last updated at'))
    
    class Meta:
        abstract = True

class NameModel(models.Model):
    name = models.CharField(max_length=1000, verbose_name=_('Name'), unique=True)
    permaname = AutoSlugField(always_update=True, populate_from='name', unique=True, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Last updated at'))

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.name == '':
            raise ValidationError('This model must have a non-empty name')
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

