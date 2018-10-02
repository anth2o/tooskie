from rest_framework import serializers

from tooskie.pantry.models import Pantry
from tooskie.recipe.serializers import IngredientSerializer

class PantrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pantry
        fields = (
            'id',
            'name'
        )

class PantrySerializerWithIngredients(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model = Pantry
        fields = (
            'name',
            'ingredients'
        )



