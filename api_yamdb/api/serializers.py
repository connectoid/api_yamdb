import re
import datetime
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User
from rest_framework.relations import SlugRelatedField
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )


class EmailSerializer(serializers.Serializer):
    """Email serializer"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


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
                raise ValidationError('Вы уже оставляли комментарий к этому обзору')
        return data

class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    description = serializers.StringRelatedField(required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def validate_slug(self, value):
        pattern = '^[-a-zA-Z0-9_]+$'
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                'Недопустимые символы в поле slug'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    description = serializers.StringRelatedField(required=False)

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError(
                f'Год выпуска не может быть больше {year}'
            )
        return value
