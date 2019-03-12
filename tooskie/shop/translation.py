from modeltranslation.translator import translator
from tooskie.utils.translation import NameDescriptionTranslationOptions, NameTranslationOptions
from .models import Brand, Shop, Product

translator.register(Shop, NameDescriptionTranslationOptions)
translator.register(Brand, NameDescriptionTranslationOptions)
translator.register(Product, NameTranslationOptions)
