from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(default='Wonderful user')
    password = serializers.CharField(write_only=True, default='Secret password')

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class SignUpResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class LogOutResponseSerializer(serializers.Serializer):
    success = serializers.CharField(default='Выход успешен')


class AuthResponseErrorSerializer(serializers.Serializer):
    error = serializers.CharField(default='Неверные данные')
