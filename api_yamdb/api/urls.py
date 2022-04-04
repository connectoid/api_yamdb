from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    confirmation_code, get_jwt_token)


router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='categories')


urlpatterns = [
    path('v1/auth/signup/', confirmation_code, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='token'),
    path('v1/', include(router.urls)),
]
