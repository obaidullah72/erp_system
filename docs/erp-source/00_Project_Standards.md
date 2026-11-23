# Business ERP — Shared Architecture and Delivery Standards

These requirements apply to every phase.

## Required stack

| Layer | Required technologies |
| --- | --- |
| Frontend | React, Vite, JavaScript ES6+, Tailwind CSS v4, React Router DOM |
| Forms and requests | React Hook Form, Zod, Axios |
| Visual components | Recharts, Lucide React, date-fns |
| Backend | Python, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic |
| Database | PostgreSQL |
| Authentication | JWT with server-enforced permissions |
| Background work | Redis and Celery or a documented equivalent |
| Operations | Docker, Docker Compose, environment configuration, structured logs |

Select compatible dependency versions during implementation and commit lockfiles. The original setup commands are preserved in the requirements file; review compatibility before execution. This documentation task does not execute those commands.

## Repository and responsibilities

Use business-erp/frontend and business-erp/backend, with root-level operational configuration and documentation.

- Frontend: components/common, forms, tables, charts, modals and layout; pages by business module; layouts, services, hooks, context, utils, constants, validations and routes.
- Backend: app/api/v1/endpoints, core, database, models, schemas, repositories, services, dependencies and utils; alembic and tests.
- Routers handle transport and authorization dependencies. Pydantic schemas handle request and response validation.
- Repositories handle persistence; services enforce business rules and coordinate transactions. Avoid repositories that silently commit.
- The initiating service owns the database transaction. Commit related document, stock, financial and audit records together.
- Background workers handle exports, reminders and alerts after commit. They must not be the only mechanism guaranteeing stock or financial integrity.

Document APIs with FastAPI OpenAPI and meaningful response models.

## Data and transaction invariants

1. Use PostgreSQL NUMERIC and Python Decimal for money, quantities and rates with explicitly chosen scales. Exchange decimal values as strings where JavaScript arithmetic could lose precision.
2. Store dated business events and UTC timestamps. Apply the configured business timezone when grouping days and generating schedules.
3. Give operational documents unique business-scoped numbers; use internal immutable identifiers for relationships.
4. Snapshot transaction prices, discounts, taxes, unit conversion factors and costs. Later edits to master data must not rewrite history.
5. Keep finalized stock and financial history immutable. Corrections use linked reversals, returns or adjustment documents.
6. Require balanced journal entries for financial events. Validate balance at the posting boundary and prevent later direct edits.
7. Reject negative stock unless an authorized administrator explicitly enables it. Audit policy changes and enforce the same rules across every entry point.
8. Prevent concurrent overselling with transaction locking or another demonstrated equivalent; a frontend stock check is insufficient.
9. Use idempotency keys on posting/finalization, payments, returns and production completion. Persist the request fingerprint and result; reject conflicting reuse.
10. Preserve transaction references and actor identity across documents, inventory movements, batch movements, journal entries and audit records.
11. Make stock balances and party balances reconcile to their authoritative movement and financial records.
12. Verify object access and module/action permissions on the backend. Hidden buttons do not authorize requests.

## Proposed domain conventions

Use a stock transaction header and immutable movement lines. Record product, warehouse, base-unit quantity, unit cost, value, batch where relevant, source document, effective date and actor. Maintain stock balances transactionally as an acceleration layer.

Keep stock allocation separate from valuation. Physical FIFO selects older stock; FEFO selects the earliest eligible expiry. The financial valuation method is a separate business setting. Do not silently change it after posted activity.

Use journal entries with at least two journal lines, account, debit or credit, source document and posting date. Entries must balance at configured precision. Business documents reference their posting records.

Customer and supplier ledgers are controlled views or subledgers backed by posted financial events. Do not maintain an unrelated editable balance field as the source of truth.

Recommended document flow: draft → approved where configured → posted/finalized. Document cancellation either discards an unposted draft or creates a linked reversal of a posted document. Define the exact allowed transitions for each module.

## API conventions

All phase routes below are proposed contracts under /api/v1. Resolve names consistently in OpenAPI during implementation.

- Use bounded pagination, explicit filters and stable ordering on lists.
- Return consistent validation and business-error envelopes with a request identifier.
- Use 401 for missing/invalid authentication, 403 for forbidden actions, 404 for inaccessible/missing resources, and 409 for state or idempotency conflicts where appropriate.
- Validate quantities, payment allocation totals, dates, statuses and required fields on the server.
- Restrict export, approval, reversal and configuration operations explicitly.
- Version important updates or lock records to reject stale edits.
- Do not expose stack traces, credentials or token values in errors or logs.

## UI standards

Provide a responsive dashboard layout, sidebar, top bar, reusable forms, searchable paginated tables, date and dropdown filters, confirmation dialogs, loading and empty states, useful validation, toast notifications, accessible focus behavior, and persisted light/dark mode.

Every action must call a real API or clearly display that it is unavailable. Disable duplicate submission while requests are pending, then display persisted results from the API. Keep accounting terminology clear for shop operators.

## Financial integration contract

Define a posting service that accepts a typed business event and source identifier and returns a posting reference. Validate account mappings, period status and idempotency before stock or financial mutations become final.

Typical events include opening_inventory, stock_adjustment, goods_received, supplier_invoice, sale_posted, payment_received, payment_sent, sales_return, purchase_return, production_consumed and production_completed.

| Event | Example debit | Example credit |
| --- | --- | --- |
| Opening inventory | Inventory | Opening balance clearing/equity |
| Goods received before invoice | Inventory | Goods received not invoiced clearing |
| Matched supplier invoice | Receipt clearing and recoverable tax where configured | Accounts payable |
| Credit sale | Accounts receivable | Sales and output tax where configured |
| Sale cost | Cost of goods sold | Inventory |
| Customer payment | Cash/bank | Accounts receivable |
| Supplier payment | Accounts payable | Cash/bank |
| Production consumption | Work in progress | Raw material inventory |
| Production completion | Finished goods inventory | Work in progress |

These are implementation examples, not jurisdiction-specific accounting policy. Discounts, purchase costs, variances, tax recoverability, wastage and opening balances need explicit configured treatment. Recognize receiving and supplier invoicing separately so inventory is not counted twice.

## Verification and phase completion

Critical checks cover authorization, database constraints, atomic rollback, duplicate requests, concurrent requests, decimal rounding and historical reporting. Test against PostgreSQL for locking and database behavior.

Document meaningful success and failure cases in each phase. Keep a repeatable fixture set for cash/credit sales, partial receipts, partial settlements, returns and production. Record actual test results only after execution.

Never advance with broken posting integrity, disconnected frontend workflows, unapplied migrations or undocumented material blockers.
