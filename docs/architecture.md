# Architecture and major layers

TradeCore is a modular monolith: one FastAPI API, one PostgreSQL database, one React SPA and one Celery worker process sharing application code. Redis is the worker broker, not a source of financial truth. Nginx serves the production SPA and proxies `/api`; Vite provides the same contract during development. Tailwind v4 is integrated through `@tailwindcss/vite` and the CSS import/custom dark variant.

| Layer | Responsibility | Entry points |
|---|---|---|
| Browser presentation | Layout, accessible controls, forms, truthful availability states | frontend/src/layouts, components, pages |
| Browser application | Router, protected routes, session state and permission affordances | frontend/src/app, auth |
| Transport client | Same-origin Axios, in-memory bearer token, cookie refresh coalescing, safe error mapping | frontend/src/lib/axios.js |
| HTTP adapters | Typed schemas, dependencies, pagination and response DTOs | backend/app/auth/routes.py, modules/{users,roles,settings}/routes.py |
| Policies | Live tenant/session identity, explicit grants, protected-role and last-admin checks | auth/dependencies.py, core/permissions.py, module services |
| Application services | Orchestrate business changes, audit, validation; never commit internally | auth/service.py, module service.py, accounting/posting.py |
| Persistence | SQLAlchemy queries and foundation models; named keys, tenant references, decimal types | auth/repository.py, db/model_registry.py, db/session.py |
| Database invariants | Versioned DDL; tenant FKs, uniqueness, deferred journal balance and immutable history | migrations/versions/0002_foundation_tables.py |
| Platform | Validated settings, request IDs, JSON logs, redacted errors, explicit CORS | core/, main.py |
| Asynchronous runtime | Redis/Celery with diagnostic ping and worker health probe | workers/celery_app.py, workers/health.py |
| Verification | Real migrations in isolated schemas, transactional tests, browser lifecycle checks | backend/tests, frontend/tests/e2e |

Foundation models are deliberately registered together in `db/model_registry.py` because they share tenant/security/ledger constraints. Empty historical module files are dormant placeholders. Future concrete domain models should live in their owning module and register with Alembic explicitly. Small administration services currently issue SQLAlchemy queries directly; extract repositories when query reuse justifies them. HTTP code does not perform journal posting.

## Request and transaction lifecycle

A generated request ID wraps CORS and exception handling. Pydantic validates requests without echoing submitted values in errors. Authentication verifies HS256 issuer, audience and expiry, then resolves a live unrevoked session and active user/business. Permissions are fetched from current memberships and role grants; tenant identity comes from the user, not a submitted business ID.

`get_db` owns a single transaction and closes the session. Every writing dependency uses FastAPI `scope='function'` so commit finishes before the success response is sent. Service code flushes only. Exceptions roll back the complete command. CLI bootstrap and future worker commands explicitly own `SessionLocal.begin()`. Never mix manual commits into the request transaction.

The internal posting kernel accepts a validated immutable event and same-business account mappings. It serializes Stage 1 postings per business using the settings lock, checks replay first, validates period/account/currency policy, and writes journal, audit and idempotency result inside a savepoint. Source uniqueness is enforced in PostgreSQL. Savepoint rollback removes partial kernel writes; the outer transaction can still roll back all composed source changes. The per-business lock is intentionally conservative and can be narrowed when actual operational volume warrants it.

Journal rows are immutable. Deferred constraints reject a commit containing no lines, fewer than two lines, or unequal totals. Lines cannot be appended to entries from a prior transaction. Reversal workflows, chart administration, fiscal periods, tax, FX and stock valuation are later modules. `OpenPeriodPolicy` is an explicit Stage 1 policy; the inventory module exposes only a Protocol.

## Runtime limits

No business jobs are scheduled. Exports/email/report tasks are placeholders and are not registered. Add an outbox and consumer deduplication in the same migration as the first asynchronous business effect. Never send external requests inside a financial transaction. Readiness checks connectivity, while Compose's successful migration dependency ensures schema startup order. A separately deployed API must apply migrations first; readiness alone is not a schema audit.

Request logs use route templates, not URL parameters/query strings, and do not log bodies, credentials or authorization headers. Health exposes only coarse status. See [security](security.md), [domain design](domain-model.md), and [API contracts](api.md) for exact guarantees and future boundaries.
