from rest_framework import serializers

from app_core.validaters import ValidateTags
from app_tags.models import Tag


class TagSerializer(ValidateTags, serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
