# Stage 1 requirement traceability

This is the retained Stage 1 evidence map. The current full-source baseline is [ERP requirements traceability](requirements-traceability.md), reconciled against `docs/erp-source/` and the user-confirmed role override. Source phase numbers differ from the legacy nine-phase roadmap.

The Stage 1 completion record contains observed verification results. File paths below are relative to repository root. Planned domain contracts are not claims of implemented modules.

| Request | Implementation / deliverable | Verification |
|---|---|---|
| 1 Inspect, initialize and document architecture | README; docs/architecture.md; docs/folder-structure.md; existing modular monolith preserved, foundation files completed | Frontend production build; ASGI/browser startup |
| 2 Dependencies, Tailwind v4, routing, API client, sessions, migrations, settings, Compose, workers | frontend/package.json + package-lock.json; vite.config.js/index.css; lib/axios.js; backend/requirements*.lock; db/session.py; core/config.py; migrations; Compose/Dockerfiles; workers/ | Clean lockfile installation; build/lint; settings tests; Compose config; diagnostic worker test |
| 3 Full domain model before business modules | docs/domain-model.md and docs/database-design.md | Entity/owner/FK/index/state/dependency/transaction table; later modules remain unregistered |
| 4 Foundation migrations | migrations/versions/0002_foundation_tables.py; db/model_registry.py; db/seed.py | Real upgrade, downgrade/re-upgrade, ORM schema comparison, tenant FK and journal database guards |
| 5 Auth and exact nine roles | auth/; core/security.py; core/permissions.py; scripts/bootstrap_admin.py; docs/security.md; frontend/auth/permissions.js | JWT expiry/signature; password hash; login/logout/refresh replay; bootstrap refusal; exact seed names; direct permission denial |
| 6 Authorized administration, observability | modules/users, roles, settings; audit service; middleware/logging/exceptions; main.py CORS | Protected admin/Viewer rules; last admin; version conflict; tenant isolation; user disable; safe JSON/log/request-ID checks |
| 7 Posting kernel + honest inventory interfaces | modules/accounting/{schemas,posting,periods}.py; inventory/service.py; shared/numbering.py | Balanced/rejected journals; mapping/currency/period hook; duplicate source; same/changed idempotency keys; concurrent replay; outer rollback; DB immutability |
| 8 Connected frontend shell and truthful metrics | AuthProvider/LoginPage/ProtectedRoute; AuthLayout/DashboardLayout; Sidebar/Header; UI primitives; DashboardPage | Browser invalid/valid login, protected redirect, session restoration, logout, mobile navigation, theme persistence, overflow, unavailable metric copy |
| 9 Initial contracts across all modules | docs/api.md; typed implemented route DTOs; shared/schemas.py error envelope | OpenAPI includes implemented routes only; planned resource/permission/filter/decimal/date/version/retry contracts documented |
| 10 Repeatable isolated verification | Makefile; scripts/test-local.sh; backend/tests/conftest.py; tests/integration/test_stage1.py; tests/test_observability.py; frontend/playwright.config.js + tests/e2e | Dedicated *_test DB, random schemas, real migrations, browser API/Vite isolation; documented commands and evidence |

## Exit criteria mapping

| Criterion | Evidence source |
|---|---|
| Clean installation works | Fresh Python 3.11 venv from requirements-dev.lock; npm ci from package-lock.json |
| Frontend/backend start | Playwright-owned Vite and Uvicorn servers; production asset build; TestClient lifespan |
| Login and server permissions work | Integration auth and role tests, browser login, direct Viewer/Admin denials |
| Foundation migrations apply | Fresh schema upgrade for every integration fixture; downgrade/upgrade and metadata parity |
| Invalid/duplicate postings cannot partially commit | Posting service tests plus direct SQL aggregate/immutability tests and concurrent submissions |
| Focused checks pass | docs/testing.md and docs/phases/phase-01-foundation.md record exact results and environmental limits |

## Deliberate boundaries

No operational stock, sales, purchases, manufacturing, report or bank workflow is exposed. No stock service implementation is substituted for the inventory Protocol. Period administration and reversals are future work; the open-period adapter is explicitly documented. Worker business jobs and transactional outbox are future work. Runtime grants for planned modules are capability reservations, not live APIs. Docker runtime and broker delivery require a running container engine; configuration validation alone does not claim a container smoke test.
