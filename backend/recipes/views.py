from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.filters import RecipeFilter
from core.permissions import IsOwnerOrReadOnly
from core.utils import download
from core.validaters import ValidateTags
from recipes.models import (Favorite, Recipe, RecipeIngredientRelations,
                            ShoppingCart)
from recipes.serializers import RecipeSerializer, SimpleRecipeSerializer


def custom_adder(model, user, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if not model.objects.filter(user=user, recipe=recipe).exists():
        model.objects.create(user=user, recipe=recipe)
        serializer = SimpleRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Запись уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST)


def custom_deleter(model, user, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    model = model.objects.filter(user=user, recipe=recipe)
    if model.exists():
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Запись уже была удалена.'},
                    status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(ValidateTags, viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True, url_path='favorite',
            url_name='favorite')
    def favorite(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            return custom_adder(Favorite, user, pk)
        if request.method == 'DELETE':
            return custom_deleter(Favorite, user, pk)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post', 'delete'], detail=True, url_path='shopping_cart',
            url_name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            return custom_adder(ShoppingCart, user, pk)
        if request.method == 'DELETE':
            return custom_deleter(ShoppingCart, user, pk)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_cart(self, request):
        ingredients = RecipeIngredientRelations.objects.filter(
            recipe__shoppingcart__user_id=request.user.id
        ).values('ingredients__name', 'ingredients__measurement_unit'
                 ).order_by('ingredients__name'
                            ).annotate(ingredient_total=Sum('amount'))
        return download(ingredients)
