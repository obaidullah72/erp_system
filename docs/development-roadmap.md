# Nine-phase implementation roadmap

Only Phase 1 is implemented in this release. Each later phase needs its own schema, authorization, transactions, tests, and acceptance review. Dates and production readiness are not promised.

| Phase | Scope | Acceptance gate |
| --- | --- | --- |
| 1 — Foundation | Valid manifests, React shell/theme/routes, Tailwind v4, Axios, real health page, FastAPI config/logs/errors/CORS, PostgreSQL sessions, Alembic baseline, JWT utilities, Docker and docs | Frontend builds; API starts; independent liveness and real database readiness verified; unavailable checks disclosed |
| 2 — Database & authentication | Identity models/migrations; password hashing; login/logout; token rotation/revocation policy; active-user checks; roles/permissions; audit identity | Authentication abuse and authorization tests; no default admin credentials; migrations and secure bootstrap verified |
| 3 — Master data | Products/categories/brands/units, warehouses, partner customer/supplier/vendor roles, employees, settings, fitments and serial/lot policies | Validated CRUD, uniqueness, company boundaries, referential integrity and audit coverage |
| 4 — Inventory | Immutable movements, balances, reservations, transfers, returns, adjustments, lot/serial handling and valuation engine | Concurrent overselling prevention; reconciliation; transfer cost invariance; returns and rounding tests |
| 5 — Purchasing, sales & POS | Orders, receipts, draft invoices, POS session/tenders, pricing/tax contracts and document numbering | End-to-end draft workflows; idempotency; stock integration tests; financial posting remains gated until Phase 6 |
| 6 — Accounting | Chart of accounts, immutable balanced journals, periods/reversals, integrated purchasing/sales posting, cash/bank, receivables/payables, expense/allocation/reconciliation | Atomic document+stock+journal posting; period locks; debit/credit balance; immutable posting and reversal tests |
| 7 — Manufacturing | Raw materials, versioned BOMs, schedules, WIP, production batches, quality/quarantine, scrap/rework, actual costing and genealogy | Lot-to-shipment recall, yield/cost reconciliation, serial traceability, atomic consumption/completion |
| 8 — Dashboard & reporting | Real sales/stock/finance/manufacturing reports, filters, exports and permission-scoped dashboards | Totals reconcile to ledgers; no simulated production metrics; query and export performance verified |
| 9 — Hardening & deployment | Security review, end-to-end/load/restore tests, observability, release automation, backup rotation and deployment runbooks | Restore drill, load budgets, production configuration, key rotation and rollback rehearsal |

Redis/Celery may be introduced for measured needs such as large exports or scheduled reports. Use an outbox and retry-safe consumers when asynchronous work is justified. Do not add infrastructure merely to satisfy future file scaffolds.

Phase 1 deliberately excludes real login, business forms, posting, sales dashboards, inventory operations, employee management and reports. The roadmap UI labels all later work as planned.
