# ERP domain design baseline

Stage 1 implements only identity, business configuration, governance, and the journal posting kernel. Every other entity below is a design contract for an incremental migration. `business_id` is the tenant boundary (replaces the earlier proposed `company_id`). A user belongs to exactly one business; cross-business administration is not implicitly granted by any role.

## Shared invariants

UUID keys, UTC timestamps, date-only accounting dates, tenant-scoped unique codes, and foreign keys are mandatory. Tenant-owned parents expose `(business_id, id)` unique keys; children use composite foreign keys so foreign-tenant references fail in PostgreSQL. Editable resources use positive integer `version`; updates require the last observed version and return 409 on conflict. Disabled masters remain referenceable by history, but cannot receive new activity. No cascade deletion of financial history.

Money and quantities use NUMERIC(20,6), FX NUMERIC(20,10), and JSON decimal strings. Currency is a three-letter uppercase code; initial posting accepts only the business base currency and exact two-decimal amounts. Additional currency scales and FX are future work, not inferred silently. Values must be finite, bounded, and explicit. Journals require at least two lines, exactly one positive debit/credit per line, and equal totals. Immutable journal facts are protected by PostgreSQL triggers as well as the service. Business currency cannot be changed after the first posting.

## Ownership, entities, dependencies and indexes

All named operational entities are business-owned unless marked global. Every FK needs an index unless covered by a leading unique/index key. Dates on queue/report indexes follow business_id.

| Owning module | Entities and relationships | Constraints and principal indexes | Dependencies |
|---|---|---|---|
| Settings | businesses; business_settings 1:1 business; future branches N:1 business | business slug global unique; one settings row; positive version; base currency immutable after posting | none |
| Identity | users N:1 business; roles N:1 business; permissions global catalogue; user_roles and role_permissions M:N; auth_sessions N:1 user | normalized email unique per business; same-business role membership; role name per business; refresh hash unique; session expiry/revocation; user and expiry indexes | settings |
| Audit | audit_logs N:1 business, optional actor; document_sequences by business/type/year; idempotency_records by business/operation/key | append-only audit; no credentials/payloads; request ID; source/date index; sequence positive and locked atomically; request SHA256 and result identity | identity |
| Categories/brands/products | categories tree; brands; units; products → category/brand/base unit; conversions; fitments | codes/barcodes unique per business; conversion > 0; no category cycles; product kinds stock/service/raw/finished; product lookup index | settings |
| Warehouses | warehouses → branch; bins → warehouse | location code unique; no removal with history | settings, products |
| Customers/suppliers/vendors | partners; partner_roles; addresses/contacts; customer/supplier/vendor terms | one party, multiple roles; role uniqueness; credit terms nonnegative; normalized lookup | settings |
| Employees | employees → optional user, branch, cost centre | employee code unique; one optional employee/user link; active status | identity, settings |
| Inventory | stock_movements; inventory_balances; reservations; transfers/lines; cost_adjustments | movement source/line/leg unique; balance unique product/location/lot/status; no negative stock; reserve > 0; active reservation expiry index | products, warehouses, batches, accounting |
| Batches | lots; serials; lot_genealogy; serial_movements | lot code/product unique; serial unique per business; product/lot consistency; genealogy acyclic; origin and downstream indexes | products, inventory |
| Purchasing | purchase_orders/lines; goods_receipts/lines → order lines; supplier_invoices/lines → receipts; landed_costs | document number and external invoice per supplier unique; received/invoiced quantities cannot exceed permitted amounts; supplier/date/state index | partners, products, stock, accounting |
| Sales | sales_orders/lines; shipments/lines → order lines; sales_invoices/lines → shipments | number unique; fulfillment bounded; customer/date/state; tax snapshots frozen | partners, products, stock, accounting |
| POS | pos_sessions; tills; tender_records; pos_sales → sales invoice | one open session per till; tender external reference unique; cash variance recorded at closure | sales, cash_bank, identity |
| Returns/adjustments | customer_returns; supplier_returns; stock_adjustments; lines → original movement/document | returned quantity ≤ original less prior returns; reason/approval mandatory; original source index | purchases, sales, stock, accounting |
| Chart of accounts | accounts → optional parent; future account_mappings and fiscal_periods | account code unique per business; parent same tenant; kinds asset/liability/equity/income/expense; posting leaf/active validation; periods nonoverlapping | settings |
| Accounting | journal_entries; journal_entry_lines → account; future reversal links | source type/id/event unique per business; balanced deferred constraint; immutable; business/date and account/entry indexes | accounts, identity, governance |
| Cash/bank | bank_accounts → GL account; payments/receipts; bank_transactions; reconciliations | external bank transaction unique; reconciliation totals agree; account/date index | accounting, partners |
| Credit/debit | credit_notes/debit_notes/lines → original invoice | reason and original references; cap credit against unsettled/returned amount; number unique | sales, purchasing, accounting |
| Expenses | expenses/lines; attachments; approvals | expense number unique; amount > 0; payee/account/category valid; date/state index | partners, accounting, employees |
| Receivables/payables | payment_allocations → payment and invoice | allocation > 0; aggregate capped at both unallocated balances under locks; invoice/date index | sales, purchases, accounting, cash_bank |
| Customer/supplier/general ledgers | read projections of journal lines, partner references and allocations | never independently editable balances; business/partner/date and business/account/date | accounting, allocations |
| Financial statements | trial balance, P&L, balance sheet, cash flow read models | period filters; reconciled to posted journals; retained earnings treatment explicit | accounts, journals |
| BOM | bom_versions → finished product; bom_lines → material product/unit | unique product/revision; positive yields/quantities; no recursive component cycles; only one effective approved revision per interval | products, units |
| Production planning | work_orders → frozen BOM; schedules; capacity allocations | target quantity > 0; unique order; resource/time queue indexes | BOM, stock, employees |
| Manufacturing | material_issues/lines; completions; scrap/rework documents | bounded consumption/yield; each source posted once; WIP tracked by work order | planning, stock, batches, accounting |
| Quality control | inspections; samples; quality_events; releases | pending/pass/fail decision; actor/time mandatory; quarantined stock cannot ship; lot/status index | batches, manufacturing, stock |
| Production costing | cost_allocations; cost_runs; variance journals | no double allocation; material/labour/overhead totals reconcile to WIP; work-order/run unique | manufacturing, expenses, accounting |
| Dashboard/reports | query services; future export_jobs and report_snapshots | permission-filtered tenant reads; as-of timestamp; no invented metrics; job owner/status index | implemented source modules only |

## State transitions

- Business/user/master: active → disabled → active. User disable revokes all sessions. No hard deletion API.
- Session: active → rotated (old refresh secret invalid); active → revoked or expired. Access JWT always resolves the live session and active user. Logout revokes the entire session immediately.
- Role: protected Super Admin/Admin role (immutable grants) or configurable responsibility/custom role (versioned grants). Membership updates are versioned; last active Super Admin cannot be removed or disabled. Grant changes take effect on the next request.
- Order: draft → approved → partially fulfilled → fulfilled → closed; cancellation only for unfulfilled remainder. Optimistic version on draft edits; lock during fulfillment.
- Receipt/shipment/invoice/expense/adjustment: draft → approved → posted → reversed. Reversal is a new linked document; posted records are never edited. Approval requirements are module policy.
- Transfer: draft → dispatched → received, with stock owned in transit; immediate transfers commit both legs together.
- Reservation: active → consumed/released/expired. A partial release preserves remaining quantity.
- BOM: draft → approved → retired. Work orders retain the approved snapshot.
- Work order: draft → released → in_progress → completed → closed; cancellation only with explicit WIP/material unwind.
- Lot quality: quarantine → released/rejected; later recall blocks availability without rewriting history.
- Fiscal period (future): open → soft_closed → locked. Reopen requires privileged audited action. Stage 1 provides a period-policy interface, with an explicitly open policy until periods are implemented.

## Transactions and concurrency

One application command owns the outer transaction, including audit and idempotency results. Request database dependency begins/commits/rolls back; domain services flush only and can be composed by a future command orchestrator. Authentication reads use that same transaction. Posting uses a savepoint so a duplicate or integrity failure never leaves partial kernel writes even when the caller catches the domain error. Caller rollback removes successful posting and its result record together.

Posting locks business configuration before validating base currency; source uniqueness and idempotency uniqueness are enforced by database constraints. Same key + same canonical payload returns the original entry. Same key + different payload or different key + same source returns 409. No financial endpoint is exposed yet; internal callers must authorize their source command before invoking the kernel. Mappings must exactly cover the typed event's lines and resolve to active same-business accounts.

Purchase receiving/invoicing commits source state, stock/cost facts, journal, audit and idempotency together once all services exist. Sales posting commits invoice, stock issue, COGS, revenue/tax/receivable journal and audit together. Payments lock invoice and payment before allocating. Manufacturing completion commits consumption, yield/scrap, genealogy, finished stock, WIP release and variance together. Stock rows lock in sorted product/location order; no external network requests inside transactions. Email/export integrations will use a transactional outbox in a later migration; current worker only has a diagnostic ping task.

Retry the complete transaction for PostgreSQL 40001/40P01 only, with bounded jitter and the same idempotency key. Never retry validation, permission, closed-period, or conflicting-payload errors. Tenant context always comes from authenticated identity; never trust a request's business_id for authorization.

## Incremental rollout

0001 preserves the existing empty baseline; 0002 creates only foundation tables and immutable journal/audit protections. Next migrations add master data, stock, documents, accounting extensions, manufacturing, then projections/jobs. Empty module scaffolds are not registered routes. Inventory exposes only Protocol contracts and raises no false success. The foundation does not implement taxes, inventory valuation, period administration, FX, banking, reports or manufacturing workflows.
