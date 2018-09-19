from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

import logging
logger = logging.getLogger(__name__)
#TODO: set logging level as an environment variable

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Last updated at'))

    class Meta:
        abstract = True

class NameModel(models.Model):
    permaname = models.SlugField(max_length=1000, unique=True, blank=True, verbose_name=_('Permaname'))
    name = models.CharField(max_length=1000, blank=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Last updated at'))

    def __str__(self):
        return str(self.permaname)

    def save(self, *args, **kwargs):
        if self.name == '':
            raise ValidationError('This model must have a non-empty name')
        if self.permaname == '':
            self.permaname = slugify(self.name)
        try:
            super(NameModel, self).save(*args, **kwargs)
        except Exception as e:
            raise e

    class Meta:
        abstract = True
