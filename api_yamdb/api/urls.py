from django.urls import include, path
from rest_framework import routers
from api.views import registration, get_jwt_token
from api.views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'user')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
