# Local deployment and production path

Use root README commands. Compose builds a Python non-root API, PostgreSQL 17, a one-shot Alembic runner, and an Nginx unprivileged frontend. PostgreSQL must be healthy before migrations; migrations must finish before API startup; readiness must pass before frontend startup. Exposed ports bind to localhost. No workers, Redis, or Celery run.

`docker compose config --quiet` validates interpolation without printing secrets. Root `.env` is required. Container images exclude local environments and secrets using per-context `.dockerignore`. Nginx falls back to index.html for React routes and passes `/api/` directly to FastAPI; API 404 responses must never fall back to the SPA.

`docker compose -f compose.yaml -f compose.production.yaml up --build -d` enables stricter application settings and disables API docs. This override is only a starting point: terminate TLS at a managed ingress, remove developer port exposure as appropriate, use secrets injection, separate database roles, pin immutable image versions/digests and resolved dependencies, and establish monitoring, backups and rollback procedures before public use.

Compose volumes preserve database data across `down`. Do not delete volumes to resolve credential mismatches. PostgreSQL init variables only apply to an empty data directory. Test migrations against restored backups. Phase 1 has no business data migration and no tested production rollout.
