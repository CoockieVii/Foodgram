import re
from rest_framework import serializers, status
from rest_framework.response import Response

from tags.models import Tag
from users.models import Subscription


class ValidateUser(object):
    def validate_username(self, username):
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


class ValidateTags(object):
    def validate_slug(self, slug):
        text = ' -содержит недопустимые символы.'
        if re.match(r'^[-a-zA-Z0-9_]+$', slug) is None:
            raise serializers.ValidationError(slug + text)


def validate_tags(data):
    """Валидация тэгов: отсутствие в request, отсутствие в БД."""
    if not data:
        raise Response({'tags': ['Обязательное поле.']})
    if len(data) < 1:
        raise Response({'tags': ['Хотя бы один тэг должен быть указан.']})
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise Response({'tags': ['Тэг отсутствует в БД.']})
    return data
