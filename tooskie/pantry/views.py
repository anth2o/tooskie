from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.text import slugify

from tooskie.pantry.models import Pantry
from tooskie.pantry.serializers import PantrySerializer, PantrySerializerWithIngredients
from tooskie.helpers import get_or_create,get_sub_dict, remove_useless_spaces

from tooskie.constants import LOGGING_CONFIG

import logging
logging.basicConfig(**LOGGING_CONFIG)

@api_view(['POST'])
def pantry(request):
    if request.method == 'POST':
        serializer = PantrySerializerWithIngredients(request.data)
        logging.debug(serializer.data)
        pantry_model, created = Pantry.objects.get_or_create(permaname=slugify(serializer.data['name']))
        pantry_model.name = serializer.data['name']
        pantry_model.save()
        pantry_model.add_ingredients(serializer.data['ingredients'], pantry_model)
        return Response(PantrySerializer(pantry).data)
