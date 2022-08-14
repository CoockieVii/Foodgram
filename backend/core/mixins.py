from recipes import serializers
from recipes.models import (Favorite, Recipe, RecipeIngredientRelations,
                            RecipeTag, ShoppingCart)
from users.models import Subscription


class GetRecipesCount:
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()


class GetRecipe:
    def get_recipes(self, obj):
        request = self.context.get("request")
        if request.GET.get("recipe_limit"):
            recipe_limit = int(request.GET.get("recipe_limit"))
            queryset = Recipe.objects.filter(author=obj)[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(author_id=obj.id)
        serializer = serializers.SimpleRecipeSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data


class GetSubscribed:
    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author_id=obj, user_id=user
        ).exists()


class GetFavorites:
    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user_id=user.id, recipe_id=obj.id
        ).exists()


class GetIngradients:
    def get_ingradients(self, obj):
        return RecipeIngredientRelations.objects.filter(recipe_id=obj.id)


class GetTags:
    def get_tags(self, obj):
        return RecipeTag.objects.filter(recipe_id=obj.id)


class GetShoppingCart:
    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        return ShoppingCart.objects.filter(
            user_id=user.id, recipe_id=obj.id
        ).exists()


class AttributesForRecipe(GetRecipe, GetFavorites, GetShoppingCart):
    pass


class AttributesForUser(GetSubscribed):
    pass


class AttributesForSubscription(GetRecipe, GetSubscribed, GetRecipesCount):
    pass
