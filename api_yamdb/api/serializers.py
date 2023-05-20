import datetime as dt

from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализует запросы к отзывам"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        if self.context['request'].method == 'POST':
            current = Review.objects.filter(author=author, title_id=title_id)
            if current.first():
                raise ValidationError("Запрещено оставлять два отзыва на одно"
                                      "произведение!")
        return data

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
        slug_field='slug')

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=False,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            required=False,
                                            slug_field='slug'
                                            )

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(
            instance=instance.category, read_only=True
        ).data
        representation["genre"] = GenreSerializer(
            instance=instance.genre, read_only=True, many=True
        ).data
        return representation


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
    username = serializers.CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
            RegexValidator(
                regex=r'^(?!me$).*$',
                message='Использовать "me" в качестве username запрещено',
            ),
        ],
    )
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True,
    )

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        validators=[UnicodeUsernameValidator()],
        required=True)
    confirmation_code = serializers.CharField(
        required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализует данные пользователя."""

    username = serializers.CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=[
            UnicodeUsernameValidator(),
            RegexValidator(
                regex=r'^(?!me$).*$',
                message='Использовать "me" в качестве username запрещено',
            ),
            UniqueValidator(queryset=User.objects.all())
        ],
        
    )
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


class UserEditSerializer(UserSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)
