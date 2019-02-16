from django.forms.models import BaseInlineFormSet, inlineformset_factory

from .models import Recipe, Step

RecipeSteps = inlineformset_factory(
                                Recipe,
                                Step,
                                fields=('description',),
                                extra=1,
                                can_delete=False
                            )