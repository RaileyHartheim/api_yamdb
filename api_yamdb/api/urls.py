from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, SignUpViewSet, TitleViewSet, TokenViewSet,
                    UserViewSet)

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='token')
router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet, basename='reviews')

router_v1.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentsViewSet, basename='reviews')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
