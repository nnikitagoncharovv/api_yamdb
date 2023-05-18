import datetime as dt

from django.conf import settings
from django.db import IntegrityError, models
from django.forms import IntegerField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализует запросы к отзывам"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('author', 'id', 'pub_date', 'text', 'score')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализует запросы к коментариям"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('text', 'id', 'pub_date', 'author')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализует запросы к категориям"""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализует запросы к жанрам."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализует запросы к произведниям на изменение."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        required=False, many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), required=False, slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Произведение не может быть из будущего!')
        return value


class TitleRetriveSerializer(serializers.ModelSerializer):
    """Сериализует запросы к произведниям."""
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                                        'description', 'genre', 'category')


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализует запросы на регистрацию."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True
    )
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено!')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_empty(self, data):
        username = data.get('username')
        email = data.get('email')
        if not username:
            raise serializers.ValidationError(
                'Имя пользователя не может быть пустым'
            )
        if not email:
            raise serializers.ValidationError(
                'Email не может быть пустым'
            )
        return data

    def validate(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        try:
            user, _ = User.objects.get_or_create(username=username,
                                                 email=email)
        except IntegrityError:
            raise serializers.ValidationError('Это имя или email уже занято')
        return validated_data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True)
    confirmation_code = serializers.CharField(
        max_length=settings.LIMIT_CODE,
        required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class UserSerializer(serializers.ModelSerializer):
    """Сериализует данные пользователя."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_empty(self, data):
        username = data.get('username')
        email = data.get('email')
        if not username:
            raise serializers.ValidationError(
                'Имя пользователя не может быть пустым'
            )
        if not email:
            raise serializers.ValidationError(
                'Email не может быть пустым'
            )
        return data


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)
