# Business ERP — All Eight Development Phases

Prepared: 20 November 2026. Based on your supplied ERP specification.

This is a development specification, not an implementation completion report. The companion ZIP contains individual phase files and the original requirements.

## Phase index

1. Phase 1 — Foundation
2. Phase 2 — Master Data
3. Phase 3 — Inventory
4. Phase 4 — Purchases and Sales
5. Phase 5 — Accounting
6. Phase 6 — Manufacturing
7. Phase 7 — Reports and Analytics
8. Phase 8 — Testing and Optimization

---

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


---

# Phase 1 — Foundation

## Goal

Create a runnable, modular ERP foundation with PostgreSQL, authentication, permissions, initial migrations and a professional dashboard layout. Establish shared data integrity and financial posting infrastructure before transactional modules depend on it.

## Prerequisites

Read the original requirements and shared standards. Inspect any existing repository before generating files. Confirm the business configuration assumptions and select compatible dependencies without hardcoding credentials.

## Scope and implementation order

1. Initialize the React/Vite frontend and FastAPI backend under business-erp.
2. Configure Tailwind CSS v4 through its Vite plugin, routing, Axios, forms, validation, icons and charts.
3. Create the required backend layers and frontend module folders.
4. Configure PostgreSQL, SQLAlchemy sessions, Alembic and environment-based settings.
5. Add authentication, server-side permissions, audit infrastructure and the minimal journal posting contract.
6. Build the responsive dashboard shell, login screens, theme toggle and reusable UI primitives.
7. Add Docker Compose, health checks, structured logging and developer documentation.

Use Redis and worker service configuration when required. Separate public web, API, worker and database responsibilities; workers must use the same domain services as synchronous operations.

## Database tables

| Tables | Responsibility |
| --- | --- |
| businesses, business_settings | Base currency, timezone, fiscal year and operational configuration |
| users, roles, permissions, user_roles, role_permissions | Identity and action-level access |
| refresh_sessions | Refresh token/session revocation when this strategy is selected |
| audit_logs | Actor, operation, resource and timestamp for sensitive events |
| document_sequences, idempotency_records | Unique references and safe retry infrastructure |
| accounts, journal_entries, journal_entry_lines | Minimal balanced posting kernel, expanded in Phase 5 |

Create migrations with foreign keys, uniqueness, amount checks and appropriate indexes. Define role defaults: Super Admin, Business Owner, Manager, Accountant, Inventory Manager, Sales Operator, Purchase Operator, Production Manager and Read-only User.

The accounting kernel must enforce balancing through a controlled posting service; a row-level CHECK alone cannot sum all journal lines. Keep journal tables protected from direct uncontrolled writes.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET | /health/live | Process health |
| GET | /health/ready | Required dependency readiness |
| POST | /auth/login | Verify credentials and establish authentication |
| POST | /auth/refresh | Rotate/renew authentication under the selected strategy |
| POST | /auth/logout | Revoke refresh/session credentials |
| GET | /auth/me | Current user and effective permissions |
| GET/POST | /users | Authorized user listing and creation |
| GET/PATCH | /users/{id} | View or update an authorized user |
| GET/POST/PATCH | /roles and /roles/{id} | Permission administration |
| GET/PATCH | /settings/business | Authorized business configuration |
| GET | /dashboard/summary | Real initial metrics or a clear no-data response |

All routes except health checks and authentication entry points require appropriate authorization.

## Backend work

Implement configuration validation, password hashing, token expiration, refresh/session handling, CORS configuration, request IDs and a common error format. Never issue known default passwords or log tokens. Use a controlled first-admin bootstrap process.

Create service boundaries for inventory and accounting even before full workflows exist. Define the posting event contract, source uniqueness, period validation extension points, and transaction ownership. Account mappings used by later phases must fail explicitly when missing.

## Frontend work

Implement AuthLayout and DashboardLayout, protected routes, sidebar navigation and a top bar with user controls. Build reusable inputs, selects, buttons, tables, modals, date filters, toast messages and loading/empty/error components.

Show business dashboard placeholders as “No transactions yet” when appropriate. Do not populate business metrics with fabricated values. Display permission-based navigation while retaining backend enforcement.

## Acceptance checks

- A fresh developer can start the services from the documented instructions.
- Alembic creates a clean database successfully and the application connects.
- Valid login works; invalid credentials and expired authentication fail consistently.
- A Read-only User cannot create users or update settings through direct API calls.
- Session revocation/refresh behavior matches the documented strategy.
- Posting an unbalanced journal fails without committing journal or audit fragments.
- Reusing the same posting source cannot create a second finalized posting.
- Responsive navigation, keyboard focus and theme persistence work.
- Health responses and logs do not expose secrets.

## Deliverables and exit criteria

Deliver the initialized repository, dependency lockfiles, .env.example, Docker configuration, migration history, authentication API documentation and a working connected dashboard shell.

Record actual verification results and setup steps. Exit only when authentication, permission boundaries, clean database initialization and the posting contract are demonstrably usable by later phases.


---

# Phase 2 — Master Data

## Goal

Create the reliable shared records required by inventory, purchasing, sales, manufacturing and accounting.

## Prerequisites

Phase 1 passes its exit criteria. Shared forms, tables, authorization and migrations are available. Decide the base unit and quantity precision rules before stock is introduced.

## Functional scope

### Product catalog

Support unique SKU, name, barcode/QR identifiers, category and subcategory, brand/manufacturer, description, purchase reference price, wholesale/retail price, minimum selling price, minimum stock, image, supplier associations and active/inactive status.

Products may represent motorcycle spare parts, electrical meters, accessories, general trading goods, raw materials and finished goods. Model commercial classification separately from inventory/manufacturing behavior where useful.

Current stock is calculated from inventory records in Phase 3. Product editing must never directly overwrite it. Product history includes material master-data changes and links to later business transactions.

### Units and locations

Support units, product-specific conversions, categories with parent-child relationships, brands/manufacturers and warehouses. Document whether fractional quantities are allowed for each unit.

### Customers, suppliers and vendors

Support profiles, contacts, addresses, credit limits where relevant, due-date/payment-term configuration and opening-balance input staged for controlled accounting posting. One party may have both customer and supplier roles without duplicating its identity unnecessarily.

Opening receivable/payable balances must remain drafts until the accounting posting service validates and posts them. Final historical totals are derived from transactions.

## Database tables

| Tables | Responsibility |
| --- | --- |
| units, product_unit_conversions | Base units, allowed quantities and conversions |
| categories, brands, manufacturers | Classification |
| products, product_images, product_suppliers | Catalog and vendor associations |
| parties, party_roles, party_contacts, party_addresses | Shared customer/supplier/vendor identity |
| customer_profiles, supplier_profiles, vendor_profiles | Role-specific terms and limits |
| warehouses | Stock locations |
| opening_balance_drafts | Controlled party opening balance preparation |

A normalized shared party model is a proposed implementation choice. Separate customer/supplier tables are also acceptable if shared identities and reconciliation remain explicit.

Enforce business-scoped SKU uniqueness, valid prices, positive conversion factors and unique configured identifiers. Block category cycles. Archive referenced master records rather than deleting transaction history.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET/POST | /products | Search/filter products or create |
| GET/PATCH | /products/{id} | Product details and authorized edits |
| POST | /products/{id}/archive | Deactivate with audit |
| GET | /products/{id}/history | Product change and transaction history |
| POST/DELETE | /products/{id}/images and /products/{id}/images/{image_id} | Manage images |
| GET/POST/PATCH | /categories, /brands, /units, /manufacturers | Maintain catalog lookups |
| GET/POST/PATCH | /warehouses and /warehouses/{id} | Maintain warehouses |
| GET/POST/PATCH | /customers, /suppliers, /vendors | Maintain party roles and profiles |
| GET | /parties/{id}/summary | Available activity totals with clear initial state |
| POST | /parties/{id}/opening-balance-drafts | Prepare opening balance for controlled posting |
| GET | /products/{id}/barcode | Produce printable barcode/QR representation |

Define item routes for updates consistently rather than updating an entire collection.

## Backend work

Implement validated models, schemas, repositories and services. Restrict image types and size, store images through a configurable storage abstraction, and prevent user-supplied file paths from controlling storage locations.

Prevent deletion of referenced units, warehouses and parties. Do not allow base-unit conversion changes to reinterpret historical quantities. Return paginated search results and server-derived totals.

## Frontend work

Build searchable product and party tables, detail pages, create/edit forms, image previews, archive confirmation and status filters. Include product unit conversions and supplier associations.

Show customer credit limits and configured terms clearly. Mark opening balances as pending until posted. Display barcode/QR previews and print support. Use consistent server and client validation with useful field-level errors.

## Acceptance checks

- Duplicate SKU or configured unique barcode is rejected, including concurrent requests.
- Invalid prices, zero/negative conversion factors and circular categories fail.
- A party can hold customer and supplier roles while balances stay separate.
- Referenced records are archived or blocked from deletion safely.
- Image validation and permission checks work.
- Searching, filtering and pagination use real backend data.
- Product stock cannot be changed through a catalog update.
- Opening-balance drafts do not silently change financial statements.
- Permission-denied actions fail through direct API requests.

## Deliverables and exit criteria

Deliver connected master-data screens, migrations, documented APIs and a documented unit/party model. Exit when validated catalog, party and warehouse records are available to downstream modules without manual database editing.


---

# Phase 3 — Inventory

## Goal

Track every stock change with a reference, batch/location context, valuation and audit trail. Maintain accurate opening, available, reserved and closing stock.

## Prerequisites

Phases 1–2 pass. Products, units and warehouses exist. Configure the negative-stock policy, valuation method, quantity precision and inventory account mappings.

Although detailed batch manufacturing comes later, this phase must support purchased batches and optional expiry dates now.

## Functional scope

Implement opening stock, authorized stock in/out, adjustments, damage handling, returns-related movement types, reservations, warehouse transfers, physical counts and reconciliation.

Distinguish on-hand, reserved and available quantities. Exclude quarantined/rejected/expired stock from availability according to configured policy.

Opening and closing reports are period calculations from dated movements. They must not reset stock history.

Support low-stock and reorder alerts, product/warehouse stock visibility, and complete movement history. Support FIFO and FEFO physical allocation when applicable, with explicit handling for batches without expiry.

## Database tables

| Tables | Responsibility |
| --- | --- |
| inventory_transactions, inventory_movements | Immutable stock events and signed base-unit movement lines |
| stock_balances, stock_reservations | Transactionally maintained availability |
| batches, batch_stock_balances | Purchased batch identity, dates and warehouse quantities |
| stock_transfers, stock_transfer_lines | Movement between warehouses |
| stock_counts, stock_count_lines | Count sessions and approved variances |
| inventory_cost_layers or inventory_cost_state | Selected valuation implementation |
| alert_rules, alert_events | Reorder configuration and notification history |

Link movement records to product, warehouse, batch, source document and journal reference where financially relevant. Constrain balance identity and batch-product consistency.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET | /inventory/balances | Filter product, warehouse and batch balances |
| GET | /inventory/movements | Paginated movement history and references |
| POST | /inventory/openings | Create controlled opening stock |
| POST | /inventory/adjustments | Record approved correction or damage |
| POST | /inventory/reservations | Reserve available stock for a source |
| POST | /inventory/reservations/{id}/release | Release remaining reservation |
| GET/POST | /inventory/transfers | View/create transfer drafts |
| POST | /inventory/transfers/{id}/post | Atomically post a transfer |
| GET/POST | /inventory/counts | View/create physical count sessions |
| POST | /inventory/counts/{id}/finalize | Post approved count variances |
| GET/POST | /batches | View/create eligible purchased batches |
| GET | /inventory/valuation | Value stock as of a specified date |
| GET | /inventory/alerts | Low-stock and reorder visibility |

## Backend work

Build one inventory service for all modules. Validate product, unit conversion, warehouse, batch status and quantity before posting. Lock balance/cost records consistently to avoid overselling or deadlocks.

Post source and destination transfer lines atomically. A synchronous transfer moves stock immediately; a future dispatched/in-transit/received workflow needs separate state and transit stock, not a hidden subtraction.

Opening stock and value-changing adjustments require balanced accounting postings in the same transaction. A same-business warehouse transfer normally changes location rather than total asset value; preserve source costs.

Finalize physical counts against an explicit count cutoff or reconcile intervening movements. Do not overwrite live balances with an old count.

Record reversals rather than deleting finalized movement lines. Background alerts run after commit and deduplicate repeated notifications.

## Frontend work

Build stock overview, product movement detail, opening stock, adjustment forms, batch detail, transfer workflow, count/reconciliation screens and alert views.

Show on-hand, reserved and available separately. Display original unit and converted base quantity. Require a reason and confirmation for adjustments; show financial impact when available. Make unavailable or expired batches clear during allocation.

## Acceptance checks

- Opening 100 units and issuing 10 leaves 90 with linked stock and financial references.
- A transfer conserves total business quantity and value while updating both warehouses.
- A failing destination movement rolls back the entire transfer.
- Two concurrent requests cannot consume more than available stock.
- Reservations reduce availability without reducing physical on-hand.
- A count posted after intervening movements produces a correct adjustment.
- FEFO selects the earliest eligible expiry and excludes unusable stock.
- A retry does not duplicate movement or journal lines.
- Historical valuation uses recorded costs, not the current product purchase price.
- Unauthorized users cannot adjust or enable negative stock.

## Deliverables and exit criteria

Deliver the shared inventory service, connected stock/batch screens, migrations, valuation decision documentation and concurrency/rollback verification. Exit when stock balances reconcile to movements and value-changing events reconcile to accounting postings.


---

# Phase 4 — Purchases and Sales

## Goal

Implement end-to-end purchasing, receiving, wholesale/retail billing, POS, settlements and returns with immediate, consistent inventory and financial effects.

## Prerequisites

Phases 1–3 pass. Product/party/location records, inventory allocation, idempotency and the balanced posting kernel work.

Implement the transaction-specific accounting postings in this phase. Phase 5 adds full accounting management; it does not defer the financial effects of already finalized purchases or sales.

## Purchasing scope

Support purchase orders, supplier invoices, partial/full receiving, cash and credit purchases, discounts, tax configuration, additional purchase expenses, payment status, supplier history and purchase returns.

Separate purchase ordering, physical receiving, supplier invoicing and payment. Posting a supplier invoice for goods already received must not add the inventory again. Use receipt clearing and explicit matching when receiving precedes invoicing.

Track ordered, received, returned and remaining quantities. Reject over-receipt unless a configured authorized tolerance permits it. Allocate landed purchase costs by a documented rule.

## Sales scope

Support sales invoices, a fast POS screen, wholesale/retail price selection, cash/credit sales, partial/full payments, discounts, minimum price rules, cancellation, customer/product history and profit per invoice/product.

Support cash, bank transfer and configurable payment channels. Validate credit limits, available stock and batch eligibility. Provide printable invoices.

A credit sale increases receivables; cash increases only when a payment is actually posted. Do not treat an invoice as a receipt of cash.

## Database tables

| Tables | Responsibility |
| --- | --- |
| purchase_orders, purchase_order_lines | Supplier commitments |
| goods_receipts, goods_receipt_lines | Actual quantities received |
| supplier_invoices, supplier_invoice_lines, receipt_invoice_matches | Payables and receipt matching |
| sales_invoices, sales_invoice_lines, sales_allocations | Billing and batch allocation |
| payment_methods, payments, payment_allocations | Settlements linked to invoices/parties |
| sales_returns, sales_return_lines | Customer returns and disposition |
| purchase_returns, purchase_return_lines | Supplier returns |
| credit_notes, debit_notes | Financial adjustments with source links |
| document_taxes, document_charges | Snapshotted taxes and extra costs |

Reuse inventory, journal, idempotency and audit tables. Snapshot prices, costs, terms and taxes.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET/POST | /purchases/orders | Search/create purchase orders |
| GET/PATCH | /purchases/orders/{id} | View/edit allowed draft fields |
| POST | /purchases/orders/{id}/approve | Approve where configured |
| POST | /purchases/receipts | Post receipt against eligible order lines |
| GET/POST | /purchases/invoices | View/create supplier invoices |
| POST | /purchases/invoices/{id}/post | Post invoice and payable |
| GET/POST | /sales/invoices | View/create sales drafts |
| POST | /sales/invoices/{id}/post | Finalize stock and financial effects |
| GET | /sales/invoices/{id}/print | Printable invoice |
| POST | /sales/checkout | Atomic POS sale and optional settlement |
| POST | /payments | Post receipt/payment and allocations |
| GET/POST | /sales/returns and /purchases/returns | Review/create linked returns |
| POST | /sales/invoices/{id}/reverse | Authorized linked cancellation/reversal |
| GET | /customers/{id}/transactions and /suppliers/{id}/transactions | Party history |

## Backend work

Calculate totals on the server. Validate discounts, taxes and totals using Decimal and explicit rounding. Recalculate outstanding amounts from posted allocations.

Post document state, inventory movements, journal entries, settlement allocations and audit events within one transaction. For external payment services, introduce explicit pending/confirmed states and reconciliation rather than holding database locks during network calls.

Prevent duplicate invoice numbers, double posting, overpayment allocations and returns exceeding eligible original quantities. Returns reference original costs and tax treatment. Separate resalable, damaged and quarantined returns; only eligible goods become sellable.

If stock was received but the supplier invoice is pending, preserve the receipt clearing balance. Reversals must consider subsequent allocations and settled amounts; block invalid transitions or require linked corrective documents.

## Frontend work

Build order entry, receiving, supplier billing, sales invoicing, POS product search/barcode input, payment dialogs, invoice print preview and returns screens.

Show cash received separately from invoice total and remaining balance. Display stock, batch selection, wholesale/retail prices and credit-limit warnings. Show partial receiving and payment states. Disable duplicate posting while preserving retry-safe behavior.

## Acceptance checks

- Receive 4 of 10 ordered units; the order shows 6 outstanding.
- Invoicing those 4 units does not increase stock a second time.
- A credit sale of 100 with payment of 40 leaves receivables of 60 and cash increased by 40.
- A cash sale posts sales, cash and cost-of-goods entries correctly.
- Concurrent POS requests cannot oversell remaining stock.
- A failed posting rolls back document, inventory, journal and allocation changes.
- A return restores only eligible stock and reverses the appropriate revenue/cost/tax effects.
- Returning a sale made at an old cost preserves historical costing.
- Repeated checkout/finalization requests return the original result.
- Operators cannot exceed their price, refund, reversal or approval permissions.

## Deliverables and exit criteria

Deliver connected purchase, sales, POS, payment and return workflows; printable invoices; migrations; API documentation; and verification of atomic stock/accounting behavior. Exit when cash, credit, partial settlements and returns reconcile across operational and financial records.


---

# Phase 5 — Accounting

## Goal

Expand the existing posting kernel into a full double-entry accounting workspace with receivables, payables, payments, expenses, reconciliations and financial statements.

## Prerequisites

Phases 1–4 pass, including balanced postings from inventory, purchasing and sales. Review and reconcile existing opening inventory, receipt clearing, receivables and payables before exposing financial statements.

## Functional scope

Implement Chart of Accounts, General Ledger, Cash Book, Bank Book, journals, cash receipts/payments, AR/AP, income/expenses, Day Book, trial balance, profit and loss, balance sheet, cash flow, opening/closing balances, partial settlements, advances and controlled adjustments.

Support multiple cash/bank accounts, deposits, withdrawals, bank transfers, daily cash closing, cash reconciliation and bank reconciliation.

Support expense categories such as rent, electricity, salaries, transportation, fuel, maintenance, manufacturing, packaging and miscellaneous expenses. Attach receipts, dates, categories and payment method.

Support due dates, aging, customer/supplier statements and payment reminders. Reminders are authorized business notifications; configure recipients, templates and delivery channels before enabling external sending.

## Database tables

| Tables | Responsibility |
| --- | --- |
| accounts, account_mappings, fiscal_periods | Account hierarchy, event mappings and period controls |
| journal_entries, journal_entry_lines | Authoritative balanced postings |
| cash_bank_accounts | Cash/bank identity linked to GL accounts |
| payments, payment_allocations | Settlements, advances and allocations |
| expense_categories, expenses, expense_attachments | Expense capture and supporting receipts |
| bank_statement_imports, bank_statement_lines | Imported statement data and deduplication |
| reconciliation_sessions, reconciliation_matches | Cash/bank comparison and matching |
| cash_closings | Expected, counted and variance records |
| reminder_rules, reminder_deliveries | Authorized reminder history |

Prefer ledger views derived from journal lines and party links. If materialized subledger tables exist, reconcile them to the GL and prevent uncontrolled edits.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET/POST/PATCH | /accounting/accounts and /accounting/accounts/{id} | Chart of Accounts |
| GET/POST | /accounting/journals | Search/create draft journals |
| POST | /accounting/journals/{id}/post | Validate and post |
| POST | /accounting/journals/{id}/reverse | Linked reversal |
| GET | /accounting/general-ledger | Account/date ledger |
| GET | /customers/{id}/ledger and /suppliers/{id}/ledger | Party ledgers |
| GET | /accounting/receivables and /accounting/payables | Outstanding invoices and aging |
| GET/POST | /expenses | View/create expenses |
| POST | /expenses/{id}/post | Post expense and payment/payable effect |
| POST | /accounting/transfers | Transfer between cash/bank accounts |
| GET/POST | /accounting/reconciliations | Create/review reconciliation |
| POST | /accounting/reconciliations/{id}/finalize | Close approved reconciliation |
| POST | /accounting/cash-closings | Record daily count and approved variance |
| GET | /accounting/statements/{type} | Trial balance, P&L, balance sheet or cash flow |
| POST | /accounting/periods/{id}/close | Close a reconciled period |
| POST | /accounting/periods/{id}/reopen | Privileged, audited reopening |

## Backend work

Implement account types, posting restrictions, mapping validation and period locks. Require every journal to balance at currency precision, with exactly one debit/credit direction per line and valid posting accounts.

A transfer debits the receiving cash/bank account and credits the sending account; it does not create income. Allocate receipts/payments without exceeding available amounts. Keep advances visible as unapplied balances until correctly allocated.

Stage opening balances, validate total debits equal credits and post them once. Distinguish prior opening balances from ordinary revenue. Do not duplicate stock, customer or supplier openings entered in earlier phases.

Produce statements from posted data with a documented account mapping. Balance sheet assets must reconcile to liabilities plus equity, including current earnings. Derive cash flow from cash movements with configured classification; profit is not a substitute for cash flow.

Use as-of dates for aging and statements, including reversals/allocations effective by that date. Protect finalized documents and closed periods. Audit journal posting, mappings, opening balances, reconciliation and period changes.

## Frontend work

Build accounting navigation, account tree, journal editor, cash/bank books, party ledgers, outstanding invoice views, allocation dialogs, expense forms, reconciliation matching and statement screens.

Show debits/credits, opening/running/closing balances and statement filters clearly. Display unpaid invoices separately from cash movements. Show unallocated advances and block incomplete journals before submission, with server validation as final authority.

## Acceptance checks

- Unbalanced journals fail and leave no committed lines.
- Credit sales/purchases affect AR/AP without falsely changing cash.
- A partial payment reduces the correct invoice balance once.
- A cash-to-bank transfer preserves total liquid assets and creates no income.
- Aged balances match an as-of-date fixture even after later payments.
- Party subledgers reconcile to control accounts.
- Trial balance debits equal credits; the balance sheet equation holds.
- Repeated opening balance or payment requests do not duplicate postings.
- Bank statement duplicates cannot be imported twice without explicit handling.
- Closed-period backdating and unauthorized reopening fail.

## Deliverables and exit criteria

Deliver a connected accounting workspace, documented posting/account mappings, reconciliations, financial statements and integrity verification. Exit only when operational subledgers, inventory valuation and the GL reconcile for the agreed reference dataset.


---

# Phase 6 — Manufacturing

## Goal

Plan daily or weekly production, consume raw materials, produce traceable finished batches, capture quality outcomes and calculate actual production costs.

## Prerequisites

Phases 1–5 pass. Inventory batches, cost tracking, stock transactions, work-in-progress accounts and accounting postings are operational.

## Functional scope

Implement raw materials, Bills of Materials, versioned recipes, manufacturing orders, production planning, configurable weekly/day schedules, daily entries, batch creation, material consumption, finished output, labor, overhead/manufacturing expenses, wastage, rejected output and quality control.

Support specific recurring weekdays such as Friday through configuration. Store schedule timezone, effective date range and exception dates; avoid hardcoded weekdays.

Every finished batch has a unique business-scoped identifier, product, manufacturing/production date, optional expiry, produced quantity, consumed material references, production cost and status. Show remaining, sold, returned and damaged quantities through linked inventory events.

## Database tables

| Tables | Responsibility |
| --- | --- |
| bills_of_materials, bom_versions, bom_lines | Versioned material quantities, units and yields |
| production_schedules, production_schedule_exceptions | Weekly/daily recurrence and overrides |
| manufacturing_orders, manufacturing_order_lines | Planned products, quantity and approved BOM snapshot |
| production_records | Dated production executions |
| material_consumptions, material_consumption_lines | Actual raw material batch issues |
| production_outputs | Finished, rejected, rework and scrap output |
| production_labor_costs, production_overheads | Cost components and allocation references |
| quality_checks, quality_check_results | Inspection, disposition and release |
| batch_genealogy | Material-batch to output-batch traceability |

Reuse batches, inventory movements and journals. Distinguish raw materials, work in progress, finished goods and scrap accounts where configured.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET/POST | /manufacturing/boms | View/create BOMs |
| POST | /manufacturing/boms/{id}/versions | Create a new recipe version |
| POST | /manufacturing/bom-versions/{id}/approve | Approve a valid BOM |
| GET/POST/PATCH | /manufacturing/schedules and /manufacturing/schedules/{id} | Configure production recurrence |
| GET/POST | /manufacturing/orders | Plan production |
| POST | /manufacturing/orders/{id}/release | Snapshot BOM and reserve required material |
| POST | /manufacturing/orders/{id}/consume | Post actual material consumption |
| POST | /manufacturing/orders/{id}/record-output | Record production quantities and batches |
| POST | /manufacturing/orders/{id}/quality-checks | Record quality/disposition |
| POST | /manufacturing/orders/{id}/complete | Finalize eligible output and costs |
| GET | /manufacturing/orders/{id}/costs | Planned/actual cost breakdown |
| GET | /batches/{id}/traceability | Upstream and downstream batch links |
| GET | /manufacturing/daily-summary | Daily production visibility |

## Backend work

Validate BOM units, positive quantities, yields and references. Block circular dependencies for assemblies and snapshot the approved BOM on released orders so later changes do not alter existing plans.

Allow documented partial consumption and partial output. Deduplicate schedule-generated orders using schedule occurrence identity; restarting a worker must not create duplicate Friday orders.

Consume the selected raw material batches at their historical inventory cost. Move material value into work in progress. Accumulate approved labor/overhead without recording the same expense twice. Use documented absorption or allocation rules.

On completion, move eligible output cost from work in progress to finished inventory. Define normal waste, abnormal loss, rework and scrap treatment explicitly. Prevent division by zero, overshooting remaining planned quantities without approval and completion with unresolved required costs/checks.

Keep rejected or quarantined goods out of sellable stock until released. Record material and output links so a raw material batch can be traced to every affected finished batch and sale.

Batch profitability is based on attributable revenue, cost and recorded losses; unsold stock is not recognized as sales revenue.

## Frontend work

Build BOM editor/version history, production calendar, daily production screen, material availability panel, manufacturing order detail, consumption form, output/batch form, labor/overhead capture, quality checklist and batch traceability view.

Show planned versus actual quantities and costs, remaining material, accepted/rejected output, batch expiry and order status. Provide clear controlled actions for release, consume, inspect and complete.

## Acceptance checks

- Releasing an order snapshots the correct BOM version.
- Production is blocked when required materials are unavailable.
- Consuming materials reduces the right raw batches and posts work-in-progress value.
- A completed batch increases eligible finished stock exactly once.
- Partial production retains remaining quantities and unfinished work-in-progress value.
- Labor/overhead allocation reconciles to source costs without duplication.
- Rejected output remains unavailable for sale.
- Traceability connects supplier receipt → raw batch → manufacturing order → finished batch → sale.
- A recurring Friday schedule generates one order per configured occurrence.
- Failed completion rolls back inventory, journal, status and batch updates.
- Concurrent or repeated completion cannot create duplicate finished batches.

## Deliverables and exit criteria

Deliver connected production planning and execution, cost and quality workflows, batch genealogy, migrations and scenario evidence. Exit when material usage, finished quantities, wastage and accounting values reconcile for a representative production run.


---

# Phase 7 — Reports and Analytics

## Goal

Provide accurate business visibility through dashboards, inventory/financial/manufacturing reports and shareable PDF/Excel exports.

## Prerequisites

Phases 1–6 pass. Underlying operational and accounting transactions reconcile. Agree on metric definitions and date behavior before implementing charts.

## Dashboard scope

Show total products, stock quantity/value, today's sales/purchases, cash received, credit sales, customer receivables, supplier payables, expenses, gross/net profit, production summary, low/out-of-stock items and recent transactions.

Support daily, weekly, monthly and yearly views, date ranges and relevant warehouse/product/party filters. Label invoice-based metrics separately from cash-based metrics. Mixed units must not be added into a misleading single physical quantity.

## Required report coverage

| Family | Reports |
| --- | --- |
| Inventory | Current stock, stock movement, valuation, low-stock, out-of-stock, batch-wise, warehouse-wise and damaged stock |
| Sales | Daily, weekly, monthly, annual, customer-wise, product-wise, profit margin, cash sales and credit sales |
| Purchases | Supplier-wise, product-wise, returns, outstanding purchases and purchase history |
| Accounting | Customer/supplier ledger, GL, cash book, bank book, trial balance, P&L, balance sheet, cash flow, AR aging and AP aging |
| Manufacturing | Daily production, batch-wise production, manufacturing cost, material consumption, wastage, finished goods and batch profitability |

Provide applicable filters for date range, product, customer, supplier, category and warehouse. Distinguish “purchased but unpaid” from “ordered but not received” in outstanding purchase views.

## Data and supporting tables

Use posted documents, journal lines, inventory movements, batch genealogy and payment allocations as the authoritative sources. Add report_export_jobs and report_export_files for asynchronous exports. Add aggregate/materialized views only where measurements justify them and document refresh times.

Historical reports must use transaction snapshots and as-of logic rather than current catalog prices or current balances.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET | /dashboard/summary | Filtered headline metrics |
| GET | /dashboard/trends | Date-bucketed chart series |
| GET | /reports/inventory/{report} | Inventory report dataset |
| GET | /reports/sales/{report} | Sales report dataset |
| GET | /reports/purchases/{report} | Purchasing report dataset |
| GET | /reports/accounting/{report} | Financial report dataset |
| GET | /reports/manufacturing/{report} | Production report dataset |
| POST | /reports/exports | Request PDF or Excel with explicit filters |
| GET | /reports/exports/{id} | Job status and failure details |
| GET | /reports/exports/{id}/download | Authorized download |

Share aggregation services with Phase 5 financial statement routes so two screens cannot calculate different trial balances.

## Backend work

Specify whether each metric uses document date, posting date, settlement date or production date. Apply business timezone boundaries consistently and use half-open timestamp ranges for day/month queries.

Implement optimized queries with bounded pagination, suitable indexes and database aggregation. Avoid per-row database calls. Scope both report generation and downloads to the requesting user's permissions.

Use background export jobs for expensive output, recording requester, filters, format, generation timestamp and source cutoff. Generate small exports synchronously only when safe. Cache with business, authorization scope, date and filter inputs in the key.

For Excel, preserve numeric financial cells and guard against formula execution in untrusted text cells. For PDF, include readable columns, page breaks, totals, units/currency and filter context. Do not silently truncate large exports.

## Frontend work

Build a reporting center with grouped reports, saved filter state, searchable/paginated results, totals, drill-down links and export controls. Use Recharts for trends with clear axes, currency/units and loading/error states.

Allow users to move from dashboard totals to the supporting transactions. Show when data is stale, a report is empty or an export is still processing.

## Acceptance checks

- Dashboard totals match the underlying transaction lists for identical filters.
- AR/AP aging matches the historical reference dataset.
- A later catalog price change leaves historical profit and inventory value unchanged.
- Credit sales do not appear as cash received.
- Inventory reports reconcile with stock movements and GL inventory value.
- Manufacturing reports reconcile consumption, output, wastage and finished batch costs.
- Month/day filters handle timezone boundaries correctly.
- Export totals match on-screen totals for the same source cutoff.
- Users cannot download another unauthorized user's export by changing an identifier.
- Large datasets paginate and exports finish without silent row loss.

## Deliverables and exit criteria

Deliver the full report center, dashboard metrics, drill-downs, PDF/Excel exports, data definitions and measured query results. Exit when every required report has a real source, documented formulas and reconciliation evidence.


---

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
