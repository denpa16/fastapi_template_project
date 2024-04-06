THIS_FILE := $(lastword $(MAKEFILE_LIST))

COMPOSE_FILES := -f docker-compose.yml -f docker-compose.override.yml

# e.g. make makemigrations c=django_app_name
makemigrations:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic revision --autogenerate $(c)

# e.g. make migrate c=django_app_name
migrate:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic upgrade head
