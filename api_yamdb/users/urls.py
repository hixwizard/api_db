from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import SignupView, TokenView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='token'),
    path('', include(router.urls)),
]
