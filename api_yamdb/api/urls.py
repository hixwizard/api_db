from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    AuthViewSet, UserViewSet, TitleViewSet, CategoryViewSet,
    GenreViewSet, ReviewViewSet, CommentViewSet
)

router_v1 = DefaultRouter()

# Аутентификация
router_v1.register('auth', AuthViewSet, basename='auth')

# Пользователи
router_v1.register('users', UserViewSet, basename='users')

# Произведения
router_v1.register('titles', TitleViewSet, basename='titles')

# Категории
router_v1.register('categories', CategoryViewSet, basename='categories')

# Жанры
router_v1.register('genres', GenreViewSet, basename='genres')

# Отзывы
router_v1.register(r'titles(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')

# Комментарии
router_v1.register(r'reviews(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
