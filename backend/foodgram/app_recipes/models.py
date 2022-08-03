from django.db import models

from app_ingredients.models import Ingredient
from app_tags.models import Tag
from app_users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='recipe')
    name = models.CharField(max_length=200)
    ingredient = models.ManyToManyField(Ingredient,
                                        through='RecipeIngredientRelations',
                                        verbose_name='Ингредиенты')
    tag = models.ManyToManyField(Tag,
                                 through='RecipeTagRelations',
                                 verbose_name='Теги',
                                 related_name='recipe')
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='image/recipes/')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}: {self.ingredient}'


class RecipeIngredientRelations(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиенты',
                                   related_name='recipeingredientrelations')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipeingredientrelations')
    amount = models.IntegerField(verbose_name='Количество выбора',
                                 default=1)

    def __str__(self):
        return f'{self.ingredient}: {self.recipe}'


class RecipeTagRelations(models.Model):
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name='Тег',
                            related_name='recipetagrelations')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipetagrelations')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tag', 'recipe'],
                                    name='unique_recipetagrelations')]

    def __str__(self):
        return f'{self.tag}: {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorite')

    class Meta:
        verbose_name = 'Избранные'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user}: {self.recipe}'
