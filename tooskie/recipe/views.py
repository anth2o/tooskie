from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tooskie.recipe.models import Ingredient, Recipe
from tooskie.pantry.models import Pantry
from tooskie.pantry.generate_recipes import filter_recipes, get_ingredients, get_recipes_pickle,save_recipes_pickle
from tooskie.recipe.serializers import IngredientSerializerWithPicture, RecipeShortSerializer, RecipeSerializer

import time

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
def recipe_with_pantry(request, permaname):
    # TODO: optimize filter recipes
    try:
        t0 = time.time()
        try:
            recipes = get_recipes_pickle()
        except:
            recipes = save_recipes_pickle()
        t1 = time.time()
        logging.debug('Get recipes execution time: ' + str(t1 - t0))
        logging.debug('Number of recipes scanned: ' + str(len(recipes)))
        pantry = Pantry.objects.get(permaname=permaname)
        ingredients = get_ingredients(pantry)
        t2 = time.time()
        logging.debug('Get ingredients execution time: ' + str(t2 - t1))
        logging.debug('Ingredients in pantry: ' + str(len(ingredients)))
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            recipes = filter_recipes(recipe_list=recipes, ingredients=ingredients)
            t3 = time.time()
            logging.debug('Filter recipes execution time: ' + str(t3 - t2))
            logging.debug('Recipes filtered: ' + str(recipes))
            # recipes = Recipe.objects.filter(id__lte=1035)
            serializer = RecipeShortSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def recipe(request, permaname):
    if request.method == 'GET':
        try:
            recipe = Recipe.objects.get(permaname=permaname)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)