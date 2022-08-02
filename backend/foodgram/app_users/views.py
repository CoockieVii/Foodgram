from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app_core.validaters import validate_subscription
from .models import User, Subscription
from .serializers import UserSerializer, SubscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание подписок."""
        author_id = self.kwargs.get('users_id')
        author = get_object_or_404(User, id=author_id)
        validate = validate_subscription(author, request.user)
        if validate:
            return Response(data=validate['data'], status=validate['status'])
        if Subscription.objects.create(
                user=request.user,
                author=author):
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Удаление подписки."""
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        if get_object_or_404(
                Subscription,
                user__id=user_id,
                author__id=author_id).delete():
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return get_list_or_404(User, subscriber__user=self.request.user)
