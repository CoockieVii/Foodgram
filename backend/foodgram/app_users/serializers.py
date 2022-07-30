from rest_framework import serializers

from app_core.mixin import ValidateMixin
from .models import User


class UserSerializer(ValidateMixin, serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password')
        model = User
