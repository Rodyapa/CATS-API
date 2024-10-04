# CATS-API (Тестовое задание)
## Endpoints
* /api/docs/swagger/ - Документация эндпоинтов.
## Просмотр проекта на локальной машине:
Склонировать репозиторий на локальную машину:
```
git clone git@github.com:Rodyapa/CATS-API.git
```
Перейти в директорию с файлом  docker-compose
```
cd CATS-API/infra
```
Запустить контейнеры
```
sudo docker compose -f docker-compose.yml -d 
```
Запросы к api делать на порт 8070:
```
http://127.0.0.1:8070/api/...
```

## Технологии:
    *Python
    *Django
    *Django REST framework
    *Swagger OpenAPI Docs
    *pytest library 
