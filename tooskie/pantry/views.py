from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.text import slugify

from tooskie.pantry.models import Pantry
from tooskie.pantry.serializers import PantrySerializer, PantrySerializerWithIngredients
from tooskie.helpers import get_or_create_then_save,get_sub_dict, remove_useless_spaces

@api_view(['POST'])
def pantry(request):
    if request.method == 'POST':
        request.data['name'] = request.data['name'].capitalize()
        serializer = PantrySerializerWithIngredients(request.data)
        pantry_model, created = get_or_create_then_save(Pantry, get_sub_dict(serializer.data, ['name']))
        print(created)
        print(pantry_model)
        pantry_model.add_ingredients(serializer.data['ingredients'])
        return Response(PantrySerializer(pantry).data)
