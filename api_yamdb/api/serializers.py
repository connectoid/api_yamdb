import re
import datetime

from django.conf import settings
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from rest_framework.relations import SlugRelatedField
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя пользователя "me" не разрешено.'
            )
        return username


class EmailSerializer(serializers.ModelSerializer):
    """Email serializer"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя пользователя "me" не разрешено.'
            )
        return username


class ConfirmCodeSerializer(serializers.Serializer):
    """Confirmation code serializer"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context['request']
        user = request.user
        pk = request.parser_context['kwargs'].get('title_id')
        title = get_object_or_404(Title, pk=pk)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=user).exists():
                raise ValidationError(
                    'Вы уже оставляли комментарий к этому обзору'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, value):
        pattern = '^[-a-zA-Z0-9_]+$'
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                'Недопустимые символы в поле slug'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        exclude = ('descriptions',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all()
    )
    # category = CategorySerializer()
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        many=True,
        queryset=Genre.objects.all()
    )
    # genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'category', 'genre',
            'year', 'descriptions', 'rating',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year'),
                message='Такое произведениеe уже сущесвтует'
            )
        ]

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))
        return rating['score__avg']

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError(
                f'Год выпуска не может быть больше {year}'
            )
        return value


class UserInfoSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )
