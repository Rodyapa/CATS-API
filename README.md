# CATS-API (Тестовое задание)
## Endpoints
* /docs/swagger/ - Документация эндпоинтов.
## Просмотр проекта на локальной машине:
Склонировать репозиторий на локальную машину:
```
git clone git@github.com:Rodyapa/CATS-API.git
```
Перейти в директорию с файлом  docker-compose
```
cd CATS-API/infra
```
Создайте файл с необходимыми переменными окружения:
```
touch .env
```
Заполните файл:
```
POSTGRES_DB=django_db # Название базы данных, которая будет создана в контейнере PostgreSQL
POSTGRES_USER=django_admin # Имя пользователя, от имени которого будет использоваться база данных
POSTGRES_PASSWORD=password1@s # Пароль пользователя бд
DB_HOST=db   # По умолчанию - db (по названию сервиса в файле docker-compose)
DB_PORT=5432 # По умолчанию - порт на который PostgreSQL отвечает по умолчанию
```
Запустить контейнеры
```
sudo docker compose -f docker-compose.yml -d 
```
Запросы к api делать на порт 8070:
```
http://127.0.0.1:8070/api/...
```
## Запуском тестов:
Запуск тестов из корневой директории проекта
```

```
## Технологии:
    *Python
    *Django
    *Django REST framework
    *Swagger OpenAPI Docs
    *pytest library 
