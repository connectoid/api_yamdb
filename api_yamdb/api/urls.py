from django.urls import include, path
from rest_framework import routers

from .views import confirmation_code, get_jwt_token

urlpatterns = [
    path('v1/auth/signup/', confirmation_code),
    path('v1/auth/token/', get_jwt_token),
]