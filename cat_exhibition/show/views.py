from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cat, Breed, Vote
from .serializers import CatSerializer, BreedSerializer, VoteSerializer


# Операции с животными
class CatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        breed = request.query_params.get('breed_id', None)
        if breed:
            try:
                cat = Cat.objects.filter(breed_id=breed)
                serializer = CatSerializer(cat, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                raise Http404(f'Животное с указанной породой не найдено.')
        print('123')
        queryset = Cat.objects.all()
        serializer = CatSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            cat = Cat.objects.get(pk=pk)
            serializer = CatSerializer(cat)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404(f'Животное с указанным id={pk} не найдено.')

    def create(self, request):
        cat_data = request.data
        cat_data['owner'] = request.user.id
        serializer = CatSerializer(data=cat_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            cat = Cat.objects.get(pk=pk)
            if cat.owner != request.user.id:
                return Response('У Вас нет прав изменять эти данные. Животное принадлежит не Вам.',
                                status=status.HTTP_403_FORBIDDEN)
            cat_data = request.data
            cat_data['owner'] = request.user.id
            serializer = CatSerializer(instance=cat, data=cat_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            raise Http404(f'Животное с указанным id={pk} не найдено.')

    def destroy(self, request, pk=None):
        try:
            cat = Cat.objects.get(pk=pk)
            if cat.owner != request.user.id:
                return Response('У Вас нет прав удалять эти данные. Животное принадлежит не Вам.',
                                status=status.HTTP_403_FORBIDDEN)
            cat.delete()
            return Response({'message': f'Животное с id={pk} было удалено с выставки'},
                            status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise Http404(f'Животное с указанным id={pk} не найдено.')


class BreedViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Breed.objects.all()
        serializer = BreedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = BreedSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class VoteAPIView(APIView):

    def post(self, request, cat_id=None):
        value = request.data.get('value')

        try:
            serializer = VoteSerializer(data={'value': value})
            if not serializer.is_valid():
                raise ValidationError
            user = User.objects.get(pk=request.user.id)
            cat = Cat.objects.get(pk=cat_id)
            Vote.objects.create(user=user,
                                cat=cat,
                                value=value)
            if not cat.rating:
                cat.rating = value
            else:
                cat.rating = (value + cat.rating) / 2
            cat.save()
            return Response(f'Вы успешно поставили {value} питомцу с id={cat_id}')
        except ValidationError:
            return Response(f'Не удалось оценить питомца.Оценка должна быть от 0 до 5.')
        except ObjectDoesNotExist:
            return Response(f'Питомца с id={cat_id} не существует.')
        except IntegrityError:
            return Response(f'Вы уже голосовали за питомца с id={cat_id}.')
