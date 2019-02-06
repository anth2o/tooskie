from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tag
from .serializers import TagWithRecipesSerializer

import logging
from tooskie.constants import LOGGING_CONFIG

logger = logging.getLogger("django")

@api_view(['GET'])
def all_tags(request):
    if request.method == 'GET':
        try:
            tags = Tag.objects.filter(to_display=True)
            serializer = TagWithRecipesSerializer(tags, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)