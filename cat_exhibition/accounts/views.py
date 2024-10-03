from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .serializers import UserSerializer, LogOutSerializer, LogOutResponseSerializer, AuthResponseErrorSerializer, \
    SignUpResponseSerializer


# Регистрация нового пользователя с присваиванием и возвращением ему JWT токена

class RegistrationAPIView(APIView):
    @extend_schema(tags=['Auth'],
                   summary='User registration',
                   request=UserSerializer,
                   responses={
                       status.HTTP_201_CREATED: OpenApiResponse(
                           response=SignUpResponseSerializer,
                           description='Успешная регистрация пользователя'),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           response=AuthResponseErrorSerializer,
                           description='Ошибка регистрации пользователя')
                   })
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(username=request.data.get('username'))
            user.set_password(request.data.get('password'))
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response({'error': 'Неверные данные'},
                        status=status.HTTP_400_BAD_REQUEST)


# Вход зарегистрированного пользователя с возвращением ему JWT токена

class LogInAPIView(APIView):
    @extend_schema(tags=['Auth'],
                   summary='User login',
                   request=UserSerializer,
                   responses={
                       status.HTTP_200_OK: OpenApiResponse(
                           response=SignUpResponseSerializer,
                           description='Успешный вход пользователя'),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           response=AuthResponseErrorSerializer,
                           description='Ошибка авторизации пользователя')}
                   )
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Неверные данные'},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


# Выход из аккаунта с добавлением токена в blackList

class LogOutAPIView(APIView):
    @extend_schema(tags=['Auth'],
                   summary='User logout',
                   request=LogOutSerializer,
                   responses={status.HTTP_200_OK: OpenApiResponse(
                       response=LogOutResponseSerializer,
                       description='Успешный выход'),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           response=AuthResponseErrorSerializer,
                           description='Неверный refresh token')})
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)
