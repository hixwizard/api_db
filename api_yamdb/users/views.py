import random
from rest_framework import status, views
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers import SignupSerializer, TokenSerializer
from .models import UserModel
from core.constants import MIN_CODE, MAX_CODE
from users.permissions import IsAuthenticatedOrReadOnly


class SignupView(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))
            user, crated = UserModel.objects.get_or_create(
                username=username,
                email=email,
                defaults={'confirmation_code': confirmation_code}
            )
            if not crated:
                user.confirmation_code = confirmation_code
                user.save()
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения {confirmation_code}'
            )
            return Response(
                {'message': 'Код подтверждения отправлен на указаную почту'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
