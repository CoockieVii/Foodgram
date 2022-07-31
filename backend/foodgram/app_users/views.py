from rest_framework import viewsets, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import User, Subscription
from .serializers import UserSerializer, SubscriptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriptionViewSet(views.APIView):
    """Подписки пользователей"""

    def get(self, request, pk):
        """Просмотр подписок пользователя."""
        author = get_object_or_404(User, id=pk)
        follows_author = author.subscriber.all()
        serializer = SubscriptionSerializer(follows_author, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Создание подписок."""
        user = self.request.user
        author = get_object_or_404(User, id=pk)
        data = {'user': user.id, 'author': author.id}
        serializer = SubscriptionSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Удаление подписки."""
        author = get_object_or_404(User, id=pk)
        get_object_or_404(Subscription,
                          user=self.request.user,
                          author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
