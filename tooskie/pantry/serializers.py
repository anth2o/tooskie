from rest_framework import serializers

from tooskie.pantry.models import Pantry
from tooskie.recipe.serializers import IngredientSerializer, IngredientSerializerWithPicture

class PantrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pantry
        fields = (
            'id',
            'name'
        )

class PantrySerializerWithIngredients(serializers.ModelSerializer):
    ingredients = serializers.ListField(child=serializers.CharField())
        
    class Meta:
        model = Pantry
        fields = (
            'permaname',
            'name',
            'ingredients'
        )

class PantrySerializerWithIngredientsDetailed(serializers.ModelSerializer):
    ingredients = IngredientSerializerWithPicture(many=True)
        
    class Meta:
        model = Pantry
        fields = (
            'permaname',
            'name',
            'ingredients'
        )
