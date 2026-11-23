# ERP source phases and delivery checkpoints

Use the populated [source pack](erp-source/00_README.md) and [requirements traceability](requirements-traceability.md). The earlier nine-phase roadmap and empty placeholders are superseded as requirement sources. Preserve prior Stage 1 completion evidence separately.

## Source dependency order

| Source phase | Required scope | Acceptance gate |
|---|---|---|
| 1 Foundation | Platform, identity, nine confirmed roles, configuration, journal kernel | Auth, migrations, permissions, balanced/idempotent posting and connected shell |
| 2 Master Data | Products, units/conversions, classifications, warehouses, shared parties and opening drafts | Validated persisted masters, tenant boundaries, uniqueness, archival and image controls |
| 3 Inventory | Immutable movements, balances, reservations, batches, FIFO/FEFO allocation, valuation, transfers, counts and alerts | No overselling, atomic rollback, historical costs and stock/GL reconciliation |
| 4 Purchases and Sales | Orders, partial receipts, matching, invoices, POS, settlements and returns | Atomic source/stock/journal effects; cash and credit remain distinct |
| 5 Accounting | Account mappings, periods, GL, AR/AP, statements, expenses, cash/bank and reconciliation | Financial equations, historical aging, protected postings and period controls |
| 6 Manufacturing | BOM versions, schedules, orders, batch consumption/output, costs, quality and genealogy | Raw/WIP/finished/loss reconciliation, quality gates and idempotent completion |
| 7 Reports and Analytics | Dashboard and exact 40 reports, drill-downs, filters, PDF/Excel jobs | Independent totals, snapshot history, authorized complete exports and measured queries |
| 8 Testing and Optimization | Full reference scenario, failure/concurrency, security, performance and recovery | Actual critical-test evidence, restore drill, startup/upgrade and operational readiness |

The source phases are dependencies, not permission prompts. The user's delivery Stages 2–5 are separate checkpoints: complete frontend, complete backend in dependency order, connect every workflow, then comprehensive verification/readiness. Continue authorized work through the checkpoints; do not infer business completion from UI scaffolds.

## Current boundaries

The existing Stage 1 record covers foundation behavior. Operational services and report calculations are not implemented; their UI workspaces expose honest unavailable states. Redis/Celery currently provides only a diagnostic task. No business export/reminder/alert delivery is verified. Add after-commit scheduling and deduplication with real services. Exact source coverage is now indexed; this does not change any pending business acceptance result.
