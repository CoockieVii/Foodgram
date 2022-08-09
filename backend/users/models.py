from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Адрес электронной почты', unique=True)
    username = models.CharField('Юзернейм', max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    password = models.CharField('Пароль', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    created = models.DateTimeField('Дата подписки',
                                   auto_now_add=True,
                                   db_index=True)
    user = models.ForeignKey(User, verbose_name='Подписчик',
                             on_delete=models.CASCADE,
                             related_name='subscriber',
                             blank=False)
    author = models.ForeignKey(User, verbose_name='Отслеживаемый автор',
                               on_delete=models.CASCADE,
                               related_name='author',
                               blank=False)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписки пользователей'
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscription')]

    def clean(self):
        if self.user == self.author:
            raise ValueError('Нельзя подписываться на самого себя.')
