from drf_base64.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.mixins import AttributesForRecipe
from core.validaters import validate_tags
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredientRelations
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class RecipeIngredientRelationsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = RecipeIngredientRelations
        fields = ('id', 'name', 'measurement_unit', 'amount')


class SimpleRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(AttributesForRecipe, SimpleRecipeSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientRelationsSerializer(
        read_only=True, many=True, source='recipeingredientrelations')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_recipes(self, data):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = (data.recipes.all()[
                   :int(recipes_limit)] if recipes_limit else data.recipes)
        serializer = serializers.ListSerializer(child=RecipeSerializer())
        return serializer.to_representation(recipes)

    def create_ingredient_amount(self, valid_ingredients, recipe):
        for ingredient_data in valid_ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_data.get('id'))
            RecipeIngredientRelations.objects.create(
                recipe=recipe,
                ingredients=ingredient,
                amount=ingredient_data.get('amount'))

    def create_tags(self, data, recipe):
        valid_tags = validate_tags(data.get('tags'))
        tags = Tag.objects.filter(id__in=valid_tags)
        recipe.tags.set(tags)

    def create(self, validated_data):
        valid_ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(self.initial_data, recipe)
        self.create_ingredient_amount(valid_ingredients, recipe)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        data['ingredients'] = ingredients
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        instance.tags.remove()
        self.create_tags(self.initial_data, instance)
        instance.ingredientamount_set.filter(recipe__in=[instance.id]).delete()
        valid_ingredients = validated_data.get(
            'ingredients', instance.ingredients)
        self.create_ingredient_amount(valid_ingredients, instance)
        return instance
