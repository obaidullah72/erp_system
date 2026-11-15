.PHONY: help install backend frontend build test up down migrate health
PYTHON ?= python3
BACKEND_PYTHON := backend/venv/bin/python

help:
	@echo "install backend frontend build test up down migrate health"

install:
	$(PYTHON) -m venv backend/venv
	$(BACKEND_PYTHON) -m pip install -r backend/requirements-dev.txt
	npm ci --prefix frontend

backend:
	cd backend && venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

frontend:
	npm run dev --prefix frontend

build:
	npm run build --prefix frontend

test:
	cd backend && venv/bin/python -m pytest -q

up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	cd backend && venv/bin/python -m alembic upgrade head

health:
	curl --fail --show-error http://localhost:8000/api/v1/health/live
	curl --fail --show-error http://localhost:8000/api/v1/health/ready
