# Architecture

## Scope and runtime

Phase 1 is an operational foundation, not a business ERP release. The only API resources are liveness and database readiness. React routes provide system status, foundation information, a memory-only validation form, and a roadmap. Login, CRUD, postings, and reports are not implemented.

The modular monolith has one FastAPI deployment, one PostgreSQL database, and one React application. Vite serves development assets and proxies `/api` to FastAPI. Container Nginx serves the compiled SPA and proxies `/api` to the API. PostgreSQL is the source of truth. No Redis, Celery, or distributed transactions are needed in Phase 1.

## Boundaries

Each future domain owns `routes.py` (HTTP and dependencies), `schemas.py` (Pydantic request/response contracts), `models.py` (SQLAlchemy persistence), `repository.py` (queries and writes), and `service.py` (business orchestration). Routes call services; services use repositories; repositories use request-scoped sessions. Routes never perform business posting, repositories never commit, and models never depend on HTTP. Shared code holds genuinely shared primitives rather than domain rules.

Auth dependencies verify identity; permission decisions belong in explicit policies. Core contains settings, logging, middleware, security, and safe exceptions. Database configuration owns engine, sessions, and the common declarative base. Health follows the same route/schema/service/repository separation without inventing business tables.

Existing empty module files predate this implementation and remain dormant. New modules should be created only when their phase implements them. Cross-domain writes go through an orchestrating service, never a call to another module's HTTP API.

## Transaction boundaries (design contract for later phases)

One business command owns one outer `with session.begin()` transaction. Request dependencies provide and close sessions; services explicitly begin and commit. Repositories may flush but cannot commit. Exceptions roll back the whole command; response construction happens after successful commit. Never reuse an implicit read transaction and then begin a nested business transaction by accident.

Receiving goods eventually atomically writes receipt status, stock movements, valuation, payable journal, audit event, and idempotency result. Posting a sale atomically writes invoice state, stock issue, COGS, receivable/revenue/tax journal, and audit event. A warehouse transfer writes both stock legs atomically; in-transit ownership is explicit for delayed transfers. Production completion atomically records material consumption, yield/scrap, finished stock, batch genealogy, valuation, and WIP release.

Phase 5 may create draft orders and invoices before Phase 6 accounting exists. Financial posting must remain disabled until the accounting posting engine is available; never partially post inventory or expose a successful financial posting in the meantime.

Use unique document/idempotency constraints and row locks on stock balance/valuation rows. Lock rows in stable product/location order to avoid deadlocks. Retry an entire command for recognized transient deadlocks/serialization failures only, with bounded retries and the same idempotency key. Prevent overselling under concurrency; SQL alone must enforce critical uniqueness and referential integrity. Add an outbox in the same transaction when actual asynchronous side effects arrive. External email and webhooks must not run inside a database transaction.

## Money, quantity, and valuation

Use Python `Decimal`, PostgreSQL `NUMERIC`, and decimal strings over JSON. Never derive money from binary float; parse decimal input strings and reject nonfinite values. Proposed money/unit costs use NUMERIC(20,6), quantities NUMERIC(20,6), exchange rates NUMERIC(20,10). Round at documented document/tax boundaries using the currency's minor units and an explicitly chosen rounding policy (initial proposal: ROUND_HALF_UP, subject to jurisdiction review). Store original currency and exchange rate with immutable base-currency postings. JavaScript must not calculate posted balances with Number; server results are authoritative.

The initial proposed valuation is perpetual moving weighted average per product and warehouse, with cost carried across transfers. Reservations change available quantity, not on-hand or valuation. Backdated stock movements into closed periods and negative physical stock are initially disallowed. Returns link original movement and cost; approved adjustments require reasons and paired accounting. FIFO needs explicit cost layers if selected later; do not mix valuation policies silently. See database blueprint and inventory rules.

## Financial immutability and traceability

Posted journal headers/lines and posted stock movements are append-only. Corrections use linked reversals and replacement documents, never edits/deletes to posted rows. Only drafts may change. Financial periods can be locked; postings must balance in base currency before commit. Enforce posting restrictions in both services and database protections in the accounting phase.

Batch lineage links supplier lots, receipts, material issues, work orders, production batches, finished lots, quality decisions, shipments, and returns. Serial-tracked electrical meters and applicable spare parts get unique serial identities separate from lots. Quarantined stock is not saleable. Preserve source-document references and actor/time context. Cost adjustments must retain the original traceable posting and add adjustment entries.

## Operations and limitations

Liveness does not connect to PostgreSQL. Readiness performs `SELECT 1`, returns 503 on connection/query failure, and does not assert schema revision or business readiness. Compose applies Alembic explicitly before API startup. No automatic `create_all` or auto-migration in application lifespan. The baseline creates no business tables.

Logs are JSON and contain request ID, method, path (without query), status, and elapsed milliseconds. Exceptions return safe envelopes, omit validation input values, and include a generated request ID. Credentials, authorization headers, and database errors are not returned to clients. CORS uses explicit origins, and the global wrapper includes error responses. Themes are browser-local, status history is memory-only, and readiness is public with no server details.
