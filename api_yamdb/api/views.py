from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Category, Genre, Title

from .serializers import (CategorySerializer, GenreSerializer, TitleCreateSerializer, TitleSerializer)

class TitleViewSet(viewsets.ModelViewSet):
    """
    Admin can manage titles, other can only read
    titles/ - get all titles
    titles/{id}/ - get title with id
    titles/?gerne,category,year,name - filter titles
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

class GenreViewSet(viewsets.ModelViewSet):
    """
    Admin can manage genres, other can only read
    /genres/ - get all genres
    /genres/{id}/ - get genre with id
    /genres/{slug}/ - delete genre with slug
    /genres/?search=name - search genre with name
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
    """
    Admin can manage genres, other can only read
    /categories/ - get all categories
    /categories/{id}/ - get category with id
    /categories/{slug}/ - delete category with slug
    /genres/?search=name - search category with name
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
