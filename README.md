# Проект "Выставка кошек" на Django, DRF с использованием  Docker, pytest

Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Workmate-Test.git.
Перейдите в папку проекта.
В терминале создайте виртуальное окружение (например python -m venv venv) и активируйте его (venv\scripts\activate).
Установите все зависимости при помощи pip install -r requirements.txt.
Создайте файл .env в каталоге проекта и пропишите в нем настройки по примеру .env.example.
Ключ для Django можно сгенерировать по пути https://djecrety.ir/.
Запустите сервер из каталога проекта (python manage.py runserver)

# EndPoints:

## AUTH API

http://127.0.0.1:8000/api-auth/signup/ - Регистрация нового пользователя
http://127.0.0.1:8000/api-auth/login/ - Вход в аккаунт уже зарегистрированного пользователя
http://127.0.0.1:8000/api-auth/logout/ - Выход из аккаунта
http://127.0.0.1:8000/api-auth/refresh/ - Получение нового access token при помощи refresh token

## MAIN API

http://127.0.0.1:8000/api/cats/ - Получение всех/указанной породы/ Создание питомцев.
При использовании query params (breed_id= ID породы) получение питомцев породы указанного id.
- http://127.0.0.1:8000/api/cats/id/ - Получение/ Изменение/ Удаление питомца с указанным id. 

- http://127.0.0.1:8000/api/breeds/ - Получение/ Добавление/ пород питомцев. 

- http://127.0.0.1:8000/api/voting/id/ - Выставление оценки питомцу с указанным id. 