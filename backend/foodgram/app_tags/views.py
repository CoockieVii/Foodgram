from rest_framework.permissions import AllowAny
from rest_framework import mixins, viewsets

from app_tags.models import Tag
from app_tags.serializers import TagSerializer


class TagsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None
