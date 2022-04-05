from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_score, title_year_validator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    email = models.EmailField(max_length=55, unique=True,
                              blank=False, verbose_name='Почта')
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default=USER,
                            verbose_name='Роль'
                            )
    password = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя жанра')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя категории')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название произведения',
        db_index=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        db_column='genre',
        verbose_name='Жанр',
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        db_column='category',
        verbose_name='Категория',
        db_index=True
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    year = models.IntegerField(
        validators=[title_year_validator],
        verbose_name='Дата выпуска'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        db_index=True
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        db_column='author',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[validate_score]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]

    def __str__(self):
        return (
            f'{self.text[:25]}'
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        db_column='author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'{self.text[:50]}'
        )
