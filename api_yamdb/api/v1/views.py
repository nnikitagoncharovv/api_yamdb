from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, permissions, viewsets

from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title

from .permissions import IsAdminOrReadOnlyPermission
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleRetriveSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    filterset_fields = ('category', 'genre',
                        'name', 'year')
    
    def get_serializer_class(self):
        if self.action == 'list' or 'retrive':
            return TitleRetriveSerializer
        return TitleSerializer
