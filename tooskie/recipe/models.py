from django.utils.translation import ugettext_lazy as _
from django.db import models
from tooskie.user.models import BaseModel

class Recipe(BaseModel):
    name = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Name'))
    cooking_time = models.IntegerField(null=True, blank=True, verbose_name=_('Cooking time'))
    preparation_time = models.IntegerField(null=True, blank=True, verbose_name=_('Preparation time'))
