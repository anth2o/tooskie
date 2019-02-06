from rest_framework import serializers

from .models import Tag
from tooskie.recipe.serializers import RecipeWithoutTagsSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

        fields = (
            'name',
        )

class TagWithRecipesSerializer(serializers.ModelSerializer):
    picture = serializers.URLField()    
    recipes = RecipeWithoutTagsSerializer(many=True)

    class Meta:
        model = Tag

        fields = (
            'name',
            'picture',
            'recipes'
        )
