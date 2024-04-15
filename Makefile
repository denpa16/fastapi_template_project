THIS_FILE := $(lastword $(MAKEFILE_LIST))

COMPOSE_FILES := -f docker-compose.yml -f docker-compose.override.yml

# e.g. make makemigrations c=django_app_name
makemigrations:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic revision --autogenerate -m "$(c)"

# e.g. make migrate c=django_app_name
migrate:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic upgrade head

# e.g. make tests c=app_name
tests:
	docker-compose $(COMPOSE_FILES) exec backend poetry run pytest $(c)
