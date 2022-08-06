from django.contrib import admin

from app_recipes.models import Favorite
from app_recipes.models import Recipe
from app_recipes.models import RecipeIngredientRelations
from app_recipes.models import RecipeTag
from app_recipes.models import ShoppingCart


class RecipeIngredientRelationsInline(admin.TabularInline):
    model = RecipeIngredientRelations
    extra = 0
    verbose_name = model.ingredients.field.verbose_name
    verbose_name_plural = verbose_name + 'ы'


class RecipeTagRelationsInline(admin.TabularInline):
    model = RecipeTag
    extra = 0
    verbose_name = RecipeTag.tags.field.verbose_name
    verbose_name_plural = verbose_name + 'и'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientRelationsInline, RecipeTagRelationsInline)
    list_display = ('name', 'author', 'cooking_time')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class FavoriteShoppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    empty_value_display = '-пусто-'
