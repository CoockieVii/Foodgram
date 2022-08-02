import re

from rest_framework import serializers, status

from app_users.models import Subscription


class ValidateUser(object):
    def validate_username(self, username):
        """Валидация username"""
        text = 'Недопустимый username: '
        if username == 'me':
            raise serializers.ValidationError(text + username)
        if re.match(r'^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(text + username)
        return username


def validate_subscription(author, user):
    if author == user:
        result = {'data': 'Нельзя подписываться на самого себя',
                  'status': status.HTTP_400_BAD_REQUEST}
        return result
    if Subscription.objects.filter(user=user, author=author).exists():
        result = {'data': 'Подписка уже оформлена',
                  'status': status.HTTP_400_BAD_REQUEST}
        return result
