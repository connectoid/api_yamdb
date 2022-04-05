from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    list_filter = ("role", )
    search_fields = ("username__startswith", )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_filter = ("year", )
    search_fields = ("name__startswith", )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ("text", )
    list_filter = ("author", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("text", )
    list_filter = ("author", )
