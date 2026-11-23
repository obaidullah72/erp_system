# Repeatable verification

## Commands and isolation

`make install` installs pinned native dependencies. `make lint` and `make build` check the frontend. `make test` runs backend tests with database tests explicitly skipped unless `ERP_TEST_DATABASE_URL` is supplied. `make test-integration` refuses to run without that URL; its database name must end in `_test`.

`make test-local` creates a new local PostgreSQL cluster in a unique `/tmp/erp-foundation.*` directory, listens on loopback port 55439 (override ERP_TEST_PORT), runs backend and browser tests, then shuts it down with an EXIT trap. PostgreSQL binaries and a browser executable must be installed first. Logs are retained in the printed temporary directory for diagnosis.

Integration fixtures create unique schemas, apply real Alembic migrations and remove only those schemas. They exclude the public schema from search_path. Test settings ignore `backend/.env` and override the database/signing key before application import. The dedicated database is never the development ERP database. Browser verification independently creates a unique schema, bootstraps test-only credentials, starts API/Vite on 8001/5174, and drops that schema on graceful shutdown. Tests do not rely on production users or accounts.

```sh
# Existing dedicated test PostgreSQL:
export ERP_TEST_DATABASE_URL='postgresql+psycopg://erp_test:password@127.0.0.1:5432/erp_test'
make test-integration
cd frontend && npx playwright install chromium && cd ..
make test-e2e
# Or provision the local disposable cluster automatically:
make test-local
```

Playwright 1.65.1's browser downloader does not support macOS 13. On that host, use an already-installed compatible Chromium executable:

```sh
export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH='/absolute/path/to/chrome-headless-shell'
make test-e2e
```

The override only selects the test browser; no application behavior changes. This workspace has a Chromium headless shell under `~/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-x64/chrome-headless-shell`. On supported hosts, use Playwright's normal browser installer. Screenshots/traces live under ignored `frontend/test-results`; failure artifacts are retained, and the mobile check records a full-page screenshot.

## Coverage

- Settings validation and hidden secret inputs; JWT signature/audience/expiry; independent liveness and sanitized readiness failure; CORS, generated request IDs, redacted JSON errors and validation details.
- Actual migration upgrade/downgrade/re-upgrade and ORM schema parity; first-admin bootstrap and refusal; exact nine-role seed catalogue; password hashing.
- Login, current-user lookup, rotation, old-refresh replay revocation, absolute session expiry, logout and disabled-user revocation.
- Direct Viewer/Admin API denials, protected administrator grants, configurable responsibility roles, last-admin preservation, cross-business API and FK isolation, optimistic settings conflicts, duplicate-user rollback.
- Balanced posting, rejected unbalanced/invalid-mapping/closed-period-hook requests, base currency freeze, duplicate sources, changed idempotency payloads, concurrent duplicate and same-key submissions, outer transaction rollback.
- Direct PostgreSQL unbalanced-commit rejection, immutable journal/audit rows and forbidden later line insertion.
- Structured log checks exclude password/email/token/query/path inputs; diagnostic worker ping has no business effects.
- Real desktop/mobile browser login, invalid credentials, protected-path return, cookie session restoration, logout, unavailable metrics, responsive navigation, persisted theme, live health responses and horizontal-overflow check.

## Recorded environment and limits

Python 3.11, Node 22.23.2, PostgreSQL 16.15. Fresh Python installation used `requirements-dev.lock`; frontend used `npm ci`. Compose targets PostgreSQL 17; that container version was not exercised here. Base and production-override Compose configurations were validated using nonsecret placeholders without printing resolved configuration.

Docker Engine is unavailable in this workspace. Container image builds, Compose startup and live Redis/Celery broker delivery remain unverified here. Celery configuration and diagnostic task execution are checked without claiming business jobs exist. The installed Starlette test client emits one httpx deprecation warning; it does not fail checks. Final consolidated `make test-local`: **30 backend checks and 2 browser checks passed**, with automatic temporary-cluster shutdown. Frontend lint/build and both Compose configuration checks passed. See the Stage 1 completion record for the full evidence table.

Migrations and tests make no claim about later module correctness. Inventory protocols, open-period policy, planned contracts and worker stubs are documented extension points.
