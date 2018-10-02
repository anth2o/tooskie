from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tooskie.pantry.models import Pantry
from tooskie.pantry.serializers import PantrySerializer, PantrySerializerWithIngredients


@api_view(['POST'])
def pantry(request):
    if request.method == 'POST':
        serializer = PantrySerializerWithIngredients(request.data)
        pantry_model, created = Pantry.objects.get_or_create(name=serializer.data['name'])
        print(created)
        print(pantry_model)
        pantry_model.add_ingredients(serializer.data['ingredients'])
        return Response(PantrySerializer(pantry).data)
