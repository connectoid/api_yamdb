from django.urls import include, path
from rest_framework import routers

from .views import (ReviewViewSet, CommentViewSet, confirmation_code,
                    get_jwt_token, UserInfoView, UserViewSet)


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/signup/', confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserInfoView.as_view()),
    path('v1/', include(router.urls)),
]
