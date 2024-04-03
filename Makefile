THIS_FILE := $(lastword $(MAKEFILE_LIST))

COMPOSE_FILES := -f docker-compose.yml -f docker-compose.override.yml

start:
	docker-compose $(COMPOSE_FILES) up --remove-orphans -d

down:
	docker-compose $(COMPOSE_FILES) down

restart:
	docker-compose $(COMPOSE_FILES) restart

rebuild:
	docker-compose $(COMPOSE_FILE) up -d --remove-orphans --build

ps:
	docker-compose ps

# e.g. make logs c=backend
logs:
	docker-compose $(COMPOSE_FILE) logs --tail=300 -f $(c)

tests:
	docker-compose $(COMPOSE_FILE) exec backend poetry run pytest --create-db $(c)

tests-all:
	docker-compose $(COMPOSE_FILE) exec backend poetry run pytest -p no:warnings --cov-report term:skip-covered --cov --cov-fail-under=93


backend-shell:
	docker-compose $(COMPOSE_FILES) exec backend bash

django-shell:
	docker-compose $(COMPOSE_FILES) exec backend poetry run python3 manage.py shell

# e.g. make makemigrations c=django_app_name
makemigrations:
	docker-compose $(COMPOSE_FILES) exec backend poetry run python3 manage.py makemigrations $(c)

# e.g. make migrate c=django_app_name
migrate:
	docker-compose $(COMPOSE_FILES) exec backend poetry run python3 manage.py migrate $(c)

pre-commit:
	pre-commit run --all-files

linters:
	docker-compose $(COMPOSE_FILES) exec backend poetry run ruff check . --fix

format:
	docker-compose $(COMPOSE_FILES) exec backend poetry run ruff format .

lint-check:
	docker-compose $(COMPOSE_FILES) exec backend poetry run ruff check . --statistics
