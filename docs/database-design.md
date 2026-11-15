# Database blueprint — proposed, not migrated

Phase 1 contains an empty Alembic baseline and no business tables. `alembic upgrade head` creates Alembic's revision table only. The following is the target relational blueprint for later phases, not a claim that any domain exists today.

## Shared conventions

Use UUID primary keys; UTC `TIMESTAMPTZ`; explicit foreign keys; stable unique business codes; optimistic version fields for editable drafts; and non-null actor/timestamps. Put `company_id` on business documents and relevant master records, and include it in business uniqueness and foreign-key boundaries. Start with one company; multi-company access control must be designed and tested before enabling it. Branches and warehouses are explicit locations. Avoid premature sharding and generic JSON storage for financial facts.

Use NUMERIC(20,6) for money/unit cost and quantity, NUMERIC(20,10) for FX rates, currency ISO codes, and decimal JSON strings. Quantize posted currency totals to the currency's minor units. Enforce finite values, quantity sign rules, and currency consistency. Use date-only fields for accounting dates and UTC instants for events.

## Proposed entities and relationships

| Domain | Entities and principal constraints |
| --- | --- |
| Identity | users, roles, permissions, user_roles, role_permissions; unique normalized email; active/disabled state; hashed passwords; revoked refresh-token hashes if refresh is introduced |
| Organization | companies, branches, employees, settings; employees optionally link users; settings scoped by company |
| Catalog | products → category, brand, base_unit; units and product_unit_conversions; product codes/barcodes unique per company; variant/fitment attributes for spare parts; stock/service/raw/finished classification |
| Locations | warehouses → branch; bins → warehouse; no warehouse deletion with posted history |
| Partners | partners with customer/supplier/vendor roles and role-specific terms; contact/address children; one legal party can have multiple roles without duplicated balances |
| Stock | stock_movements → product, warehouse/bin, lot/serial, source document and line; inventory_balances unique by product/location/lot/status; reservations → demand line and expiry; transfer headers/lines link both movement legs |
| Stock corrections | returns reference original receipt/issue; adjustment documents require reason, approval and journal linkage; no direct balance edits |
| Purchasing | purchase_orders/lines; goods_receipts/lines → order lines; supplier_invoices/lines → receipts; supplier_credit_notes link originals; supplier identity is a partner role |
| Sales/POS | sales_orders/lines; shipments/lines; sales_invoices/lines; credit_notes; pos_sessions, tills and tender records; invoice and payment references are independently unique |
| Accounting | accounts, fiscal_periods, journal_entries, journal_lines, payment_allocations, bank_accounts, bank_transactions, expenses and reconciliations; journal line references one account, base currency debit/credit and partner when relevant |
| Manufacturing | bom_versions/lines → products; work_orders → frozen BOM revision; schedules; material_issues/lines; production_batches; batch_material_links; completions; quality_inspections; scrap and rework; cost_allocations |
| Traceability | lots → product and supplier/manufacturing origin; serials unique per company/product or globally per manufacturer's policy; serial movement history; batch genealogy is explicit many-to-many |
| Governance | audit_events append-only with actor, action, source identity and request ID; idempotency_records unique by company/operation/key with request hash; future outbox_events commit with business command |

Customer/supplier ledgers, receivables, payables, and general-ledger reports derive from posted journals and allocation records. Do not create independent editable balance tables as a competing source of truth. Cached projections require reconciliation back to journals.

## Posting and concurrency

Document states are explicit: draft → approved (where needed) → posted → reversed. Posting acquires a document lock, verifies expected state/version and unlocked fiscal period, validates stock/cost/tax and permission policy, writes all stock/financial/audit facts in one transaction, and marks the document posted. A unique source-document posting constraint and idempotency key prevent duplicate postings. Reusing a key with a different request hash must fail.

Journal lines require exactly one positive debit or credit; each posted entry must balance in base currency. An aggregate balance cannot be enforced with a simple row CHECK: implement transactional posting validation plus deferred database enforcement and post-state mutation triggers in Phase 6. Posted journals and stock movements cannot be updated/deleted; reversal entries reference originals. Draft deletion must not cascade into posted facts. Closed periods reject backdated postings.

Inventory balances are projections maintained under row locks in the same transaction as append-only movements. Available = saleable on-hand − active reservations; quarantine is excluded. Initial policy rejects negative stock. Use stable row lock ordering and unique constraints to handle first-insert races. Transfers preserve carrying cost; returns reverse original cost; manufacturing moves raw material to WIP then finished goods with auditable variance allocation.

## Valuation and batch genealogy

Proposed initial method: perpetual moving weighted average by product/warehouse. Receipt cost includes documented landed costs. Issue cost uses the locked current carrying cost; last-unit depletion must clear residual rounding value. Late cost adjustments generate linked value adjustments, never rewrite movements. FIFO is an alternative requiring explicit cost layers and separate policy approval. No silent switching or backdated recalculation across closed periods.

Every material consumption row records source lot, quantity, unit and cost and the destination production batch. Finished lots link completion documents and the same batch. Quality status and releases are recorded as events. Partial consumption, split/merge, scrap, rework and returns preserve lineage; immutable serial movements support targeted recall. Validate lot/product consistency and unit conversion precision. Prevent cycles in genealogy at the service boundary.

## Indexes, migrations, and access

Index foreign keys, normalized lookup codes, date/document filters, journal account/date, partner/date, stock product/warehouse/time, and lot/serial lookup paths. Use partial indexes for open reservations and draft/unpaid operational queues where justified by query plans. Keep audit and journal history; archive policies require explicit retention decisions.

Register concrete SQLAlchemy models in Alembic's env as they are implemented. Review generated migrations, name all constraints, test upgrades on a copy and verify backup/restore. Never run `create_all` in production. Production application credentials should have least privilege; a separate migration role handles DDL, and posting protections must apply to the runtime role.
