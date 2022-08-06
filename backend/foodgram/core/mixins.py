from recipes.models import (ShoppingCart, RecipeTag, Favorite, Recipe,
                            RecipeIngredientRelations)
from users.models import Subscription
from recipes import serializers


class GetRecipesCount:
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()


class GetRecipe:
    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            queryset = Recipe.objects.filter(
                author=obj)[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(
                author=obj)
        serializer = serializers.SimpleRecipeSerializer(
            queryset, read_only=True, many=True)
        return serializer.data


class GetSubscribed:
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and Subscription.objects.filter(
            author=obj, user=user).exists()


class GetFavorites:
    def get_is_favorited(self, obj):
        user_id = self.context.get('request').user.id
        return Favorite.objects.filter(user=user_id, recipe=obj.id).exists()


class GetIngradients:
    def get_ingradients(self, obj):
        return RecipeIngredientRelations.objects.filter(recipe=obj)


class GetTags:
    def get_tags(self, obj):
        return RecipeTag.objects.filter(recipe=obj)


class GetShoppingCart:
    def get_is_in_shopping_cart(self, obj):
        user_id = self.context.get('request').user.id
        return ShoppingCart.objects.filter(
            user=user_id, recipe=obj.id).exists()


class AttributesForRecipe(GetFavorites, GetShoppingCart):
    pass


class AttributesForUser(GetSubscribed):
    pass


class AttributesForSubscription(GetRecipe, GetSubscribed, GetRecipesCount):
    pass
