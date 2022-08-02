from django.db import models
from colorfield.fields import ColorField


# Create your models here.
class Tags(models.Model):
    name = models.CharField('Название тега', max_length=200)
    color = ColorField('Цвет тега', max_length=7, format="hex",
                       default='#FF0000')
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug
