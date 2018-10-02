from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tooskie.recipe.models import Ingredient
from tooskie.recipe.serializers import IngredientShortSerializer


@api_view(['GET'])
def all_ingredients(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientShortSerializer(ingredients, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def ingredient(request, permaname):
    try:
        ingredient = Ingredient.objects.get(permaname=permaname)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientShortSerializer(ingredient)
        return Response(serializer.data)