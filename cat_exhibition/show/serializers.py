from rest_framework import serializers

from .models import Cat, Breed, Vote


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = '__all__'
        # fields = ['name', 'color', 'description', 'age', 'description', 'breed']


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['value']