import re

from rest_framework import serializers


class ValidateUser(object):
    def validate_username(self, username):
        """Валидация username"""
        text = 'Недопустимый username: '
        if username == 'me':
            raise serializers.ValidationError(text + username)
        if re.match(r'^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(text + username)
        return username


class ValidateFollow(object):
    def validate_following(self, following):
        if self.context['request'].user == following:
            raise serializers.ValidationError(
                'Подписка на самого себя запрещена!.')
        return following
