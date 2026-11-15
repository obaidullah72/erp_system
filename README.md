# TradeCore ERP — Phase 1

A local modular-monolith foundation for trading, wholesale, retail, motorcycle spare parts, electrical meters, and manufacturing. **No business module or login workflow is implemented yet.** Existing empty domain scaffolds remain inactive.

## Prerequisites

Node.js 22.12+ (Node 22 recommended), npm, Python 3.11+, and PostgreSQL 17 or Docker Compose v2. Docker must be running for container commands.

## Run everything with Docker

1. Copy `.env.example` to `.env`.
2. Replace both values with independent secrets. Use URL-safe hex for the database password; the Compose database URL interpolates it directly. Generate each with `python3 -c "import secrets; print(secrets.token_hex(32))"`.
3. Run `docker compose config --quiet`, then `make up`.
4. Open http://localhost:8080/system. API health is at http://localhost:8000/api/v1/health/live and `/api/v1/health/ready`; development API docs are at http://localhost:8000/docs.

Compose waits for PostgreSQL, runs Alembic once through a migration service, then starts the API and frontend. `make down` preserves the database volume. Changing POSTGRES_PASSWORD does not change credentials inside an existing PostgreSQL volume; rotate them explicitly.

## Native development

```sh
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
make install
```

Edit `backend/.env` to use your real local database credentials and an independently generated JWT secret if testing JWT utilities. Start PostgreSQL and create the `erp` database and role, or configure root `.env` and use `docker compose up -d db`. Match its password in `backend/.env`. Native backend environment variables override the `.env` file. Root `.env` is for Compose; it is not automatically loaded by native FastAPI.

```sh
make migrate
make backend
# In another terminal:
make frontend
```

Open http://localhost:5173/system. Vite proxies `/api` to `127.0.0.1:8000`; container Nginx proxies it to `api:8000`. For a separately hosted API, configure frontend `VITE_API_URL` and the backend's explicit JSON `CORS_ORIGINS` list. Vite variables are public and are embedded at build time. Frontend Docker builds intentionally use the same-origin `/api/v1` default.

Without PostgreSQL, the backend starts and liveness returns 200; readiness returns 503. No tables are created during startup. `make migrate` creates only the Alembic revision table at this phase's empty baseline.

## Verification

```sh
make build
make test
make health
cd backend && venv/bin/python -m alembic current
```

The backend tests cover health success/failure, CORS, error redaction, request IDs, settings, and JWT verification. The optional real-database test runs only with `ERP_TEST_DATABASE_URL` set. Read [testing](docs/testing.md) for limits and the actual implementation-session results.

## Documentation

- [Architecture and transaction boundaries](docs/architecture.md)
- [Directory purposes](docs/folder-structure.md)
- [Database blueprint](docs/database-design.md)
- [Nine-phase roadmap](docs/development-roadmap.md)
- [Security](docs/security.md), [deployment](docs/deployment.md), [API](docs/api.md)

Redis and Celery are not required for Phase 1. Future asynchronous workloads must justify their addition. This foundation is not a production-ready ERP release.
