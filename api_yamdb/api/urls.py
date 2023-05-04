from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (register_user, CategoryViewSet, CommentViewSet,
                       GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet,
                       get_token)

app_name = 'api'

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='сategories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')

urlpatterns = [
    path('v1/auth/signup/', register_user, name='signup'),

    path('v1/', include(router.urls)),
    path('v1/auth/token/', get_token, name='get_token'),


]
