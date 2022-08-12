from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters
from rest_framework import filters as rf_filters

from recipes.models import Recipe
from tags.models import Tag
from users.models import User


class CustomSearchFilter(rf_filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(field_name='tags__slug',
                                     to_field_name='slug',
                                     queryset=Tag.objects.all())
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_is_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user__id=self.request.user.id)
        return queryset

    def get_is_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoppingcart__user__id=self.request.user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
