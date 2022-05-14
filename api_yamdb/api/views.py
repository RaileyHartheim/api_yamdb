from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .confirmation import send_confirmation_code
from .filters import TitleFilter
from .permissions import (AdminOrReadOnlyPermission, AdminPermission,
                          AuthorOrModerOrAdminPermission)
from .serializers import (AdminUserSerializer, CategorySerializer,
                          CommentsSerializer, GenreSerializer,
                          ReviewSerializer, SignupSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [AdminOrReadOnlyPermission]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [AdminOrReadOnlyPermission]

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnlyPermission,)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username).exists():
            return Response(
                'Это имя пользователя уже занято',
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                'Эта почта уже была использована при регистрации',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create(username=username, email=email)
        user.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not user:
            return Response(
                {'username': 'Такого пользователя не существует'},
                status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Некорректный код'},
            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        ['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = AdminUserSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [AuthorOrModerOrAdminPermission,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comment.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrModerOrAdminPermission,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(author=self.request.user,
                                 title=title).exists():
            raise serializers.ValidationError()
        else:
            serializer.save(author=self.request.user, title=title)
