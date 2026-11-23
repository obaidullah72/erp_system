# Stage 1 — Foundation completion record

Date: 2026-11-22 (Asia/Karachi). This expanded Stage 1 replaces the earlier health-only Phase 1 definition.

## Delivered

- Preserved and completed the React/Vite/Tailwind v4 + FastAPI/SQLAlchemy/PostgreSQL modular monolith. Documented presentation, application, transport, policy, service, persistence, database, platform and worker layers.
- Added pinned frontend and Python runtime/development lockfiles, environment examples, startup/bootstrap instructions, migrations, Docker Compose database/migration/API/frontend/Redis/worker services and health probes.
- Designed the entire ERP domain before implementing operational modules: ownership, relationships, constraints, indexes, lifecycles, dependencies and transaction boundaries in `docs/domain-model.md`.
- Migrated all 15 requested foundation tables (the session implementation uses `auth_sessions`) in revision 0002 after the existing empty 0001. Added composite tenant FKs, financial source/idempotency uniqueness, immutable journal/audit guards and deferred journal balance enforcement.
- Implemented Argon2id passwords; expiring JWTs; rotating refresh cookies with replay revocation; logout/current-user lookup; live server authorization; controlled one-time administrator bootstrap; and the nine exact user-approved roles.
- Added authorized user, role and business-settings APIs, version conflicts, protected administrator/last-admin rules, safe error envelopes, generated request IDs, structured redacted request logs and exact-origin CORS.
- Implemented the internal posting kernel with a typed event/source contract, mapping/currency/balance validation, source uniqueness, idempotency, period-policy hook and caller-owned transactions. Inventory remains an explicit interface, with no fake stock implementation.
- Connected login/protected routes, AuthLayout/DashboardLayout, responsive sidebar/top bar, theme persistence and shared primitives. Dashboard metrics accurately state that operational workflows are not available.
- Published all-module `/api/v1` contract baseline and an implemented-only OpenAPI snapshot. Added isolated real-PostgreSQL integration and browser verification plus a disposable-cluster runner.

## Verification evidence

| Check | Result |
|---|---|
| Clean Python 3.11 install from requirements-dev.lock | Passed in fresh /private/tmp virtual environment |
| Frontend npm ci from package-lock.json | Passed, 233 packages installed |
| Full backend suite with actual PostgreSQL migrations | 30 passed in the final disposable-cluster run |
| Fresh lockfile Python environment running full database suite | 29 passed; one upstream Starlette/httpx deprecation warning |
| Migration upgrade, downgrade/re-upgrade, ORM parity | Passed |
| Login, refresh replay/expiry/logout, live permissions, protected admin/tenant checks | Passed |
| Balanced/invalid/duplicate/concurrent posting, rollback and database immutability | Passed |
| Desktop/mobile browser flows with real API and PostgreSQL | 2 passed using installed Chromium override |
| Browser screenshot inspection | Completed; mobile health page and desktop dashboard rendered correctly |
| Full `make test-local` runner | Passed: new cluster, 30 backend checks, 2 browser checks, automatic shutdown |
| Frontend lint and production build | Passed; system chart code split from core bundle |
| Base/production Compose configuration | Passed with nonsecret validation-only environment values |
| Celery diagnostic task | Passed locally; no business task claimed |
| Container startup / live Redis broker delivery | Not executed: Docker daemon unavailable |

Final native verification is complete. The consolidated runner used PostgreSQL 16.15 and the documented installed-Chromium override. It exited successfully and shut down its temporary cluster.

## Scope boundaries and handoff

Operational modules, account-management screens, fiscal-period administration, reversals, tax/FX, inventory valuation, manufacturing, financial reports, exports and asynchronous business effects remain planned. Default period policy is explicitly open. Responsibility roles are configurable by Super Admin; protected Super Admin/Admin grants and read-only Viewer semantics remain enforced. Admin has no protected Super Admin controls.

Native startup, migration, identity and posting behavior are verified. Container configuration is supplied and validated, but container runtime verification remains an environmental limitation. Playwright's current browser downloader does not support this macOS 13 host; the documented executable-path override was used successfully. Use a supported Playwright browser installation in CI.

Start from the root README. Follow `docs/api.md` for contracts, `docs/traceability.md` for requirement-to-code/test mapping and `docs/testing.md` for repeatable commands. Later modules must add incremental migrations and compose source/stock/journal/audit/idempotency in a single transaction. No business completion is inferred from empty scaffolds or reserved permission grants.
