from modeltranslation.translator import translator
from tooskie.utils.translation import NameDescriptionTranslationOptions, DescriptionTranslationOptions
from .models import Playlist, SocialMedia, Status

translator.register(Playlist, NameDescriptionTranslationOptions)
translator.register(SocialMedia, DescriptionTranslationOptions)
translator.register(Status, NameDescriptionTranslationOptions)

