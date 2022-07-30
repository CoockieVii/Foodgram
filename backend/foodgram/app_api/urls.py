
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from app_users.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

urlpatterns = [
    # path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
