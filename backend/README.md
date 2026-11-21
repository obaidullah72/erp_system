# Backend foundation

Python 3.11, FastAPI, SQLAlchemy 2.0, PostgreSQL, Alembic, Argon2id/JWT, Celery/Redis. Use the root README for installation, bootstrap, startup and verification. Runtime and development lockfiles are committed; direct requirements files are inputs to intentional lock regeneration.

`app.main:app` wraps the FastAPI factory with global CORS and request logging. `/api/v1` includes auth, users, roles, business settings and health only. `get_db` owns the request transaction; function-scoped dependencies commit before response delivery. Services flush without committing. The posting kernel is internal; inventory is a Protocol, not implemented stock behavior. Foundation models are registered in `app/db/model_registry.py` and migration 0002. Future module migrations remain incremental.

Tests never inherit the developer database URL. Set `ERP_TEST_DATABASE_URL` to a dedicated database ending in `_test` to enable real migration/auth/posting checks; each test creates and removes a random schema. `make test-local` from the root provisions its own temporary PostgreSQL cluster.
