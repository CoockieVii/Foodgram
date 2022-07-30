from rest_framework import viewsets, status, permissions

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

