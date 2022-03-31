import re
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User
from rest_framework.relations import SlugRelatedField


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
