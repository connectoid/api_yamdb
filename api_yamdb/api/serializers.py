from rest_framework import serializers
from reviews.models import Categories, Comment, Genres, Review, Titles, User


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
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)