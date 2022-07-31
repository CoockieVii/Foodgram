from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter


from app_users.views import UserViewSet, SubscriptionViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('', include('djoser.urls')),
    re_path('', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('users/<int:pk>/subscribe/', SubscriptionViewSet.as_view()),
    path('', include(router_v1.urls)),
]
