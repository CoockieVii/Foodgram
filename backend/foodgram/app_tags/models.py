from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=200)
    color = ColorField('Цвет тега', max_length=7, format="hex")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}: {self.slug}'
