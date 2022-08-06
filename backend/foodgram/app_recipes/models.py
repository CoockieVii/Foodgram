from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from app_ingredients.models import Ingredient
from app_tags.models import Tag
from app_users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='recipe')
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredientRelations',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, through='RecipeTag',
                                  verbose_name='Теги',
                                  related_name='recipe')
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='recipes/image/')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(verbose_name='Время приготовления',
                                       validators=[MinValueValidator(1),
                                                   MaxValueValidator(99)])

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredientRelations(models.Model):
    ingredients = models.ForeignKey(Ingredient,
                                    on_delete=models.CASCADE,
                                    verbose_name='Ингредиент',
                                    related_name='recipeingredientrelations')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipeingredientrelations')
    amount = models.IntegerField(verbose_name='Количество выбора',
                                 default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredients'],
                                    name='unique_recipe_ingredients')]

    def __str__(self):
        return f'{self.ingredients}: {self.recipe}'


class RecipeTag(models.Model):
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE,
                             verbose_name='Тег',
                             related_name='recipetag')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipetag')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tags', 'recipe'],
                                    name='unique_recipetag')]

    def __str__(self):
        return f'{self.tags}: {self.recipe}'


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
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='unique_favorite')]

    def __str__(self):
        return f'{self.user}: {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shoppingcart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shoppingcart')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='unique_shoppingcart')]

    def __str__(self):
        return f'{self.user}: {self.recipe}'
