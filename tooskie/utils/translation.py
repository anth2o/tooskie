from modeltranslation.translator import TranslationOptions, translator
from .models import Tag

class NameTranslationOptions(TranslationOptions):
    fields = ('name',)

class NameDescriptionTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class NamePluralTranslationOptions(TranslationOptions):
    fields = ('name', 'name_plural')

class NamePluralDescriptionTranslationOptions(TranslationOptions):
    fields = ('name', 'name_plural', 'description')

class DescriptionTranslationOptions(TranslationOptions):
    fields = ('description', )

class ComplementTranslationOptions(TranslationOptions):
    fields = ('complement', 'complement_plural', )

translator.register(Tag, NameDescriptionTranslationOptions)