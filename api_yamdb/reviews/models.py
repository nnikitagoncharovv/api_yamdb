from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.db import models

from api_yamdb.settings import MAX_NAME, MAX_SLUG
from users.models import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=MAX_NAME)
    slug = models.SlugField('ID категории', max_length=MAX_SLUG, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=MAX_NAME)
    slug = models.SlugField('ID жанра', max_length=MAX_SLUG, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Произведение', max_length=MAX_NAME)
    year = models.IntegerField('Дата издания',)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'от 1 до 10', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title', ],
                name='unique'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
