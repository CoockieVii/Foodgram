from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from app_ingredients.views import IngredientViewSet
from app_recipes.views import RecipeViewSet
from app_tags.views import TagsViewSet
from app_users.views import UserViewSet, SubscriptionViewSet

app_name = 'app_api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

auth_urls = [
    path('', include('djoser.urls')),
    re_path('', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('users/subscriptions/',
         SubscriptionViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<users_id>/subscribe/',
         SubscriptionViewSet.as_view({'post': 'create', 'delete': 'delete'}),
         name='subscribe'),
    path('', include(router_v1.urls)),
]
