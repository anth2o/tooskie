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
    picture = serializers.SerializerMethodField()
    recipes = RecipeWithoutTagsSerializer(many=True)

    def get_picture(self, tag):
        request = self.context.get('request')
        return request.build_absolute_uri(tag.picture.url)

    class Meta:
        model = Tag

        fields = (
            'name',
            'picture',
            'recipes'
        )
