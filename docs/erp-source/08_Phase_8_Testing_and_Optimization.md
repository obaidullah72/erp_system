# Phase 8 — Testing and Optimization

## Goal

Verify the complete ERP as an integrated system, improve measured bottlenecks and prepare a repeatable deployment and recovery process.

## Prerequisites

Phases 1–7 pass their individual checks. All required workflows use connected APIs and persisted data. Maintain a list of unresolved issues and production configuration decisions.

Testing also happens throughout earlier phases; this phase adds system-wide and operational verification.

## Verification scope

| Area | Required evidence |
| --- | --- |
| Unit | Money/quantity rounding, costing, allocation, totals, BOM scaling and status rules |
| API | Validation, auth, permissions, filtering, pagination and error behavior |
| Integration | Inventory/accounting/document atomicity, payments, returns and production |
| Database | Constraints, migrations, idempotency, locks and concurrency |
| Frontend | Key workflows, form errors, loading/empty states and permission behavior |
| Reports | As-of totals, balance equations, subledger/GL reconciliation and exports |
| Operations | Startup, migrations, worker retries, backups, restore and monitoring |
| Performance | Representative dataset/query measurements and agreed load targets |

Use PostgreSQL for tests that depend on real locking, numeric behavior and constraints. Keep pure unit tests separate from integration tests for useful feedback.

## End-to-end reference scenario

1. Configure business settings, accounts, roles, units and warehouses.
2. Create products, raw materials, customers and suppliers.
3. Post balanced opening stock and party balances without duplication.
4. Order 100 units; receive 40 and later 60, matching invoices once.
5. Post a credit sale, receive a partial payment and verify receivables.
6. Complete a cash POS sale and verify revenue, cash, cost and stock.
7. Post a customer return and supplier return with correct disposition.
8. Transfer stock, perform a physical count and approve a variance.
9. Manufacture a finished batch using material batches, labor and overhead.
10. Record wastage and rejected output, then release acceptable goods.
11. Reconcile cash/bank records and close a fiscal period.
12. Compare stock valuation, party ledgers, trial balance, P&L, balance sheet and cash flow.
13. Generate PDF/Excel reports and verify totals.
14. Restore a backup into an isolated environment and repeat reconciliation.

## Failure and concurrency checks

- Repeat finalization, payment, return and production completion requests after simulated response loss.
- Reject idempotency key reuse with a different payload.
- Race sales against the last available stock; only permissible quantities commit.
- Simulate an accounting failure after stock changes are staged; the full transaction rolls back.
- Simulate worker retries without duplicate scheduled production, reminders or exports.
- Verify expired/revoked authentication and direct unauthorized object access.
- Reject invalid units, missing account mappings, closed-period postings and invalid batch assignments.
- Verify period controls cannot be bypassed through imports or backdated operational APIs.
- Reconcile raw materials, work in progress, finished stock and losses after partial production.

## Optimization work

Use representative data volumes and agree on expected concurrency/response targets. Capture baseline measurements before adding indexes, eager loading, cache or aggregates.

Review query plans, N+1 access, slow reports, payload size, stock-lock duration, worker throughput and frontend rendering. Preserve audit, transaction and accounting controls while improving performance. Re-run only relevant benchmarks after changes.

## Security and operational preparation

Review password/token handling, CORS, permissions, file upload validation, export authorization, rate limiting, secret management, dependency findings and log redaction.

Create environment-specific configuration, HTTPS/reverse-proxy setup as needed, database migration procedure, health checks, monitoring and alerts. Keep credentials outside source control.

Back up database and required attachments, document retention objectives and prove a restore. Record recovery-time/recovery-point objectives agreed with the business rather than inventing guarantees.

Provide a deployment runbook with preflight validation, backup, migration, application/worker startup, readiness checks, smoke tests and rollback/recovery actions. Treat data migrations as potentially non-reversible; an application rollback must not assume automatic schema rollback.

## Supporting data and APIs

No new major business module is required. Add operational job metadata or request tracing only if justified. Existing health/readiness endpoints and permission-aware monitoring should support deployment checks. Avoid exposing internal operational detail publicly.

## Deliverables

- Executable critical test suite and recorded results.
- Representative fixtures and reconciliation report.
- Resolved defect list with any accepted limitations.
- Performance measurements and changes justified by evidence.
- Clean-install and upgrade migration evidence.
- Docker/environment configuration and deployment runbook.
- Backup/restore verification and monitoring configuration.
- User/admin documentation for core workflows.

## Final exit criteria

All critical business and permission checks pass. Stock, batches, receivables/payables and GL reconcile. Cash/credit behavior and historical reports remain correct. Fresh installation and upgrade work. Backup restoration is demonstrated. Deployment configuration is complete, and no material integrity defect remains.

This documentation pack does not authorize publishing or claim that a live deployment occurred; actual implementation and release actions are separate work.
