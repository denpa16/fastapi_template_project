build:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

up:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up

redis_up:
	docker-compose up redis

down:
	docker-compose down

exec_backend:
	docker-compose exec backend /bin/bash

test:
	docker-compose exec backend pytest

shell:
	docker-compose exec backend python manage.py shell

pre-commit:
	pre-commit run --all-files

linters:
	black --config backend/pyproject.toml backend
	isort --sp backend/pyproject.toml backend
	flake8 --statistics --config backend/setup.cfg backend

check:
	black --config backend/pyproject.toml backend --check
	isort --sp backend/pyproject.toml backend --check-only
	flake8 --statistics --config backend/setup.cfg backend

ssh_dev:
	ssh root@80.249.148.147

ssh_prod:
	ssh root@80.87.107.69

get_crm_token_and_timestamp:
	docker-compose exec backend python manage.py get_token_and_timestamp

parse_properties:
	docker-compose exec backend python manage.py parse_properties
