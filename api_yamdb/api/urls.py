from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    TitleViewSet, CategoryViewSet,
    GenreViewSet, ReviewViewSet, CommentViewSet
)
from .views_matvei import ReviewViewSetT

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(r'titles(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(r'reviews(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('users.urls')),
]
