import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken


from reviews.models import User, Review, Comment, Title
from .mixins import UpdateDeleteViewSet
from .permissions import OwnerOrReadOnly
from .serializers import ConfirmCodeSerializer, EmailSerializer, ReviewSerializer, CommentSerializer


@api_view(['POST'])
def confirmation_code(request):
    """Get confirmation_code by email"""
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data['username']
    email = serializer.data['email']

    if not User.objects.filter(email=email).exists():
        User.objects.create(username=username, email=email)
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    confirmation_code = ''.join(random.choice(alphabet) for i in range(16))
    print('####', confirmation_code)
    #confirmation_code = default_token_generator.make_token(username)
    send_mail(
        subject='Код для получения пароля',
        message=f'Ваш код для получения пароля: {confirmation_code}',
        from_email=f'{settings.EMAIL_HOST_USER}',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """Check confirmation_code and send JWT-token"""
    serializer = ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    #email = serializer.data['email']
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    print('@@@@', confirmation_code)
     
    """ ЗАМЕНИТЬ НА НОРМАЛЬНУЮ ПРОВЕРКУ КОДА"""

    if confirmation_code:
       token = AccessToken.for_user(user)
       return Response({str(token)})

class ReviewViewSet(UpdateDeleteViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

class CommentViewSet(UpdateDeleteViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
