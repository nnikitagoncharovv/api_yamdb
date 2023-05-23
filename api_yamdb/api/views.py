from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .viewsets import CLDslugViewSet, PutNoViewSet

from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperUser,
                          IsAuthenticatedOrReadOnly,
                          IsStaffOrAuthorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleRetriveSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)


class ReviewViewSet(PutNoViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(PutNoViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=title)
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, title=title,
                                   id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CLDslugViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class GenreViewSet(CLDslugViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(PutNoViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('pk')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    search_fields = ('name', 'queryset')

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleRetriveSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Регистрация пользователя"""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    with_email = User.objects.filter(email=email).first()
    with_username = User.objects.filter(username=username).first()
    if with_email:
        if with_email.username != username:
            raise ValidationError("пользователь с таким email уже существует")
    if with_username:
        if with_username.email != email:
            raise ValidationError("пользователь с таким username"
                                  "уже существует")
    user, _ = User.objects.get_or_create(
        username=serializer.data["username"],
        email=serializer.data["email"]
    )

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject="Регистрация на YaMDb",
        message=f"Ваш код активации: {confirmation_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Получение jwt токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Администратор получает список пользователей или создает нового"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperUser, IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],)
    def me_info(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserEditSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserEditSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
