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
    review = SlugRelatedField(slug_field='text',read_only=True)
    class Meta:
        fields = '__all__'
        model = Comment
