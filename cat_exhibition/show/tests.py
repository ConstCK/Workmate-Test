import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status

from .models import Breed, Cat, Vote


class TestExhibition(TestCase):

    # Выполнение перед всеми тестами единожды
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
        cls.auth_url = 'api-auth/'
        cls.api_url = 'api/'
        cls.user_data_1 = {'username': 'Ivanov', 'password': 'user1234'}
        cls.user_data_2 = {'username': 'Petrov', 'password': 'user9876'}
        cls.user_data_3 = {'username': 'Sidorov', 'password': 'user9876'}
        cls.user_data_4 = {'username': 'Johnson', 'password': ''}

        cls.user_1 = cls.c.post(f'/{cls.auth_url}signup/', cls.user_data_1)
        cls.user_2 = cls.c.post(f'/{cls.auth_url}signup/', cls.user_data_2)

        cls.owner_1 = User.objects.get(id=1)
        cls.owner_2 = User.objects.get(id=2)

        cls.breed_data_1 = {'name': 'Сибирская', 'description': 'Крупная длинношерстная порода кошек'}
        cls.breed_data_2 = {'name': 'Британская', 'description': 'Крупная короткошерстная порода кошек'}
        cls.breed_data_3 = {'name': 'Шотландская',
                            'description': 'Крупная короткошерстная порода кошек с прижатыми к голове ушками'}
        cls.breed_data_4 = {'name': 'Дворовая',
                            'description': 'Мелкая и грязная'}

        cls.breed_1 = Breed.objects.create(**cls.breed_data_1)
        cls.breed_2 = Breed.objects.create(**cls.breed_data_2)
        cls.breed_3 = Breed.objects.create(**cls.breed_data_3)

        cls.cat_data_1 = {'name': 'Mark',
                          'description': 'Молодой и веселый',
                          'color': 'Черный',
                          'age': 10,
                          'breed': cls.breed_1,
                          'owner': cls.owner_1}
        cls.cat_data_2 = {'name': 'Sandy',
                          'description': 'Молодая, но гордая',
                          'color': 'Белый',
                          'age': 13,
                          'breed': cls.breed_1,
                          'owner': cls.owner_2}
        cls.cat_data_3 = {'name': 'Billy',
                          'description': 'Ленивый',
                          'color': 'Серый',
                          'age': 23,
                          'breed': cls.breed_2,
                          'owner': cls.owner_1}
        cls.cat_data_4 = {'name': 'Helena',
                          'description': 'Игривая и доверчивая',
                          'color': 'Черный с белыми пятнами',
                          'age': 16,
                          'breed': cls.breed_2,
                          'owner': cls.owner_2}
        cls.cat_data_5 = {'name': 'Vasya',
                          'description': 'Очень культурный',
                          'color': 'Рыжий с белыми пятнами',
                          'age': 6,
                          'breed': 3,
                          'owner': 1}
        cls.cat_data_6 = {'name': 'Jack',
                          'description': 'Очень культурный',
                          'color': 'Рыжий с белыми пятнами',
                          'age': 'old',
                          'breed': 3,
                          'owner': 1}
        cls.cat_data_7 = {'name': 'Mark',
                          'description': 'Молодой и веселый',
                          'color': 'Красный',
                          'age': 20,
                          'breed': 1,
                          }

        cls.cat_1 = Cat.objects.create(**cls.cat_data_1)
        cls.cat_2 = Cat.objects.create(**cls.cat_data_2)
        Cat.objects.create(**cls.cat_data_3)
        Cat.objects.create(**cls.cat_data_4)
        Vote.objects.create(value=5, user_id=1, cat_id=2)

    # Проверка функции регистрации при правильном вводе данных
    def test_signup_success(self):
        response = self.client.post(f'/{self.auth_url}signup/', self.user_data_3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(len(response.data.get('access')), 200)

    # Проверка функции регистрации при неправильном вводе пароля
    def test_signup_failed_1(self):
        response = self.client.post(f'/{self.auth_url}signup/', self.user_data_4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка функции регистрации при повторе пользователя
    def test_signup_failed_2(self):
        response = self.client.post(f'/{self.auth_url}signup/', self.user_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка login функции при правильном вводе данных
    def test_login_success(self):
        response = self.client.post(f'/{self.auth_url}login/', self.user_data_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data.get('access')), 200)

    # Проверка login функции при неправильном вводе данных
    def test_login_failed(self):
        response = self.client.post(f'/{self.auth_url}login/', self.user_data_4)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Проверка метода создания породы
    def test_breed_creation_success(self):
        response = self.client.post(f'/{self.api_url}breeds/',
                                    self.breed_data_4,
                                    headers={'authorization': f'Bearer {self.user_1.data.get("access")}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Проверка метода получения списка всех пород
    def test_breed_getting_success(self):
        response = self.client.get(f'/{self.api_url}breeds/',
                                   headers={'authorization': f'Bearer {self.user_1.data.get("access")}'})
        self.assertEqual(len(response.data), 3)

    # Проверка метода получения списка всех пород для неавторизованных пользователей
    def test_breed_getting_failed(self):
        response = self.client.get(f'/{self.api_url}breeds/', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Проверка метода создания питомца
    def test_cat_creation_success(self):
        response = self.client.post(f'/{self.api_url}cats/',
                                    self.cat_data_5,
                                    headers={'authorization': f'Bearer {self.user_1.data.get("access")}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Проверка метода создания питомца для неавторизованных пользователей
    def test_cat_creation_failed_1(self):
        response = self.client.post(f'/{self.api_url}cats/',
                                    self.cat_data_5,
                                    )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Проверка метода создания питомца с некорректными данными
    def test_cat_creation_failed_2(self):
        response = self.client.post(f'/{self.api_url}cats/',
                                    self.cat_data_6,
                                    headers={'authorization': f'Bearer {self.user_1.data.get("access")}'}
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка метода обновления данных питомца
    def test_cat_update_success(self):
        data = json.dumps(self.cat_data_7)
        response = self.client.put(f'/{self.api_url}cats/{self.cat_1.id}/',
                                     data,
                                     headers={'authorization': f'Bearer {self.user_1.data.get("access")}',
                                              'Content-Type': 'application/json'}
                                     )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Проверка метода обновления данных питомца для чужого хозяина
    def test_cat_update_failed_1(self):
        response = self.client.put(f'/{self.api_url}cats/{self.cat_1.id}/',
                                     self.cat_data_7,
                                     headers={'authorization': f'Bearer {self.user_2.data.get("access")}',
                                              }
                                     )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Проверка метода обновления данных питомца с некорректными данными
    def test_cat_update_failed_2(self):
        data = json.dumps(self.cat_data_6)
        response = self.client.put(f'/{self.api_url}cats/{self.cat_1.id}/',
                                     data,
                                     headers={'authorization': f'Bearer {self.user_1.data.get("access")}',
                                              'Content-Type': 'application/json'}
                                     )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка метода удаления питомца
    def test_cat_delete_success(self):
        response = self.client.delete(f'/{self.api_url}cats/{self.cat_1.id}/',
                                      headers={'authorization': f'Bearer {self.user_1.data.get("access")}', }
                                      )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Проверка метода удаления питомца для чужого хозяина
    def test_cat_delete_failed_1(self):
        response = self.client.delete(f'/{self.api_url}cats/{self.cat_1.id}/',
                                      headers={'authorization': f'Bearer {self.user_2.data.get("access")}', }
                                      )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Проверка метода удаления несуществующего питомца
    def test_cat_delete_failed_2(self):
        response = self.client.delete(f'/{self.api_url}cats/100/',
                                      headers={'authorization': f'Bearer {self.user_1.data.get("access")}', }
                                      )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Проверка метода выставления оценок питомцу
    def test_vote_for_cat_success(self):
        response = self.client.post(f'/{self.api_url}voting/{self.cat_1.id}/',
                                    {'value': 4},
                                    headers={'authorization': f'Bearer {self.user_1.data.get("access")}', }
                                    )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Проверка метода выставления некорректной оценки питомцу
    def test_vote_for_cat_failed_1(self):
        response = self.client.post(f'/{self.api_url}voting/{self.cat_1.id}/',
                                    {'value': 40},
                                    headers={'authorization': f'Bearer {self.user_1.data.get("access")}', }
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка метода выставления повторной оценки питомцу
    def test_vote_for_cat_failed_2(self):

        response = self.client.post(f'/{self.api_url}voting/{self.cat_2.id}/',
                                    {'value': 3},
                                    headers={'authorization': f'Bearer {self.user_1.data.get("access")}', }
                                    )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)