from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.views import (
<<<<<<< HEAD
    TitleViewSet, CategoryViewSet,
    GenreViewSet, CommentViewSet, ReviewViewSet
)
=======
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    CommentViewSet,
    ReviewViewSet)

>>>>>>> 85e76090129dbff2d0639b0b697b3de7de63dd33

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
<<<<<<< HEAD
router_v1.register(r'titles(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'reviews(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')
=======
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet, basename='comments')
>>>>>>> 85e76090129dbff2d0639b0b697b3de7de63dd33
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('users.urls')),
]
