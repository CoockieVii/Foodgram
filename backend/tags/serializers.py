from rest_framework import serializers

from core.validaters import ValidateTags
from tags.models import Tag


class TagSerializer(ValidateTags, serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
