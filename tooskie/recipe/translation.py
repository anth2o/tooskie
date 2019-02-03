from modeltranslation.translator import translator
from tooskie.utils.translation import NameTranslationOptions, NamePluralTranslationOptions, NamePluralDescriptionTranslationOptions, NameDescriptionTranslationOptions
from .models import Recipe, BudgetLevel, DifficultyLevel, Ingredient, NutritionalProperty, SpecialDiet, Step, Unit, Ustensil

translator.register(Recipe, NameTranslationOptions)
translator.register(BudgetLevel, NameDescriptionTranslationOptions)
translator.register(DifficultyLevel, NameDescriptionTranslationOptions)
translator.register(Ingredient, NamePluralTranslationOptions)
translator.register(NutritionalProperty, NameDescriptionTranslationOptions)
translator.register(SpecialDiet, NameDescriptionTranslationOptions)
translator.register(Step, NameTranslationOptions)
translator.register(Unit, NamePluralTranslationOptions)
translator.register(Ustensil, NamePluralDescriptionTranslationOptions)
