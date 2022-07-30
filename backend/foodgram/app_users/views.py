from rest_framework import viewsets, filters, mixins
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserSerializer, FollowSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    """Подписки."""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=user__username', '=author__username')

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
