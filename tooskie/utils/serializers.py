from rest_framework import serializers

from tooskie.utils.models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

        fields = (
            'name',
        )
