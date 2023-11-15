# fastapi_template_project
Template Project

## Локальный запуск приложения

```shell
docker-compose build
# Не забудьте создать файл .env
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --remove-orphans -d --build
```

## Создать начальные конфиги для миграций

```shell
docker-compose exec backend alembic init -t async ./app/migrations
```
