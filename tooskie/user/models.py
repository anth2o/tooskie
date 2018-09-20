from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from tooskie.utils.models import BaseModel, NameModel
from tooskie.constants import LINK_WORD

class User(NameModel):
    first_name = models.CharField(max_length=1000, verbose_name=_('First name'))
    last_name = models.CharField(max_length=1000, verbose_name=_('Full name'))
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name=_('Date of birth'))

    # Relations
    recipe = models.ManyToManyField('recipe.Recipe', through='RecipeSuggested', verbose_name=_('Recipes suggested'))
    status = models.ForeignKey('Status', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Status'))
    playlist = models.ManyToManyField('Playlist', through='CanAccessPlaylist')
    social_media = models.ManyToManyField('SocialMedia', through='IsConnectedTo')

    def save(self, *args, **kwargs):
        self.name = self.first_name + ' ' + self.last_name
        try:
            super(User, self).save(*args, **kwargs)
        except Exception as e:
            raise e            

class Status(NameModel):
    description = models.TextField(blank=True)

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

class ReplacedIngredient(BaseModel):
    proportion_replaced = models.FloatField(blank=True, null=True, verbose_name=_('Proportion of original ingredient replaced'))

    # Relations
    # Check that the recipe in "can_replace" is the same than the recipe in "recipe_suggested"
    recipe_suggested = models.ForeignKey('RecipeSuggested', on_delete=models.CASCADE, verbose_name=_('Recipe cooked'))
    can_replace = models.ForeignKey('recipe.CanReplace', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.can_replace) + LINK_WORD + str(self.recipe_suggested)

class Playlist(NameModel):
    is_public = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)

    # Relations
    recipe = models.ManyToManyField('recipe.Recipe', through='IsInPlaylist', verbose_name=_('Recipes in playlist'))

class CanAccessPlaylist(BaseModel):
    is_owner = models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
    
    # Relations
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + LINK_WORD + str(self.playlist)

class IsInPlaylist(BaseModel):
    rank = models.PositiveIntegerField(blank=True, null=True)

    # Relations
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.playlist) + LINK_WORD + str(self.recipe)

class SocialMedia(NameModel):
    is_available = models.BooleanField(default=False)
    description = models.TextField(blank=True)

class IsConnectedTo(BaseModel):
    token = models.CharField(max_length=1000, blank=True, verbose_name=_('Token to access social media'))

    # Relations
    social_media = models.ForeignKey('SocialMedia', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)