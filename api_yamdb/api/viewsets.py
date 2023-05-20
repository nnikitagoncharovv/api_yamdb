from rest_framework import mixins, viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly


class CLDslugViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)


class PutNoViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
