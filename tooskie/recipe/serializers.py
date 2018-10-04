from rest_framework import serializers

from tooskie.recipe.models import Ingredient, Recipe
from tooskie.utils.serializers import TagSerializer



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

class RecipeShortSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField('get_tags_name')
    budget_level = serializers.SerializerMethodField('get_budget_level_name')
    difficulty_level = serializers.SerializerMethodField('get_difficulty_level_name')

    def get_budget_level_name(self, obj):
        return obj.budget_level.name

    def get_difficulty_level_name(self, obj):
        return obj.difficulty_level.name

    def get_tags_name(self, obj):
        names = []
        for tag in obj.tag.all():
            names.append(tag.name)
        return names

    class Meta:
        model = Recipe
        fields = (
            'name',
            'picture',
            'cooking_time',
            'preparation_time',
            'budget_level',
            'difficulty_level',
            'tag',
            'number_of_steps'
        )
