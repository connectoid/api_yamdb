from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from api.validators import validate_score


class User(AbstractUser):
    email = models.EmailField(max_length=55, unique=True, blank=False)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20,
                            choices=settings.ROLE_CHOICES,
                            default='user'
                            )
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=250)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        db_column='genre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        db_column='category'
    )
    description = models.TextField(blank=True)
    year = models.IntegerField()

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
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
