# Incremental ERP roadmap

The expanded Stage 1 supersedes the original narrow Phase 1 scope: identity, foundation tables and the minimal posting kernel are now included. This does not imply the later business modules are complete.

| Stage | Scope / remaining work | Acceptance gate |
|---|---|---|
| 1 Foundation | Connected login/shell, live RBAC, tenant configuration, foundation migrations, journal kernel, full domain/API baseline, runtime and verification | Clean install/start, authorization, migration, journal invariants, browser checks |
| 2 Identity extensions | Password reset/MFA/rate limiting, organization membership extensions as required; core identity already implemented | Abuse, recovery and policy tests |
| 3 Master data | Products/categories/brands/units, warehouses, partner roles, employees, fitments and lot/serial policy | Tenant CRUD, versions, uniqueness, audit |
| 4 Inventory | Movements, balances, reservations, transfers, valuation, lot/serial tracking | Concurrent overselling prevention, cost reconciliation, rounding |
| 5 Purchasing/sales/POS | Orders, receipts, invoices, tenders, tax/pricing rules and stock/ledger orchestration | Atomic source+stock+journal; source uniqueness and retries |
| 6 Accounting extensions | Chart management, periods, reversals, FX, bank/allocations/reconciliation and statements | Period locks, reversal invariants, financial reconciliation |
| 7 Manufacturing | BOM, schedules, WIP, consumption/completion, genealogy, quality, scrap/rework and costing | Traceability, yield/cost reconciliation and atomic posting |
| 8 Reporting | Actual dashboards, reports, authorized exports | Totals reconcile; missing metrics explicit; performance |
| 9 Hardening | Security/load/restore review, release automation and production operations | Restore drill, monitoring, key rotation and rollback rehearsal |

Redis/Celery is configured in Stage 1 but only diagnostic ping exists. Add an outbox and retry-safe consumers when real asynchronous jobs arrive. Existing empty files and module grants are scaffolding, not feature implementations. Financial source posting stays unavailable until each complete source workflow and all dependencies are implemented, even though the internal kernel is ready.
