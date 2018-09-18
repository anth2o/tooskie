from django.utils.translation import ugettext_lazy as _
from django.db import models

import logging
logger = logging.getLogger(__name__)
#TODO: set logging level as an environment variable

class BaseModel(models.Model):
    permaname = models.SlugField(max_length=1000, unique=True, verbose_name=_('Permaname'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Last updated at'))

    class Meta:
        abstract = True
