from django.core import validators
from rest_framework import serializers

from .models import Cat, Breed, Vote
from accounts.serializers import UserSerializer


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class CatSerializer(serializers.ModelSerializer):
    # Поля для большей информативности
    breed_info = BreedSerializer(read_only=True, source='breed')
    owner_info = UserSerializer(read_only=True, source='owner')
    total_marks = serializers.IntegerField(read_only=True, default=0)
    total_votes = serializers.IntegerField(read_only=True, default=0)
    age = serializers.IntegerField(default=12)

    class Meta:
        model = Cat
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    cat = CatSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    value = serializers.IntegerField(validators=[validators.MaxValueValidator(5,
                                                                              message='Значение должно быть от 0 до 5')])

    class Meta:
        model = Vote
        fields = ['value', 'user', 'cat']


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default='Успешное выполнение операции')


class Error400ResponseSerializer(serializers.Serializer):
    error = serializers.CharField(default='Введенные данные некорректны')


class Error403ResponseSerializer(serializers.Serializer):
    error = serializers.CharField(default='Отсутствуют права на данную операцию')


class Error404ResponseSerializer(serializers.Serializer):
    error = serializers.CharField(default='Данные не найдены')
