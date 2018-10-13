from rest_framework import serializers

from tooskie.recipe.models import Ingredient, Recipe, Step, IngredientInRecipe
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
    picture = serializers.URLField()
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

class StepSerializer(serializers.ModelSerializer):
    picture = serializers.URLField()

    class Meta:
        model = Step
        fields = (
            'step_number',
            'description',
            'picture'
        )

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_ingredient_name')
    name_plural = serializers.SerializerMethodField('get_ingredient_name_plural')

    unit = serializers.SerializerMethodField()
    unit_plural = serializers.SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = (
            'name',
            'name_plural',
            'complement',
            'complement_plural',
            'unit',
            'unit_plural',
            'quantity',
            'picture'
        )

    def get_ingredient_name(self, obj):
        return obj.unit_of_ingredient.ingredient.name

    def get_ingredient_name_plural(self, obj):
        return obj.unit_of_ingredient.ingredient.name_plural

    # def get_picture(self, obj):
    #     return obj.unit_of_ingredient.ingredient.picture

    def get_unit(self, obj):
        return obj.unit_of_ingredient.unit.name
    
    def get_unit_plural(self, obj):
        return obj.unit_of_ingredient.unit.name_plural

class RecipeSerializer(serializers.ModelSerializer):
    picture = serializers.URLField()
    tags = serializers.SerializerMethodField('get_tags_name')
    budget_level = serializers.SerializerMethodField('get_budget_level_name')
    difficulty_level = serializers.SerializerMethodField('get_difficulty_level_name')
    ustensils = serializers.SerializerMethodField('get_ustensils_name')

    def get_budget_level_name(self, obj):
        return obj.budget_level.name

    def get_difficulty_level_name(self, obj):
        return obj.difficulty_level.name

    def get_tags_name(self, obj):
        names = []
        for tag in obj.tag.all():
            names.append(tag.name)
        return names

    def get_ustensils_name(self, obj):
        names = []
        for ustensil in obj.ustensil.all():
            names.append(ustensil.name)
        return names
    
    steps = StepSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'name',
            'picture',
            'budget_level',
            'difficulty_level',
            'ustensils',
            'tags',
            'steps',
            'ingredients',
            'cooking_time',
            'preparation_time',
        )
