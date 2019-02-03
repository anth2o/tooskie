from modeltranslation.translator import translator
from tooskie.utils.translation import NameDescriptionTranslationOptions
from .models import Brand, Shop

translator.register(Shop, NameDescriptionTranslationOptions)
translator.register(Brand, NameDescriptionTranslationOptions)
