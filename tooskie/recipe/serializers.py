from rest_framework import serializers

from tooskie.recipe.models import Ingredient, Recipe, Step, IngredientInRecipe, Tag

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
             'name_plural',
            'picture'
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
    picture = serializers.URLField()

    unit = serializers.SerializerMethodField()
    unit_plural = serializers.SerializerMethodField()

    linking_word = serializers.SerializerMethodField()
    linking_word_plural = serializers.SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = (
            'name',
            'name_plural',
            'complement',
            'complement_plural',
            'unit',
            'unit_plural',
            'linking_word',
            'linking_word_plural',
            'quantity',
            'picture'
        )

    def get_ingredient_name(self, obj):
        return obj.unit_of_ingredient.ingredient.name

    def get_ingredient_name_plural(self, obj):
        return obj.unit_of_ingredient.ingredient.name_plural

    def get_unit(self, obj):
        return obj.unit_of_ingredient.unit.name
    
    def get_unit_plural(self, obj):
        return obj.unit_of_ingredient.unit.name_plural

    def get_linking_word(self, obj):
        return obj.unit_of_ingredient.linking_word
    
    def get_linking_word_plural(self, obj):
        return obj.unit_of_ingredient.linking_word_plural

class RecipeWithoutTagsSerializer(serializers.ModelSerializer):
    picture = serializers.URLField()
    budget_level = serializers.SerializerMethodField('get_budget_level_name')
    difficulty_level = serializers.SerializerMethodField('get_difficulty_level_name')
    ustensils = serializers.SerializerMethodField('get_ustensils_name')

    def get_budget_level_name(self, obj):
        return obj.budget_level.name

    def get_difficulty_level_name(self, obj):
        return obj.difficulty_level.name

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
            'steps',
            'ingredients',
            'cooking_time',
            'preparation_time',
        )

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

