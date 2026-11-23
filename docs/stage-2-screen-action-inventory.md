# Stage 2 screen/action inventory

Generated from the current workspace catalog. `connected` describes a transport connection, not proof that every action or workflow has been tested. `pending` is a proposed contract with no handler. `contract-gap` still lacks a resolved specific contract. Business actions remain visibly unavailable until implemented and verified.

Source authority: [complete requirements map](requirements-traceability.md). Cross-cutting routes: `/login` (public login), `/` (protected dashboard, metrics unavailable), `/system` (live health), `/roadmap` (planning), `/workspace/:group` (module navigation), forbidden/not-found/error states. Sidebar and route guards use current grants; backend authorization remains mandatory.

Shared behavior: `ResourcePage` renders lists/filter/pagination/error/unavailable states; `DetailPage` renders record tabs; `DraftPage` validates local inputs without persistence; `AdminEditorPage` connects user/role forms; `SettingsPage` connects currency/timezone changes. Report exports and business print actions have no persisted output yet. `WorkflowActions` lists review requirements only. IDs and decimal strings are preserved. See catalog.json for complete field schemas, line fields, tabs and columns, and workspaces/actions.js for action fields/grants/provisional states.

| Resource / route | Forms and actions | Read permission | API base (prefix /api/v1) | Connection |
|---|---|---|---|---|
| Products `/products` | list/detail; new/edit; archive | `products:read` | `/products` | pending |
| Categories & subcategories `/categories` | list/detail; new/edit; archive | `categories:read` | `/categories` | pending |
| Units `/units` | list/detail; new/edit; archive | `products:read` | `/units` | pending |
| Product unit conversions `/unit-conversions` | list/detail; new/edit; archive | `products:read` | `/product-unit-conversions` | pending |
| Brands `/brands` | list/detail; new/edit; archive | `brands:read` | `/brands` | pending |
| Manufacturers `/manufacturers` | list/detail; new/edit; archive | `brands:read` | `unresolved` | contract-gap |
| Warehouses `/warehouses` | list/detail; new/edit; archive | `warehouses:read` | `/warehouses` | pending |
| Customers `/customers` | list/detail; new/edit; archive | `customers:read` | `/customers` | pending |
| Suppliers `/suppliers` | list/detail; new/edit; archive | `suppliers:read` | `/suppliers` | pending |
| Vendors `/vendors` | list/detail; new/edit; archive | `vendors:read` | `/vendors` | pending |
| Employees `/employees` | list/detail; new/edit; archive | `employees:read` | `/employees` | pending |
| User & party contacts `/contacts` | list/detail; new/edit; archive | `employees:read` | `unresolved` | contract-gap |
| Opening balance drafts `/opening-balances` | list/detail; new/edit; post, cancel | `accounting:read` | `unresolved` | contract-gap |
| Stock availability `/stock` | list/detail; none | `inventory:read` | `/inventory/balances` | pending |
| Opening stock `/opening-stock` | list/detail; new/edit; post, cancel | `inventory:read` | `unresolved` | contract-gap |
| Movement history `/stock-movements` | list/detail; none | `inventory:read` | `/inventory/movements` | pending |
| Stock adjustments `/stock-adjustments` | list/detail; new/edit; approve, post, reverse, cancel | `inventory:read` | `/stock-adjustments` | pending |
| Damaged stock `/damaged-stock` | list/detail; new/edit; approve, post, reverse | `inventory:read` | `unresolved` | contract-gap |
| Stock reservations `/reservations` | list/detail; new/edit; release | `inventory:read` | `/inventory/reservations` | pending |
| Warehouse transfers `/warehouse-transfers` | list/detail; new/edit; approve, dispatch, receive, cancel | `inventory:read` | `/inventory/transfers` | pending |
| Physical counts & variances `/physical-counts` | list/detail; new/edit; review, approve, post | `inventory:read` | `unresolved` | contract-gap |
| Inventory reconciliation `/inventory-reconciliation` | list/detail; reconcile | `inventory:read` | `unresolved` | contract-gap |
| Stock valuation `/stock-valuation` | list/detail; none | `inventory:read` | `unresolved` | contract-gap |
| Batches & expiry `/batches` | list/detail; new/edit; approve, post, reverse, cancel | `batches:read` | `/batches` | pending |
| Low-stock & reorder alerts `/stock-alerts` | list/detail; none | `inventory:read` | `unresolved` | contract-gap |
| Purchase orders `/purchase-orders` | list/detail; new/edit; approve, receive, cancel | `purchases:read` | `/purchase-orders` | pending |
| Goods receipts `/goods-receipts` | list/detail; new/edit; post, reverse | `purchases:read` | `/goods-receipts` | pending |
| Supplier invoices `/supplier-invoices` | list/detail; new/edit; approve, post, pay, reverse | `purchases:read` | `/supplier-invoices` | pending |
| Receipt-to-invoice matching `/purchase-matching` | list/detail; new/edit; match | `purchases:read` | `unresolved` | contract-gap |
| Supplier settlements `/supplier-settlements` | list/detail; new/edit; allocate, post, reverse | `purchases:read` | `/payments` | pending |
| Purchase returns `/purchase-returns` | list/detail; new/edit; approve, post, refund, reverse | `returns_adjustments:read` | `/returns` | pending |
| Sales orders `/sales-orders` | list/detail; new/edit; approve, fulfill, cancel | `sales:read` | `/sales-orders` | pending |
| Shipments `/shipments` | list/detail; new/edit; post, reverse | `sales:read` | `/shipments` | pending |
| Sales invoices `/sales-invoices` | list/detail; new/edit; credit_check, post, pay, reverse | `sales:read` | `/sales-invoices` | pending |
| Customer returns & refunds `/sales-returns` | list/detail; new/edit; approve, post, refund, reverse | `returns_adjustments:read` | `/returns` | pending |
| Wholesale & retail prices `/pricing` | list/detail; new/edit; archive | `sales:read` | `unresolved` | contract-gap |
| Point of sale `/pos` | list/detail; new/edit; credit_check, pay, post | `pos:read` | `/pos/sales` | pending |
| Till sessions `/pos-sessions` | list/detail; new/edit; open, close | `pos:read` | `/pos/sessions` | pending |
| Chart of accounts `/accounts` | list/detail; new/edit; archive | `chart_of_accounts:read` | `/accounts` | pending |
| Journal drafts & postings `/journals` | list/detail; new/edit; post, reverse | `accounting:read` | `/journal-entries` | pending |
| General Ledger `/general-ledger` | list/detail; none | `general_ledger:read` | `/general-ledger` | pending |
| Day Book `/day-book` | list/detail; none | `general_ledger:read` | `unresolved` | contract-gap |
| Cash Book `/cash-book` | list/detail; none | `cash_bank:read` | `unresolved` | contract-gap |
| Bank Book `/bank-book` | list/detail; none | `cash_bank:read` | `unresolved` | contract-gap |
| Accounts Receivable `/receivables` | list/detail; none | `receivables:read` | `/receivables` | pending |
| Accounts Payable `/payables` | list/detail; none | `payables:read` | `/payables` | pending |
| Customer ledgers `/customer-ledgers` | list/detail; none | `customer_ledgers:read` | `/customer-ledgers/{partner_id}` | pending |
| Supplier ledgers `/supplier-ledgers` | list/detail; none | `supplier_ledgers:read` | `/supplier-ledgers/{partner_id}` | pending |
| Receivable & payable aging `/aging` | list/detail; none | `receivables:read` | `unresolved` | contract-gap |
| Customer & supplier advances `/advances` | list/detail; new/edit; post, allocate, reverse | `cash_bank:read` | `unresolved` | contract-gap |
| Payment allocations `/payment-allocations` | list/detail; new/edit; allocate, reverse | `cash_bank:read` | `/payment-allocations` | pending |
| Expenses & receipts `/expenses` | list/detail; new/edit; approve, post, reverse | `expenses:read` | `/expenses` | pending |
| Cash & bank transfers `/cash-bank-transfers` | list/detail; new/edit; post, reverse | `cash_bank:read` | `unresolved` | contract-gap |
| Daily cash closing `/cash-closing` | list/detail; new/edit; close | `cash_bank:read` | `unresolved` | contract-gap |
| Bank statement imports `/bank-imports` | list/detail; new/edit; import | `cash_bank:read` | `/bank-transactions` | pending |
| Bank reconciliation `/bank-reconciliation` | list/detail; new/edit; match, reconcile | `cash_bank:read` | `/reconciliations` | pending |
| Fiscal periods `/fiscal-periods` | list/detail; new/edit; close, reopen | `chart_of_accounts:read` | `/fiscal-periods` | pending |
| Trial balance `/trial-balance` | list/detail; none | `financial_statements:read` | `/financial-statements/trial-balance` | pending |
| Profit & loss `/profit-loss` | list/detail; none | `financial_statements:read` | `/financial-statements/profit-loss` | pending |
| Balance sheet `/balance-sheet` | list/detail; none | `financial_statements:read` | `/financial-statements/balance-sheet` | pending |
| Cash-flow statement `/cash-flow` | list/detail; none | `financial_statements:read` | `/financial-statements/cash-flow` | pending |
| Bills of materials `/boms` | list/detail; new/edit; approve, retire | `bom:read` | `/boms` | pending |
| Production schedules `/production-schedules` | list/detail; new/edit; schedule, cancel | `production_planning:read` | `/production-schedules` | pending |
| Manufacturing orders `/work-orders` | list/detail; new/edit; release, consume, complete, close, cancel | `production_planning:read` | `/work-orders` | pending |
| Material availability `/material-availability` | list/detail; none | `manufacturing:read` | `unresolved` | contract-gap |
| Material consumption `/material-consumption` | list/detail; new/edit; post, reverse | `manufacturing:read` | `/material-issues` | pending |
| Daily & partial output `/production-output` | list/detail; new/edit; post, reverse | `manufacturing:read` | `/production-completions` | pending |
| Finished batches `/finished-batches` | list/detail; new/edit; approve, post, reverse, cancel | `batches:read` | `/batches` | pending |
| Labor costs `/labor-costs` | list/detail; new/edit; allocate, post, reverse | `production_costing:read` | `/cost-allocations` | pending |
| Overhead costs `/overhead-costs` | list/detail; new/edit; allocate, post, reverse | `production_costing:read` | `/cost-allocations` | pending |
| Wastage & scrap `/wastage` | list/detail; new/edit; approve, post, reverse | `manufacturing:read` | `/scrap` | pending |
| Rejected output `/rejected-output` | list/detail; new/edit; approve, post, reverse | `manufacturing:read` | `unresolved` | contract-gap |
| Rework `/rework` | list/detail; new/edit; approve, post, reverse | `manufacturing:read` | `/rework` | pending |
| Quality checks & releases `/quality-checks` | list/detail; new/edit; approve, quality_release, reject | `quality_control:read` | `/quality-inspections` | pending |
| Planned versus actual costs `/production-costs` | list/detail; none | `production_costing:read` | `/cost-runs` | pending |
| Batch traceability `/batch-traceability` | list/detail; none | `batches:read` | `/batches/{id}/genealogy` | pending |
| Users `/users` | list/detail; new/edit; none | `users:read` | `/users` | connected |
| Roles & permissions `/roles` | list/detail; new/edit; none | `roles:read` | `/roles` | connected |
| Business settings `/business-settings` | settings edit; approve, post, reverse, cancel | `settings:read` | `/business-settings` | connected |
| Account mappings `/account-mappings` | list/detail; new/edit; archive | `chart_of_accounts:read` | `/account-mappings` | pending |
| Audit log `/audit-logs` | list/detail; none | `audit_logs:read` | `/audit-logs` | pending |
| Reminder configuration `/reminders` | list/detail; new/edit; archive | `settings:read` | `unresolved` | contract-gap |
| Alert configuration `/alert-configuration` | list/detail; new/edit; archive | `settings:read` | `unresolved` | contract-gap |
| Current stock `/reports/current-stock` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/current-stock` | pending |
| Stock movement `/reports/stock-movement` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/stock-movement` | pending |
| Stock valuation `/reports/stock-valuation` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/stock-valuation` | pending |
| Low-stock `/reports/low-stock` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/low-stock` | pending |
| Out-of-stock `/reports/out-of-stock` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/out-of-stock` | pending |
| Batch-wise stock `/reports/batch-wise-stock` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/batch-wise-stock` | pending |
| Warehouse-wise stock `/reports/warehouse-wise-stock` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/warehouse-wise-stock` | pending |
| Damaged stock `/reports/damaged-stock` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/inventory/damaged-stock` | pending |
| Daily sales `/reports/daily-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/daily-sales` | pending |
| Weekly sales `/reports/weekly-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/weekly-sales` | pending |
| Monthly sales `/reports/monthly-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/monthly-sales` | pending |
| Annual sales `/reports/annual-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/annual-sales` | pending |
| Customer-wise sales `/reports/customer-wise-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/customer-wise-sales` | pending |
| Product-wise sales `/reports/product-wise-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/product-wise-sales` | pending |
| Profit margin `/reports/profit-margin` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/profit-margin` | pending |
| Credit sales `/reports/credit-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/credit-sales` | pending |
| Cash sales `/reports/cash-sales` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/sales/cash-sales` | pending |
| Supplier-wise purchases `/reports/supplier-wise-purchases` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/purchases/supplier-wise-purchases` | pending |
| Product-wise purchases `/reports/product-wise-purchases` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/purchases/product-wise-purchases` | pending |
| Purchase returns `/reports/purchase-returns` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/purchases/purchase-returns` | pending |
| Outstanding purchases `/reports/outstanding-purchases` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/purchases/outstanding-purchases` | pending |
| Purchase history `/reports/purchase-history` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/purchases/purchase-history` | pending |
| Customer ledger `/reports/customer-ledger` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/customer-ledger` | pending |
| Supplier ledger `/reports/supplier-ledger` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/supplier-ledger` | pending |
| General Ledger `/reports/general-ledger` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/general-ledger` | pending |
| Cash Book `/reports/cash-book` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/cash-book` | pending |
| Bank Book `/reports/bank-book` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/bank-book` | pending |
| Trial balance `/reports/trial-balance` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/trial-balance` | pending |
| Profit and loss `/reports/profit-and-loss` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/profit-and-loss` | pending |
| Balance sheet `/reports/balance-sheet` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/balance-sheet` | pending |
| Cash flow `/reports/cash-flow` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/cash-flow` | pending |
| Receivables aging `/reports/receivables-aging` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/receivables-aging` | pending |
| Payables aging `/reports/payables-aging` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/accounting/payables-aging` | pending |
| Daily production `/reports/daily-production` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/daily-production` | pending |
| Batch-wise production `/reports/batch-wise-production` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/batch-wise-production` | pending |
| Manufacturing cost `/reports/manufacturing-cost` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/manufacturing-cost` | pending |
| Raw material consumption `/reports/raw-material-consumption` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/raw-material-consumption` | pending |
| Production wastage `/reports/production-wastage` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/production-wastage` | pending |
| Finished goods `/reports/finished-goods` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/finished-goods` | pending |
| Batch profitability `/reports/batch-profitability` | list/detail; none; filter, drill-down, print, PDF/Excel (pending) | `reports:read` | `/reports/manufacturing/batch-profitability` | pending |

Create/edit use each resource's createPermission/updatePermission; action permissions combine resource.module with the action's grant in actions.js. Protected user/role controls add backend checks. Generic action states remain provisional until each domain service validates its exact state machine. Source-specific proposed APIs supersede conflicting early Stage 1 paths; see source-reconciliation.md. No nonexistent command is sent by the current transport.
