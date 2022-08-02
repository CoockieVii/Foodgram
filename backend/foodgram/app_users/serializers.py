from rest_framework import serializers

from app_core.mixins import AttributesForUser, AttributesForSubscription
from app_core.validaters import ValidateUser
from .models import User


class UserSerializer(ValidateUser, AttributesForUser, serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SubscriptionSerializer(AttributesForSubscription,
                             serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    # recipes_count = serializers.SerializerMethodField()
    # recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',
                  # 'recipes', 'recipes_count'
                  )
