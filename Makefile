THIS_FILE := $(lastword $(MAKEFILE_LIST))

COMPOSE_FILES := -f docker-compose.yml -f docker-compose.override.yml

makemigrations:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic revision --autogenerate -m "$(c)"

migrate:
	docker-compose $(COMPOSE_FILES) exec backend poetry run alembic upgrade head

tests:
	docker-compose $(COMPOSE_FILES) exec backend poetry run pytest $(c)
