from rest_framework import serializers

from tooskie.recipe.models import Ingredient



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
        )

class IngredientSerializerWithPicture(serializers.ModelSerializer):
    picture = serializers.URLField()
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'picture'
        )


