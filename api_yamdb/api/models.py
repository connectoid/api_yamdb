from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField()
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    categories = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    descriptions = models.TextField(),
    year = models.IntegerField()

    def __str__(self):
        return self.name
