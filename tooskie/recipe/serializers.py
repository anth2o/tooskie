from rest_framework import serializers

from tooskie.recipe.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'name_plural',
            'complement',
            'complement_plural',
            'picture'
        )


