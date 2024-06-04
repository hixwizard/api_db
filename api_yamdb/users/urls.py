from django.urls import path
from users.views import SignupView, TokenView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenView.as_view(), name='token'),
]
