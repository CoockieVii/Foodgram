from rest_framework import serializers

from app_core.validaters import ValidateUser, ValidateFollow
from .models import User, Subscription


class UserSerializer(ValidateUser, serializers.ModelSerializer):
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

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        author = obj
        return Subscription.objects.filter(user=user, author=author).exists()


class SubscriptionSerializer(ValidateFollow, serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'author')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author')
            )
        ]
