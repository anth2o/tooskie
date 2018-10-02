from rest_framework import serializers

from tooskie.recipe.models import Ingredient


class IngredientShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'picture'
        )


