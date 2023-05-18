from rest_framework import mixins, viewsets

class CLDslugViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,):
    lookup_field = 'slug'


class PutNoViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']