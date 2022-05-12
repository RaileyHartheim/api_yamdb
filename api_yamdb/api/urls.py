from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, SignUpViewSet,
                    TokenViewSet, TitleViewSet, UserViewSet)


router_v1 = DefaultRouter()

router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='token')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
