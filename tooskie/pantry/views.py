from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from tooskie.pantry.models import Pantry
from tooskie.pantry.serializers import PantrySerializer, PantrySerializerWithIngredients
from tooskie.helpers import get_sub_dict, remove_useless_spaces

from tooskie.constants import LOGGING_CONFIG

import logging
logging.basicConfig(**LOGGING_CONFIG)

@api_view(['POST'])
def pantry(request):
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
