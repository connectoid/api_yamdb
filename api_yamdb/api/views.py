import random
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Category, Genre, User, Review, Comment, Title
from .mixins import UpdateDeleteViewSet, ListCreateDeleteViewSet
from .permissions import AdminOnly, OwnerOrReadOnly
from .serializers import (CategorySerializer, ConfirmCodeSerializer,
                          EmailSerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer, TitleSerializer,
                          TitleListSerializer, UserSerializer,
                          UserInfoSerializer)


@api_view(['POST'])
def confirmation_code(request):
    """Send confirmation_code by email"""
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    email = serializer.data['email']
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email)
        send_confirm_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username, email=email)
    send_confirm_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Check confirmation_code and send JWT-token"""
    serializer = ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(ListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(ListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)


class UserInfoView(APIView):
    """ViewSet для User"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserInfoSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirm_code(user):
    """Send confirmation_code"""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код авторизации',
        message=f'Ваш код для авторизации на сайте: {confirmation_code}',
        from_email=f'{settings.EMAIL_HOST_USER}',
        recipient_list=[user.email],
        fail_silently=False,
    )
