from rest_framework import serializers
from app_core.mixins import AttributesForUser, AttributesForSubscription
from app_core.validaters import ValidateUser
from djoser.serializers import UserCreateSerializer

from .models import User


class CreateUserSerializer(UserCreateSerializer, ValidateUser):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class UserSerializer(AttributesForUser, serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class SubscriptionSerializer(AttributesForSubscription,
                             serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

