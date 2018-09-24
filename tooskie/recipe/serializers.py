from rest_framework import serializers

from tooskie.recipe.models import Recipe, Ingredient

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe


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


