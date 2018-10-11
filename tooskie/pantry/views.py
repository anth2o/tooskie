from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from tooskie.pantry.models import Pantry
from tooskie.pantry.serializers import PantrySerializer, PantrySerializerWithIngredients, PantrySerializerWithIngredientsDetailed
from tooskie.recipe.serializers import IngredientSerializerWithPicture
from tooskie.helpers import get_sub_dict, remove_useless_spaces

from tooskie.constants import LOGGING_CONFIG

import logging
logging.basicConfig(**LOGGING_CONFIG)

@api_view(['GET', 'POST'])
def pantry(request):
    if request.method == 'GET':
        try:
            pantries = Pantry.objects.all()
            logging.debug(pantries)
            serializer = PantrySerializer(pantries, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            serializer = PantrySerializerWithIngredients(request.data)
            logging.debug(serializer.data)
            logging.debug(serializer.data['name'])
            pantry_model, created = Pantry.objects.get_or_create(name=serializer.data['name'])
            pantry_model.add_ingredients(serializer.data['ingredients'], pantry_model)
            return Response(PantrySerializer(pantry_model).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def pantry_by_permaname(request, permaname):
    if request.method == 'GET':
        try:
            ingredients = Pantry.objects.get(permaname=permaname).ingredients
            serializer = IngredientSerializerWithPicture(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

