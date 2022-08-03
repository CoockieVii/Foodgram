from django.contrib import admin

from app_recipes.models import Favorite
from app_recipes.models import Recipe
from app_recipes.models import RecipeIngredientRelations
from app_recipes.models import RecipeTagRelations


class RecipeIngredientRelationsInline(admin.TabularInline):
    model = RecipeIngredientRelations
    extra = 0


class RecipeTagRelationsInline(admin.TabularInline):
    model = RecipeTagRelations
    extra = 0


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
    search_fields = ('user',)
    empty_value_display = '-пусто-'
