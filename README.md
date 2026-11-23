# TradeCore ERP — Stage 1 Foundation

Runnable React/Tailwind v4 + FastAPI/PostgreSQL modular monolith with login, live authorization, nine roles, business settings, foundation migrations, and an internal transactional journal kernel. Business transaction modules remain planned; the dashboard shows unavailable metrics honestly.

## Quick start with Docker Compose

Requires Docker Engine/Compose v2. Copy `.env.example` to `.env`. Replace both placeholder secrets independently using `python3 -c "import secrets; print(secrets.token_hex(32))"`; use URL-safe hex for POSTGRES_PASSWORD. Placeholders are not usable credentials.

```sh
cp .env.example .env
# Edit .env with generated secrets before continuing.
docker compose config --quiet
make up
docker compose exec api python -m scripts.bootstrap_admin --business demo --name 'My Business' --email admin@example.com
```

The bootstrap prompts for a password (12–256 characters) twice. It creates one business and its nine roles, then refuses all further bootstrap attempts. There is no default account or public registration endpoint. Sign in at **http://localhost:8080/login** with business code `demo` and your chosen credentials. API docs: http://localhost:8000/docs. The bootstrap must run after migrations complete.

Compose starts PostgreSQL, applies migrations in a one-shot service, starts the API and frontend, and starts Redis plus a Celery worker. All long-running services have health checks. `docker compose ps` shows status. `make down` preserves volumes. Changing `.env` database passwords does not rotate an existing PostgreSQL role's password.

## Native development

Requires Python 3.11, Node 22.12+ (Node 22 recommended), npm, and PostgreSQL 16/17. Redis is needed only to run the worker; authentication and posting do not depend on Redis. With root Compose secrets configured, `docker compose up -d db redis` provides both on loopback ports 5432/6379.

```sh
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
make install
# Edit backend/.env: real DATABASE_URL and independently generated JWT_SECRET_KEY.
# Create the configured PostgreSQL role/database, or use Compose's db service.
make migrate
cd backend
venv/bin/python -m scripts.bootstrap_admin --business demo --name 'My Business' --email admin@example.com
cd ..
make backend
# Another terminal:
make frontend
# Optional, once Redis is available:
make worker
```

Open **http://localhost:5173/login**. Vite proxies `/api` to port 8000; container Nginx proxies to `api:8000`. Native settings always load `backend/.env`; environment variables override it. Root `.env` is Compose-only. VITE settings are public; never put secrets there. Keep frontend/API same-origin through a proxy for refresh cookies.

`make install` uses `backend/requirements-dev.lock` and `frontend/package-lock.json`; Docker uses `backend/requirements.lock` and `npm ci`. Direct dependency manifests remain available for intentional upgrades. Python locks target Python 3.11; regenerate/test them when upgrading the interpreter.

## Verification

```sh
make test                       # unit checks; PostgreSQL checks explicitly skip without test URL
make lint
make build
make test-local                 # fresh temporary local PostgreSQL cluster; tests + browser checks
# Or use an existing dedicated database whose name ends in _test:
export ERP_TEST_DATABASE_URL='postgresql+psycopg://erp_test:password@127.0.0.1:5432/erp_test'
make test-integration
cd frontend && npx playwright install chromium && cd ..
make test-e2e
make health                     # running native API, port 8000
```

`make test-local` requires PostgreSQL binaries (`initdb`, `pg_ctl`, `createdb`) and Chromium installed by Playwright. It owns its temporary cluster and shuts it down on exit; it does not use developer database settings. Each integration test gets a random schema, real Alembic upgrades, and teardown. Browser tests start isolated API/Vite servers on 8001/5174, use test-only credentials and drop their random schema on shutdown. See [verification and limitations](docs/testing.md).

## What is implemented

- Argon2id passwords; 15-minute access JWTs; seven-day absolute sessions by default; rotating HttpOnly refresh cookies, replay revocation, logout, current-user lookup, active-user checks.
- Super Admin, Admin, Accountant, Sales Manager, Purchase Manager, Inventory Manager, Production Manager, Cashier, Viewer. Explicit module/action grants. Super Admin-only protected controls, configurable responsibility roles, read-only Viewer.
- Authorized user, role and business-settings APIs with tenant boundaries and optimistic versions; request IDs, safe error envelopes, structured request logs and exact CORS origins.
- Fifteen foundation tables plus Alembic versioning. Journal balance/immutability triggers, source uniqueness, account mapping checks, idempotency and rollback. Period-policy and inventory interfaces are explicit extension points.
- Connected login, protected shell, responsive navigation, persistent theme, shared controls, live health page. No fabricated sales or stock figures.

## Documentation

[Architecture](docs/architecture.md) · [Layer map](docs/folder-structure.md) · [Full domain design](docs/domain-model.md) · [Database/migrations](docs/database-design.md) · [API baseline](docs/api.md) · [Security and roles](docs/security.md) · [Deployment](docs/deployment.md) · [Traceability](docs/traceability.md) · [Stage 1 record](docs/phases/phase-01-foundation.md)
