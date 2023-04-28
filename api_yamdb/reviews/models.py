from django.db import models
from django.core import validators
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True
    )
    password = None

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Categories(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[validators.RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категории содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(
        max_length=75,
        verbose_name='Название жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='год выпуска',
        validators=[
            validators.MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            validators.MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='жанр'

    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre}'


class Review(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            validators.MinValueValidator(
                1,
                message='Оценка не может быть меньше 1.'
            ),
            validators.MaxValueValidator(
                10,
                message='Оценка не может быть больше 10.'
            )
        ],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Пользователь, который оставил комментарий'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
