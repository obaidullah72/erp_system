# Startup and deployment

See the root README for complete native and Docker startup. Compose requires independent POSTGRES_PASSWORD and JWT_SECRET_KEY. `docker compose config --quiet` validates without printing interpolated secrets. `docker compose up --build -d` starts PostgreSQL → migration → API/frontend, and Redis → worker. No tables are created from API lifespan.

The one-shot migration service must exit successfully before API/worker start. Bootstrap is explicit: `docker compose exec api python -m scripts.bootstrap_admin --business demo --name 'My Business' --email admin@example.com`. Password entry is interactive and never appears in command arguments. Existing installations refuse bootstrap. `docker compose ps`, API `/api/v1/health/live` and `/ready`, Redis PING, worker control ping and frontend HTTP checks expose coarse health. API readiness currently verifies database connectivity, not revision parity; deployment owns migration ordering.

Native services use `make backend`, `make frontend`, and optional `make worker`. Workers require REDIS_URL; no business task or beat schedule exists. Diagnostic task `erp.ping` is the sole registered application task. Exports/notifications/scheduled reports remain unimplemented scaffolds. Add durable outbox delivery before introducing external effects.

Frontend uses a multi-stage Node 22 build and unprivileged Nginx. Python image uses the pinned runtime lock and an unprivileged user. Node installs with `npm ci`; Python 3.11 locks are committed. Containers bind host developer ports to loopback. PostgreSQL/Redis volumes persist across `down`. Restore/upgrade procedures must preserve journal and audit triggers.

`docker compose -f compose.yaml -f compose.production.yaml up --build -d` enables production configuration for API/migration/worker. It is not a full production topology: provide TLS (required for Secure refresh cookies), trusted same-origin ingress, production CORS origins, a private broker, separate DDL/runtime roles, backup/restore validation, monitoring and ingress login throttling. Do not publish development ports directly. Image tags should be promoted to reviewed digests in deployment automation.

## Dependency updates

Runtime constraints: `backend/requirements.txt`; development constraints: `requirements-dev.txt`. Regenerate with Python 3.11 and pip-tools:

```sh
backend/venv/bin/pip-compile --output-file backend/requirements.lock backend/requirements.txt
backend/venv/bin/pip-compile --constraint backend/requirements.lock --output-file backend/requirements-dev.lock backend/requirements-dev.txt
npm install --package-lock-only --prefix frontend
make install
make test-local
make lint build
```

Review dependency/lock diffs before deployment. The locks pin versions; they are not a claim of security certification. See Stage 1 record for exactly which runtime paths were verified in this workspace.
