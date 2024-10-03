from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import Http404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cat, Breed, Vote
from .serializers import CatSerializer, CatCreationSerializer, BreedSerializer, VoteSerializer, SuccessResponseSerializer, \
    Error404ResponseSerializer, Error400ResponseSerializer, Error403ResponseSerializer


# Операции с животными
@extend_schema(tags=['Cats'])
class CatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Получение всех питомцев/ питомцев с указанным id породы в query параметрах
    @extend_schema(summary='Cats data list getting',
                   responses={
                       status.HTTP_200_OK: OpenApiResponse(
                           response=CatSerializer,
                           description='Получение списка питомцев'),
                   },
                   parameters=[
                       OpenApiParameter(
                           name='breed_id',
                           location=OpenApiParameter.QUERY,
                           description='Id породы для фильтрации запроса',
                           required=False,
                           type=int
                       ),
                   ]
                   )
    def list(self, request):
        breed = request.query_params.get('breed_id', None)
        if breed:
            cat = Cat.objects.filter(breed_id=breed)
            serializer = CatSerializer(cat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Cat.objects.all()
        serializer = CatSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Получение питомца с указанным id в url
    @extend_schema(summary='Definite cat data getting',
                   responses={
                       status.HTTP_200_OK: OpenApiResponse(
                           response=CatSerializer,
                           description='Получение указанного питомца'),
                       status.HTTP_404_NOT_FOUND: OpenApiResponse(
                           response=Error404ResponseSerializer,
                           description='Указанный питомец не найден'),
                   },
                   parameters=[
                       OpenApiParameter(
                           name='id',
                           location=OpenApiParameter.PATH,
                           description='Id питомца',
                           required=True,
                           type=int)
                   ]
                   )
    def retrieve(self, request, pk: int = None):
        try:
            cat = Cat.objects.get(id=pk)
            serializer = CatSerializer(cat)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404({'error': f'Животное с указанным id={pk} не найдено.'})

    # Добавление питомца
    @extend_schema(summary='Cat data adding',
                   request=CatCreationSerializer,
                   responses={
                       status.HTTP_201_CREATED: OpenApiResponse(
                           response=CatSerializer,
                           description='Добавление данных о питомце'),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           response=Error400ResponseSerializer,
                           description='Введенные данные некорректны'),
                   },
                   )
    def create(self, request):
        cat_data = request.data.copy()
        cat_data['owner'] = request.user.id
        serializer = CatSerializer(data=cat_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Передайте все данные о питомце'}, status=status.HTTP_400_BAD_REQUEST)

    # Изменение данных питомца с проверкой на принадлежность
    @extend_schema(summary='Cat data changing',
                   request=CatSerializer,
                   responses={
                       status.HTTP_201_CREATED: OpenApiResponse(
                           response=CatSerializer,
                           description='Изменение данных о питомце'),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           response=Error400ResponseSerializer,
                           description='Введенные данные некорректны'),
                       status.HTTP_403_FORBIDDEN: OpenApiResponse(
                           response=Error403ResponseSerializer,
                           description='Отсутствуют права на изменение данных'),
                       status.HTTP_404_NOT_FOUND: OpenApiResponse(
                           response=Error404ResponseSerializer,
                           description='Питомец не найден'),
                   },
                   parameters=[
                       OpenApiParameter(
                           name='id',
                           location=OpenApiParameter.PATH,
                           description='Id питомца',
                           required=True,
                           type=int)
                   ]
                   )
    def partial_update(self, request, pk: int = None):
        try:
            cat = Cat.objects.get(id=pk)
            # Проверка на принадлежность питомца создателю запроса
            if cat.owner.id != request.user.id:
                return Response('У Вас нет прав изменять эти данные. Животное принадлежит не Вам.',
                                status=status.HTTP_403_FORBIDDEN)
            cat_data = request.data.copy()
            cat_data['owner'] = request.user.id
            serializer = CatSerializer(instance=cat, data=cat_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Передайте все данные о питомце'}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404(f'Животное с указанным id={pk} не найдено.')

    # Удаление питомца по id с проверкой на принадлежность
    @extend_schema(summary='Cat data erasing',
                   responses={
                       status.HTTP_200_OK: OpenApiResponse(
                           response=SuccessResponseSerializer,
                           description='Удаление данных о питомце'),
                       status.HTTP_403_FORBIDDEN: OpenApiResponse(
                           response=Error403ResponseSerializer,
                           description='Отсутствуют права на удаление данных'),
                       status.HTTP_404_NOT_FOUND: OpenApiResponse(
                           response=Error404ResponseSerializer,
                           description='Питомец не найден'),
                   },
                   parameters=[
                       OpenApiParameter(
                           name='id',
                           location=OpenApiParameter.PATH,
                           description='Id питомца',
                           required=True,
                           type=int)
                   ]
                   )
    def destroy(self, request, pk: int = None):
        try:
            cat = Cat.objects.get(id=pk)
            # Проверка на принадлежность питомца создателю запроса
            if cat.owner.id != request.user.id:
                return Response({'error': 'У Вас нет прав удалять эти данные. Животное принадлежит не Вам.'},
                                status=status.HTTP_403_FORBIDDEN)
            cat.delete()
            return Response({'message': f'Животное с id={pk} было удалено с выставки'},
                            status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise Http404(f'Животное с указанным id={pk} не найдено.')


# Операции с породами
@extend_schema(tags=['Breeds'])
class BreedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Получение всех пород
    @extend_schema(summary='Breed data list getting',
                   responses={
                       status.HTTP_200_OK: OpenApiResponse(
                           response=BreedSerializer,
                           description='Получение списка пород питомцев'),
                   },
                   )
    def list(self, request):
        queryset = Breed.objects.all()
        serializer = BreedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Добавление пород
    @extend_schema(summary='Breed data adding',
                   request=BreedSerializer,
                   responses={
                       status.HTTP_201_CREATED: OpenApiResponse(
                           response=BreedSerializer,
                           description='Добавление данных о породе кошек'),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           response=Error400ResponseSerializer,
                           description='Введенные данные некорректны'),
                   },
                   )
    def create(self, request):
        serializer = BreedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Передайте все данные о породе'}, status=status.HTTP_400_BAD_REQUEST)


# Выставление оценок котенку
@extend_schema(tags=['Votes'])
class VoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Процесс голосование за питомца
    @extend_schema(
        summary='Cats valuation',
        request=VoteSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=SuccessResponseSerializer,
                description='Удаление данных о питомце'),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=Error403ResponseSerializer,
                description='Неверная оценка'),
            status.HTTP_409_CONFLICT: OpenApiResponse(
                response=Error403ResponseSerializer,
                description='Вы уже голосовали'),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=Error404ResponseSerializer,
                description='Питомец не найден'),
        },
    )

    def post(self, request, cat_id: int =None):
        mark = int(request.data.get('value'))
        try:
            serializer = VoteSerializer(data=request.data)
            if not serializer.is_valid():
                raise ValidationError
            user = User.objects.get(pk=request.user.id)
            cat = Cat.objects.get(pk=cat_id)
            Vote.objects.create(user=user,
                                cat=cat,
                                value=mark)
            # Расчет нового рейтинга питомца
            cat.total_votes += 1
            cat.total_marks += mark
            cat.rating = cat.total_marks / cat.total_votes
            cat.save()
            return Response({'message': f'Вы успешно поставили {mark} питомцу с id={cat_id}'},
                            status=status.HTTP_200_OK)
        except ValidationError:
            return Response({'error': 'Не удалось оценить питомца.Оценка должна быть от 0 до 5.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': f'Питомца с id={cat_id} не существует.'},
                            status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'error': f'Вы уже голосовали за питомца с id={cat_id}.'},
                            status=status.HTTP_409_CONFLICT)
