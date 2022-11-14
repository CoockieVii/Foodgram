# Продуктовый помощник :pizza:
![example workflow](https://github.com/cookievii/Foodgram/actions/workflows/foodgram_workflow.yml/badge.svg)

----------

### Стэк технологий:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

----------

### Описание проекта

Foodgram - продуктовый помощник. Здесь пользователи могут публиковать
рецепты, подписываться на
публикации других пользователей, добавлять понравившиеся рецепты в список
«Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

----------

### Установка:

Установите docker и docker-compose согласно официальной инструкции (взависимости от операционной системы сервера):

- https://docs.docker.com/engine/install/
- https://docs.docker.com/compose/install/

```bash
# - Cкачайте:
git clone git@github.com:cookievii/Foodgram.git

# - Перейдите в папку infra репозитория с помощью команды ;
cd infra/

# - Создаем файл .env -файла(Шаблон наполнения показан ниже).
touch .env

# - Запустите приложения в контейнерах:
docker-compose up -d --build

# - Выполните миграцию в контейнерах:
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# - Создайте суперпользователя Django:
docker-compose exec backend python manage.py createsuperuser

# - Соберите статику:
docker-compose exec backend python manage.py collectstatic --no-input

# - Загрузите предустановленный список ингредиентов в базу данных:
docker-compose exec backend python manage.py load_data
```

### Шаблон наполнения .env -файла:

```bash
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql.
DB_NAME=postgres # имя базы данных.
POSTGRES_USER=postgres # логин для подключения к базе данных.
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой).
DB_HOST=db # название сервиса (контейнера).
DB_PORT=5432 # порт для подключения к БД.
```

### Документация с примерами запросов и ответов*

###### *Доступна после запуска проекта

Документация для API: [по ссылке](http://localhost:8000/redoc/)


----------

### Авторы:

* **Валитов Ильмир Илсурович**
  GitHub - [cookievii](https://github.com/cookievii)

----------

### MIT License:

Copyright (c) 2022 [cookievii](https://github.com/cookievii)

----------
