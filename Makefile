.PHONY: help install backend frontend worker build lint test test-integration test-e2e test-local up down migrate health
PYTHON ?= python3
BACKEND_PYTHON := backend/venv/bin/python

help:
	@echo "install backend frontend worker build lint test test-integration test-e2e test-local up down migrate health"

install:
	$(PYTHON) -m venv backend/venv
	$(BACKEND_PYTHON) -m pip install -r backend/requirements-dev.lock
	npm ci --prefix frontend

backend:
	cd backend && venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --no-access-log

frontend:
	npm run dev --prefix frontend

worker:
	cd backend && venv/bin/python -m celery -A app.workers.celery_app:celery_app worker --loglevel=WARNING --concurrency=2

build:
	npm run build --prefix frontend

lint:
	npm run lint --prefix frontend

test:
	cd backend && venv/bin/python -m pytest -q

test-integration:
	@test -n "$$ERP_TEST_DATABASE_URL" || (echo "Set ERP_TEST_DATABASE_URL to a dedicated *_test database"; exit 1)
	cd backend && venv/bin/python -m pytest -q

test-e2e:
	@test -n "$$ERP_TEST_DATABASE_URL" || (echo "Set ERP_TEST_DATABASE_URL to a dedicated *_test database"; exit 1)
	npm run test:e2e --prefix frontend

test-local:
	bash scripts/test-local.sh

up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	cd backend && venv/bin/python -m alembic upgrade head

health:
	curl --fail --show-error http://localhost:8000/api/v1/health/live
	curl --fail --show-error http://localhost:8000/api/v1/health/ready
