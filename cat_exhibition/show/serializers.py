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

    class Meta:
        model = Cat
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(validators=[validators.MaxValueValidator(5,
                                                                              message='Значение должно быть от 0 до 5')])

    class Meta:
        model = Vote
        fields = ['value']
