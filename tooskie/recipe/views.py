from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tooskie.recipe.models import Ingredient
from tooskie.pantry.models import Pantry
from tooskie.pantry.generate_recipes import filter_recipes, get_ingredients, get_recipes
from tooskie.recipe.serializers import IngredientSerializerWithPicture, RecipeShortSerializer

import logging
from tooskie.constants import LOGGING_CONFIG

logging.basicConfig(**LOGGING_CONFIG)


@api_view(['GET'])
def all_ingredients(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializerWithPicture(ingredients, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def ingredient_by_id(request, id):
    try:
        ingredient = Ingredient.objects.get(id=id)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializerWithPicture(ingredient)
        return Response(serializer.data)

@api_view(['GET'])
def ingredient_by_permaname(request, permaname):
    try:
        ingredient = Ingredient.objects.get(permaname=permaname)
        print(ingredient.picture)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializerWithPicture(ingredient)
        return Response(serializer.data)

@api_view(['GET'])
def recipe_with_pantry(request, pantry_permaname):
    try:
        recipes = get_recipes()
        logging.debug('Number of recipes scanned: ' + str(len(recipes)))
        pantry = Pantry.objects.get(permaname=pantry_permaname)
        ingredients = get_ingredients(pantry)
        logging.debug('Ingredients in pantry: ' + str(len(ingredients)))
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            recipes = filter_recipes(recipe_list=recipes, ingredients=ingredients)
            logging.debug('Recipes filtered: ' + str(recipes))
            serializer = RecipeShortSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)