import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reviews.models import User

from .serializers import ConfirmCodeSerializer, EmailSerializer


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
    # confirmation_code = default_token_generator.make_token(username)
    send_mail(
        subject='Код для получения пароля',
        message=f'Ваш код для получения пароля: {confirmation_code}',
        from_email=f'{settings.EMAIL_HOST_USER}',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def get_jwt_token(request):
# """Check confirmation_code and send JWT-token"""
#     serializer = ConfirmCodeSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data['email']
#     user = get_object_or_404(User, email=email)
#     confirmation_code = serializer.data['confirmation_code']
#
