# ERP requirements traceability

Updated against the complete source pack on 2026-11-24. This is a source coverage index, not an ERP completion certificate.

The ten authoritative documents are listed in [source reconciliation](source-reconciliation.md). Original bytes and ZIP provenance are recorded in [manifest.json](erp-source/manifest.json). The confirmed role override `OVR-ROLES-01` takes precedence over older suggested roles. Empty legacy phase placeholders are not sources.

Stable IDs identify every source paragraph, list item, table row and fenced example. Source units include context as well as requirements; their count must not be reported as an implementation percentage. The machine-readable [index](requirements-traceability.json) preserves full text, source lines and workstream mappings. Original report items use `R01.01`–`R01.40`, also used by the [report catalog](report-catalog.json).

Mappings below identify implementation locations or planned owners. File existence, a route scaffold, and a permission reservation do not establish completed behavior. Prior Stage 1 evidence is explicitly distinguished from tests that have not run.

## Workstream mapping

### foundation

- Screens/actions: Login, protected layout, users, roles, business settings.
- Code/service owner: backend/app/auth; backend/app/modules/users; backend/app/modules/roles; backend/app/modules/settings; backend/app/modules/accounting/posting.py.
- Contracts: docs/api.md#implemented-routes; docs/openapi.json.
- Database: Implemented: businesses, business_settings, users, roles, permissions, user_roles, role_permissions, auth_sessions, audit_logs, document_sequences, idempotency_records, accounts, journal_entries, journal_entry_lines.
- Verification: docs/phases/phase-01-foundation.md; backend/tests/integration/test_stage1.py; backend/tests/test_security.py; backend/tests/test_foundation.py.
- Status: **Foundation evidence recorded previously; source additions and API differences still require reconciliation**.

### master

- Screens/actions: Master data workspace: catalog, units/conversions, parties, warehouses, opening-balance drafts.
- Code/service owner: frontend/src/workspaces/catalog.json; backend services not implemented.
- Contracts: erp-source/02_Phase_2_Master_Data.md#proposed-apis.
- Database: Planned Phase 2 tables: products, units, product_unit_conversions, categories, brands, manufacturers, warehouses, product_images, product_suppliers, parties, party_roles, party_contacts, party_addresses, customer_profiles, supplier_profiles, vendor_profiles, opening_balance_drafts.
- Verification: Required M01–M09; no persisted master-data acceptance evidence.
- Status: **UI scaffold; business APIs, migrations and verification pending**.

### inventory

- Screens/actions: Inventory workspace: stock, movements, openings, damage, reservations, transfers, counts, valuation, batches, alerts.
- Code/service owner: frontend/src/workspaces/catalog.json; backend/app/modules/inventory/service.py is an interface only.
- Contracts: erp-source/03_Phase_3_Inventory.md#proposed-apis.
- Database: Planned Phase 3 tables: inventory_transactions, inventory_movements, stock_balances, stock_reservations, batches, batch_stock_balances, stock_transfers, stock_transfer_lines, stock_counts, stock_count_lines, inventory_cost_layers or inventory_cost_state, alert_rules, alert_events.
- Verification: Required I01–I11; no stock movement/valuation acceptance evidence.
- Status: **UI scaffold and service interface; implementation and verification pending**.

### trade

- Screens/actions: Purchase and Sales workspaces: orders, receiving, matching, invoices, POS, settlements, returns.
- Code/service owner: frontend/src/workspaces/catalog.json; backend services not implemented.
- Contracts: erp-source/04_Phase_4_Purchases_and_Sales.md#proposed-apis.
- Database: Planned Phase 4 tables: purchase_orders/lines, goods_receipts/lines, supplier_invoices/lines, receipt_invoice_matches, sales_invoices/lines, sales_allocations, payment_methods, payments, payment_allocations, sales_returns/lines, purchase_returns/lines, credit_notes, debit_notes, document_taxes, document_charges.
- Verification: Required T01–T15; no persisted sales/purchase/payment acceptance evidence.
- Status: **UI scaffold; business APIs, migrations and verification pending**.

### accounting

- Screens/actions: Accounting workspace: accounts, journals, books/ledgers, AR/AP, expenses, allocations, reconciliation, periods and statements.
- Code/service owner: backend/app/modules/accounting/posting.py (internal kernel); frontend/src/workspaces/catalog.json.
- Contracts: erp-source/05_Phase_5_Accounting.md#proposed-apis; docs/api.md (internal kernel is not an HTTP journal workflow).
- Database: Implemented: accounts, journal_entries, journal_entry_lines; planned: account_mappings, fiscal_periods, cash_bank_accounts, payments/allocations, expense_categories, expenses/attachments, bank_statement_imports/lines, reconciliation_sessions/matches, cash_closings, reminder_rules/deliveries.
- Verification: backend/tests/integration/test_stage1.py verifies kernel only; required A01–A10 full accounting evidence pending.
- Status: **Posting kernel verified previously; accounting workflows and reports pending**.

### manufacturing

- Screens/actions: Manufacturing workspace: BOMs, schedules, orders, consumption, output, labor/overhead, waste/rework, quality, costs, genealogy.
- Code/service owner: frontend/src/workspaces/catalog.json; backend services not implemented.
- Contracts: erp-source/06_Phase_6_Manufacturing.md#proposed-apis.
- Database: Planned Phase 6 tables: bills_of_materials, bom_versions/lines, production_schedules/exceptions, manufacturing_orders/lines, production_records, material_consumptions/lines, production_outputs, production_labor_costs, production_overheads, quality_checks/results, batch_genealogy.
- Verification: Required P01–P12; no production/WIP/genealogy acceptance evidence.
- Status: **UI scaffold; business APIs, migrations and verification pending**.

### reports

- Screens/actions: Dashboard and 40 named report routes; see report-catalog.json and report-verification.md.
- Code/service owner: frontend/src/pages/DashboardPage.jsx; frontend/src/pages/workspaces/ResourcePage.jsx; backend aggregation/export services not implemented.
- Contracts: erp-source/07_Phase_7_Reports_and_Analytics.md#proposed-apis; report-catalog.json.
- Database: Planned reads of posted movements, journals, documents, allocations, genealogy; report_export_jobs/files are not migrated.
- Verification: R01.01–R01.40 each have six explicit verification cases; R02–R08 also required; all business results pending.
- Status: **Exact source catalog reconciled; totals, permissions, drill-downs, history and exports not verified**.

### ui

- Screens/actions: All workspace routes; shared forms, tables, dialogs, charts, filters, theme/navigation.
- Code/service owner: frontend/src/components; frontend/src/forms; frontend/src/hooks; frontend/src/app/router.jsx; frontend/src/services/resources.js.
- Contracts: stage-2-screen-action-inventory.md; actual versus planned API distinction in docs/api.md.
- Database: No direct database access; depends on each module's authorized API.
- Verification: frontend/tests/unit; frontend/tests/e2e; required U01–U07 end-to-end business evidence pending.
- Status: **Shared UI exists; connected business workflow acceptance pending**.

### architecture

- Screens/actions: Cross-cutting application layers and domain design.
- Code/service owner: README.md; docs/architecture.md; docs/domain-model.md; docs/database-design.md; frontend/package-lock.json; backend/requirements-dev.lock; compose.yaml.
- Contracts: docs/api.md; source-reconciliation.md (layout and contract differences).
- Database: Foundation migration implemented; later source-phase schemas planned incrementally.
- Verification: docs/traceability.md and docs/phases/phase-01-foundation.md cover Stage 1 only; full-domain evidence pending.
- Status: **Foundation/design baseline; entire-ERP invariants require future module evidence**.

### operations

- Screens/actions: Health, operations/runbooks, reference workflow, regression and readiness.
- Code/service owner: Makefile; scripts/test-local.sh; backend/tests; frontend/tests; docs/testing.md; docs/deployment.md; docs/backup-restore.md.
- Contracts: erp-source/08_Phase_8_Testing_and_Optimization.md; source-reconciliation.md.
- Database: Isolated PostgreSQL fixtures; full business dataset/attachment restore and upgrade evidence pending.
- Verification: Prior foundation checks are recorded in docs/testing.md; full F/M/I/T/A/P/R/U/O catalog and reference reconciliation not complete.
- Status: **Foundation evidence available; full ERP readiness unverified**.

## Source requirement index

Each ID inherits its linked workstream's screens, code/service owner, database scope and evidence status. This broad source mapping does not replace the individual test evidence required before a completion claim. Compound source paragraphs still require multiple executable checks.

### 00_Original_Requirements.md

522 indexed source units. [Read the complete document](erp-source/00_Original_Requirements.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| ORIG-001 | L5: I want to develop a comprehensive, professional, scalable, and modular ERP (Enterprise Resource Planning) system for a trading, wholesale, retail, spare parts, and manufacturing business. | [architecture](#architecture) | — |
| ORIG-002 | L7: The business deals with: | [architecture](#architecture) | — |
| ORIG-003 | L9: - Motorcycle spare parts and accessories. | [architecture](#architecture) | — |
| ORIG-004 | L10: - Electrical meters and related products. | [architecture](#architecture) | — |
| ORIG-005 | L11: - General trading products. | [architecture](#architecture) | — |
| ORIG-006 | L12: - Multiple suppliers and vendors. | [architecture](#architecture) | — |
| ORIG-007 | L13: - Wholesale and retail customers. | [architecture](#architecture) | — |
| ORIG-008 | L14: - Cash, credit, and debit transactions. | [architecture](#architecture) | — |
| ORIG-009 | L15: - Daily manufacturing and batch-based production. | [architecture](#architecture) | — |
| ORIG-010 | L16: - Inventory purchasing, selling, receiving, and dispatching. | [architecture](#architecture) | — |
| ORIG-011 | L18: The objective is to digitize and centralize every important business operation, including accounting, inventory, manufacturing, purchasing, sales, financial transactions, and reporting. | [architecture](#architecture) | — |
| ORIG-012 | L20: This must be a complete business management solution, not just a basic inventory management application. | [architecture](#architecture) | — |
| ORIG-013 | L26: Use the following technologies strictly. | [architecture](#architecture) | — |
| ORIG-014 | L29: - React.js | [architecture](#architecture) | — |
| ORIG-015 | L30: - Vite | [architecture](#architecture) | — |
| ORIG-016 | L31: - Tailwind CSS v4 | [architecture](#architecture) | — |
| ORIG-017 | L32: - JavaScript (ES6+) | [architecture](#architecture) | — |
| ORIG-018 | L33: - React Router DOM | [architecture](#architecture) | — |
| ORIG-019 | L34: - Axios | [architecture](#architecture) | — |
| ORIG-020 | L35: - React Hook Form | [architecture](#architecture) | — |
| ORIG-021 | L36: - Zod for validation | [architecture](#architecture) | — |
| ORIG-022 | L37: - Recharts for dashboards and analytics | [architecture](#architecture) | — |
| ORIG-023 | L38: - Lucide React for icons | [architecture](#architecture) | — |
| ORIG-024 | L41: - Python | [architecture](#architecture) | — |
| ORIG-025 | L42: - FastAPI | [architecture](#architecture) | — |
| ORIG-026 | L43: - SQLAlchemy 2.0 | [architecture](#architecture) | — |
| ORIG-027 | L44: - Pydantic v2 | [architecture](#architecture) | — |
| ORIG-028 | L45: - Alembic for database migrations | [architecture](#architecture) | — |
| ORIG-029 | L46: - JWT Authentication | [architecture](#architecture) | — |
| ORIG-030 | L47: - Python-based business logic and service layers | [architecture](#architecture) | — |
| ORIG-031 | L50: - PostgreSQL | [architecture](#architecture) | — |
| ORIG-032 | L53: - Redis for caching and background jobs where required. | [architecture](#architecture) | — |
| ORIG-033 | L54: - Celery or an equivalent background task system. | [architecture](#architecture) | — |
| ORIG-034 | L55: - Docker and Docker Compose. | [architecture](#architecture) | — |
| ORIG-035 | L56: - Environment-based configuration. | [architecture](#architecture) | — |
| ORIG-036 | L57: - Structured application logging. | [architecture](#architecture) | — |
| ORIG-037 | L59: Use stable, compatible versions of all dependencies. | [architecture](#architecture) | — |
| ORIG-038 | L65: Before writing application code, initialize the complete project structure. | [architecture](#architecture) | — |
| ORIG-039 | L67: The root directory should be: | [architecture](#architecture) | — |
| ORIG-040 | L69: business-erp/ | [architecture](#architecture) | — |
| ORIG-041 | L73: Execute the following commands: | [architecture](#architecture) | — |
| ORIG-042 | L75: bash mkdir business-erp cd business-erp  npm create vite@latest frontend -- --template react cd frontend  npm install  npm install react-router-dom axios npm install react-hook-form zod @hookform/resolvers npm install recharts … | [architecture](#architecture) | — |
| ORIG-043 | L94: Configure Tailwind CSS v4 using the official Vite plugin. | [architecture](#architecture) | — |
| ORIG-044 | L98: bash mkdir backend cd backend  python -m venv venv  # Linux / macOS source venv/bin/activate  # Windows # venv\Scripts\activate  pip install fastapi "uvicorn[standard]" pip install sqlalchemy psycopg[binary] pip install alembic… | [architecture](#architecture) | — |
| ORIG-045 | L125: Create the PostgreSQL database and configure the connection through environment variables. | [architecture](#architecture) | — |
| ORIG-046 | L127: Do not hardcode credentials. | [architecture](#architecture) | — |
| ORIG-047 | L133: Follow a clean, modular, layered architecture. | [architecture](#architecture) | — |
| ORIG-048 | L137: text frontend/ │ ├── public/ │ ├── src/ │   ├── assets/ │   │ │   ├── components/ │   │   ├── common/ │   │   ├── forms/ │   │   ├── tables/ │   │   ├── charts/ │   │   ├── modals/ │   │   └── layout/ │   │ │   ├── pages/ │   │… | [architecture](#architecture) | — |
| ORIG-049 | L202: text backend/ │ ├── app/ │   ├── api/ │   │   ├── v1/ │   │   │   ├── endpoints/ │   │   │   │   ├── auth.py │   │   │   │   ├── dashboard.py │   │   │   │   ├── products.py │   │   │   │   ├── inventory.py │   │   │   │   ├── … | [architecture](#architecture) | — |
| ORIG-050 | L252: Use separate model, schema, repository, service, and API layers. Do not put all business logic inside API routes. | [architecture](#architecture) | — |
| ORIG-051 | L260: Develop a comprehensive business dashboard showing: | [reports](#reports) | — |
| ORIG-052 | L262: - Total inventory value. | [reports](#reports) | — |
| ORIG-053 | L263: - Total products. | [reports](#reports) | — |
| ORIG-054 | L264: - Total stock quantity. | [reports](#reports) | — |
| ORIG-055 | L265: - Today's sales. | [reports](#reports) | — |
| ORIG-056 | L266: - Today's purchases. | [reports](#reports) | — |
| ORIG-057 | L267: - Today's cash received. | [reports](#reports) | — |
| ORIG-058 | L268: - Today's credit sales. | [reports](#reports) | — |
| ORIG-059 | L269: - Outstanding customer balances. | [reports](#reports) | — |
| ORIG-060 | L270: - Outstanding supplier balances. | [reports](#reports) | — |
| ORIG-061 | L271: - Total expenses. | [reports](#reports) | — |
| ORIG-062 | L272: - Gross profit and net profit. | [reports](#reports) | — |
| ORIG-063 | L273: - Manufacturing production summary. | [reports](#reports) | — |
| ORIG-064 | L274: - Low-stock products. | [reports](#reports) | — |
| ORIG-065 | L275: - Out-of-stock products. | [reports](#reports) | — |
| ORIG-066 | L276: - Recent transactions. | [reports](#reports) | — |
| ORIG-067 | L277: - Daily, weekly, monthly, and yearly financial statistics. | [reports](#reports) | — |
| ORIG-068 | L279: Include interactive charts and date filters. | [reports](#reports) | — |
| ORIG-069 | L283: Create a complete product management module. | [master](#master) | — |
| ORIG-070 | L285: Features: | [master](#master) | — |
| ORIG-071 | L287: - Product name and unique SKU. | [master](#master) | — |
| ORIG-072 | L288: - Barcode and QR code support. | [master](#master) | — |
| ORIG-073 | L289: - Product category and subcategory. | [master](#master) | — |
| ORIG-074 | L290: - Brand and manufacturer. | [master](#master) | — |
| ORIG-075 | L291: - Product description. | [master](#master) | — |
| ORIG-076 | L292: - Purchase price. | [master](#master) | — |
| ORIG-077 | L293: - Wholesale price. | [master](#master) | — |
| ORIG-078 | L294: - Retail price. | [master](#master) | — |
| ORIG-079 | L295: - Minimum selling price. | [master](#master) | — |
| ORIG-080 | L296: - Current stock. | [master](#master) | — |
| ORIG-081 | L297: - Minimum stock level. | [master](#master) | — |
| ORIG-082 | L298: - Unit of measurement. | [master](#master) | — |
| ORIG-083 | L299: - Product image. | [master](#master) | — |
| ORIG-084 | L300: - Supplier association. | [master](#master) | — |
| ORIG-085 | L301: - Product status. | [master](#master) | — |
| ORIG-086 | L302: - Product history. | [master](#master) | — |
| ORIG-087 | L304: Support different product types, including motorcycle spare parts, meters, accessories, and general trading items. | [master](#master) | — |
| ORIG-088 | L308: Implement a complete inventory tracking system. | [inventory](#inventory) | — |
| ORIG-089 | L310: Features: | [inventory](#inventory) | — |
| ORIG-090 | L312: - Stock in. | [inventory](#inventory) | — |
| ORIG-091 | L313: - Stock out. | [inventory](#inventory) | — |
| ORIG-092 | L314: - Stock adjustments. | [inventory](#inventory) | — |
| ORIG-093 | L315: - Opening stock. | [inventory](#inventory) | — |
| ORIG-094 | L316: - Closing stock. | [inventory](#inventory) | — |
| ORIG-095 | L317: - Stock transfers between warehouses. | [inventory](#inventory) | — |
| ORIG-096 | L318: - Damaged stock. | [inventory](#inventory) | — |
| ORIG-097 | L319: - Returned stock. | [inventory](#inventory) | — |
| ORIG-098 | L320: - Reserved stock. | [inventory](#inventory) | — |
| ORIG-099 | L321: - Available stock. | [inventory](#inventory) | — |
| ORIG-100 | L322: - Stock valuation. | [inventory](#inventory) | — |
| ORIG-101 | L323: - Inventory movement history. | [inventory](#inventory) | — |
| ORIG-102 | L324: - Reorder level notifications. | [inventory](#inventory) | — |
| ORIG-103 | L325: - Low-stock alerts. | [inventory](#inventory) | — |
| ORIG-104 | L326: - Physical stock reconciliation. | [inventory](#inventory) | — |
| ORIG-105 | L328: Every inventory movement must have a transaction reference and an audit trail. | [inventory](#inventory) | — |
| ORIG-106 | L330: Never allow stock to change without recording the corresponding inventory transaction. | [inventory](#inventory) | — |
| ORIG-107 | L334: Manage all purchasing activities. | [trade](#trade) | — |
| ORIG-108 | L336: Features: | [trade](#trade) | — |
| ORIG-109 | L338: - Purchase orders. | [trade](#trade) | — |
| ORIG-110 | L339: - Supplier invoices. | [trade](#trade) | — |
| ORIG-111 | L340: - Purchase receiving. | [trade](#trade) | — |
| ORIG-112 | L341: - Partial receiving. | [trade](#trade) | — |
| ORIG-113 | L342: - Full receiving. | [trade](#trade) | — |
| ORIG-114 | L343: - Purchase returns. | [trade](#trade) | — |
| ORIG-115 | L344: - Purchase discounts. | [trade](#trade) | — |
| ORIG-116 | L345: - Additional purchase expenses. | [trade](#trade) | — |
| ORIG-117 | L346: - Purchase tax. | [trade](#trade) | — |
| ORIG-118 | L347: - Purchase payment status. | [trade](#trade) | — |
| ORIG-119 | L348: - Cash purchases. | [trade](#trade) | — |
| ORIG-120 | L349: - Credit purchases. | [trade](#trade) | — |
| ORIG-121 | L350: - Supplier-wise purchase history. | [trade](#trade) | — |
| ORIG-122 | L352: When a purchase is finalized, update inventory and the relevant accounting records automatically. | [trade](#trade) | — |
| ORIG-123 | L356: Create a complete sales and billing module. | [trade](#trade) | — |
| ORIG-124 | L358: Features: | [trade](#trade) | — |
| ORIG-125 | L360: - Sales invoices. | [trade](#trade) | — |
| ORIG-126 | L361: - POS interface. | [trade](#trade) | — |
| ORIG-127 | L362: - Wholesale sales. | [trade](#trade) | — |
| ORIG-128 | L363: - Retail sales. | [trade](#trade) | — |
| ORIG-129 | L364: - Cash sales. | [trade](#trade) | — |
| ORIG-130 | L365: - Credit sales. | [trade](#trade) | — |
| ORIG-131 | L366: - Partial payments. | [trade](#trade) | — |
| ORIG-132 | L367: - Full payments. | [trade](#trade) | — |
| ORIG-133 | L368: - Customer discounts. | [trade](#trade) | — |
| ORIG-134 | L369: - Sales returns. | [trade](#trade) | — |
| ORIG-135 | L370: - Invoice cancellation. | [trade](#trade) | — |
| ORIG-136 | L371: - Customer-wise sales history. | [trade](#trade) | — |
| ORIG-137 | L372: - Product-wise sales history. | [trade](#trade) | — |
| ORIG-138 | L373: - Daily sales reports. | [trade](#trade) | — |
| ORIG-139 | L374: - Profit per invoice and product. | [trade](#trade) | — |
| ORIG-140 | L376: Support multiple payment methods, including cash, bank transfer, and other configurable payment channels. | [trade](#trade) | — |
| ORIG-141 | L380: Maintain complete customer records. | [master](#master) | — |
| ORIG-142 | L382: Features: | [master](#master) | — |
| ORIG-143 | L384: - Customer profile. | [master](#master) | — |
| ORIG-144 | L385: - Contact information. | [master](#master) | — |
| ORIG-145 | L386: - Address. | [master](#master) | — |
| ORIG-146 | L387: - Opening balance. | [master](#master) | — |
| ORIG-147 | L388: - Credit limit. | [master](#master) | — |
| ORIG-148 | L389: - Total purchases. | [master](#master) | — |
| ORIG-149 | L390: - Total outstanding balance. | [master](#master) | — |
| ORIG-150 | L391: - Payment history. | [master](#master) | — |
| ORIG-151 | L392: - Customer ledger. | [master](#master) | — |
| ORIG-152 | L393: - Credit and debit transactions. | [master](#master) | — |
| ORIG-153 | L394: - Due dates. | [master](#master) | — |
| ORIG-154 | L395: - Payment reminders. | [master](#master) | — |
| ORIG-155 | L396: - Customer statements. | [master](#master) | — |
| ORIG-156 | L398: Each customer should have an automatically maintained account ledger. | [master](#master) | — |
| ORIG-157 | L402: Maintain separate supplier and vendor records where required. | [master](#master) | — |
| ORIG-158 | L404: Features: | [master](#master) | — |
| ORIG-159 | L406: - Supplier profiles. | [master](#master) | — |
| ORIG-160 | L407: - Vendor profiles. | [master](#master) | — |
| ORIG-161 | L408: - Contact information. | [master](#master) | — |
| ORIG-162 | L409: - Opening balances. | [master](#master) | — |
| ORIG-163 | L410: - Purchase history. | [master](#master) | — |
| ORIG-164 | L411: - Payment history. | [master](#master) | — |
| ORIG-165 | L412: - Outstanding payable amounts. | [master](#master) | — |
| ORIG-166 | L413: - Supplier ledger. | [master](#master) | — |
| ORIG-167 | L414: - Credit purchases. | [master](#master) | — |
| ORIG-168 | L415: - Debit payments. | [master](#master) | — |
| ORIG-169 | L416: - Supplier returns. | [master](#master) | — |
| ORIG-170 | L417: - Due dates. | [master](#master) | — |
| ORIG-171 | L418: - Supplier statements. | [master](#master) | — |
| ORIG-172 | L422: This is one of the most important modules. | [accounting](#accounting) | — |
| ORIG-173 | L424: Implement a proper double-entry accounting system. | [accounting](#accounting) | — |
| ORIG-174 | L426: Required modules: | [accounting](#accounting) | — |
| ORIG-175 | L428: - Chart of Accounts. | [accounting](#accounting) | — |
| ORIG-176 | L429: - General Ledger. | [accounting](#accounting) | — |
| ORIG-177 | L430: - Cash Book. | [accounting](#accounting) | — |
| ORIG-178 | L431: - Bank Book. | [accounting](#accounting) | — |
| ORIG-179 | L432: - Journal Entries. | [accounting](#accounting) | — |
| ORIG-180 | L433: - Cash Receipts. | [accounting](#accounting) | — |
| ORIG-181 | L434: - Cash Payments. | [accounting](#accounting) | — |
| ORIG-182 | L435: - Customer Receivables. | [accounting](#accounting) | — |
| ORIG-183 | L436: - Supplier Payables. | [accounting](#accounting) | — |
| ORIG-184 | L437: - Accounts Receivable (AR). | [accounting](#accounting) | — |
| ORIG-185 | L438: - Accounts Payable (AP). | [accounting](#accounting) | — |
| ORIG-186 | L439: - Income and Expenses. | [accounting](#accounting) | — |
| ORIG-187 | L440: - Trial Balance. | [accounting](#accounting) | — |
| ORIG-188 | L441: - Profit and Loss Statement. | [accounting](#accounting) | — |
| ORIG-189 | L442: - Balance Sheet. | [accounting](#accounting) | — |
| ORIG-190 | L443: - Cash Flow Statement. | [accounting](#accounting) | — |
| ORIG-191 | L444: - Day Book. | [accounting](#accounting) | — |
| ORIG-192 | L445: - Opening Balances. | [accounting](#accounting) | — |
| ORIG-193 | L446: - Closing Balances. | [accounting](#accounting) | — |
| ORIG-194 | L448: Support: | [accounting](#accounting) | — |
| ORIG-195 | L450: 1. Cash transactions. | [accounting](#accounting) | — |
| ORIG-196 | L451: 2. Credit transactions. | [accounting](#accounting) | — |
| ORIG-197 | L452: 3. Debit transactions. | [accounting](#accounting) | — |
| ORIG-198 | L453: 4. Partial settlements. | [accounting](#accounting) | — |
| ORIG-199 | L454: 5. Advance payments. | [accounting](#accounting) | — |
| ORIG-200 | L455: 6. Outstanding balances. | [accounting](#accounting) | — |
| ORIG-201 | L456: 7. Customer and supplier adjustments. | [accounting](#accounting) | — |
| ORIG-202 | L458: Every finalized financial transaction must generate balanced journal entries. | [accounting](#accounting) | — |
| ORIG-203 | L460: Do not treat credit sales as cash received. Do not treat unpaid purchases as cash payments. | [accounting](#accounting) | — |
| ORIG-204 | L464: Develop a dedicated manufacturing and production management module. | [manufacturing](#manufacturing) | — |
| ORIG-205 | L466: The business manufactures products in daily batches. | [manufacturing](#manufacturing) | — |
| ORIG-206 | L468: Features: | [manufacturing](#manufacturing) | — |
| ORIG-207 | L470: - Manufacturing orders. | [manufacturing](#manufacturing) | — |
| ORIG-208 | L471: - Production planning. | [manufacturing](#manufacturing) | — |
| ORIG-209 | L472: - Production schedules. | [manufacturing](#manufacturing) | — |
| ORIG-210 | L473: - Daily production entries. | [manufacturing](#manufacturing) | — |
| ORIG-211 | L474: - Batch creation. | [manufacturing](#manufacturing) | — |
| ORIG-212 | L475: - Batch numbers. | [manufacturing](#manufacturing) | — |
| ORIG-213 | L476: - Manufacturing date. | [manufacturing](#manufacturing) | — |
| ORIG-214 | L477: - Production quantity. | [manufacturing](#manufacturing) | — |
| ORIG-215 | L478: - Raw material consumption. | [manufacturing](#manufacturing) | — |
| ORIG-216 | L479: - Finished goods production. | [manufacturing](#manufacturing) | — |
| ORIG-217 | L480: - Production cost calculation. | [manufacturing](#manufacturing) | — |
| ORIG-218 | L481: - Labor costs. | [manufacturing](#manufacturing) | — |
| ORIG-219 | L482: - Manufacturing expenses. | [manufacturing](#manufacturing) | — |
| ORIG-220 | L483: - Production wastage. | [manufacturing](#manufacturing) | — |
| ORIG-221 | L484: - Rejected products. | [manufacturing](#manufacturing) | — |
| ORIG-222 | L485: - Quality control. | [manufacturing](#manufacturing) | — |
| ORIG-223 | L486: - Batch-wise inventory. | [manufacturing](#manufacturing) | — |
| ORIG-224 | L487: - Batch-wise profitability. | [manufacturing](#manufacturing) | — |
| ORIG-225 | L489: Every manufactured batch must have its own unique identification number. | [manufacturing](#manufacturing) | — |
| ORIG-226 | L491: Track: | [manufacturing](#manufacturing) | — |
| ORIG-227 | L493: - Product name. | [manufacturing](#manufacturing) | — |
| ORIG-228 | L494: - Batch number. | [manufacturing](#manufacturing) | — |
| ORIG-229 | L495: - Manufacturing date. | [manufacturing](#manufacturing) | — |
| ORIG-230 | L496: - Production date. | [manufacturing](#manufacturing) | — |
| ORIG-231 | L497: - Quantity manufactured. | [manufacturing](#manufacturing) | — |
| ORIG-232 | L498: - Raw materials consumed. | [manufacturing](#manufacturing) | — |
| ORIG-233 | L499: - Production cost. | [manufacturing](#manufacturing) | — |
| ORIG-234 | L500: - Remaining quantity. | [manufacturing](#manufacturing) | — |
| ORIG-235 | L501: - Quantity sold. | [manufacturing](#manufacturing) | — |
| ORIG-236 | L502: - Quantity returned. | [manufacturing](#manufacturing) | — |
| ORIG-237 | L503: - Quantity damaged. | [manufacturing](#manufacturing) | — |
| ORIG-238 | L504: - Batch status. | [manufacturing](#manufacturing) | — |
| ORIG-239 | L506: The system must allow production planning by date, including specific weekdays such as Friday and other scheduled production days. | [manufacturing](#manufacturing) | — |
| ORIG-240 | L508: Support configurable weekly and daily production schedules. | [manufacturing](#manufacturing) | — |
| ORIG-241 | L512: Implement batch-level inventory tracking. | [inventory](#inventory) | — |
| ORIG-242 | L514: Features: | [inventory](#inventory) | — |
| ORIG-243 | L516: - Batch-wise stock. | [inventory](#inventory) | — |
| ORIG-244 | L517: - Manufacturing date. | [inventory](#inventory) | — |
| ORIG-245 | L518: - Expiry date, where applicable. | [inventory](#inventory) | — |
| ORIG-246 | L519: - Batch purchase cost. | [inventory](#inventory) | — |
| ORIG-247 | L520: - Batch manufacturing cost. | [inventory](#inventory) | — |
| ORIG-248 | L521: - Batch selling price. | [inventory](#inventory) | — |
| ORIG-249 | L522: - Batch-wise sales history. | [inventory](#inventory) | — |
| ORIG-250 | L523: - Batch returns. | [inventory](#inventory) | — |
| ORIG-251 | L524: - Batch transfers. | [inventory](#inventory) | — |
| ORIG-252 | L525: - Batch availability. | [inventory](#inventory) | — |
| ORIG-253 | L527: Support FIFO and FEFO stock allocation where applicable. | [inventory](#inventory) | — |
| ORIG-254 | L529: Allow the business to select the appropriate batch when selling products. | [inventory](#inventory) | — |
| ORIG-255 | L531: The system must maintain complete traceability from manufacturing or purchasing through final sale. | [inventory](#inventory) | — |
| ORIG-256 | L535: Create an expense tracking module. | [accounting](#accounting) | — |
| ORIG-257 | L537: Categories may include: | [accounting](#accounting) | — |
| ORIG-258 | L539: - Rent. | [accounting](#accounting) | — |
| ORIG-259 | L540: - Electricity. | [accounting](#accounting) | — |
| ORIG-260 | L541: - Salaries. | [accounting](#accounting) | — |
| ORIG-261 | L542: - Transportation. | [accounting](#accounting) | — |
| ORIG-262 | L543: - Fuel. | [accounting](#accounting) | — |
| ORIG-263 | L544: - Maintenance. | [accounting](#accounting) | — |
| ORIG-264 | L545: - Manufacturing expenses. | [accounting](#accounting) | — |
| ORIG-265 | L546: - Packaging. | [accounting](#accounting) | — |
| ORIG-266 | L547: - Miscellaneous expenses. | [accounting](#accounting) | — |
| ORIG-267 | L549: Support expense receipts, dates, payment methods, categories, and accounting entries. | [accounting](#accounting) | — |
| ORIG-268 | L553: Implement: | [accounting](#accounting) | — |
| ORIG-269 | L555: - Multiple cash accounts. | [accounting](#accounting) | — |
| ORIG-270 | L556: - Multiple bank accounts. | [accounting](#accounting) | — |
| ORIG-271 | L557: - Cash deposits. | [accounting](#accounting) | — |
| ORIG-272 | L558: - Cash withdrawals. | [accounting](#accounting) | — |
| ORIG-273 | L559: - Bank transfers. | [accounting](#accounting) | — |
| ORIG-274 | L560: - Cash opening balances. | [accounting](#accounting) | — |
| ORIG-275 | L561: - Daily cash closing. | [accounting](#accounting) | — |
| ORIG-276 | L562: - Cash reconciliation. | [accounting](#accounting) | — |
| ORIG-277 | L563: - Bank reconciliation. | [accounting](#accounting) | — |
| ORIG-278 | L564: - Cash transaction history. | [accounting](#accounting) | — |
| ORIG-279 | L565: - Cash-in-hand reporting. | [accounting](#accounting) | — |
| ORIG-280 | L569: Support: | [trade](#trade) | — |
| ORIG-281 | L571: - Customer sales returns. | [trade](#trade) | — |
| ORIG-282 | L572: - Supplier purchase returns. | [trade](#trade) | — |
| ORIG-283 | L573: - Damaged goods. | [trade](#trade) | — |
| ORIG-284 | L574: - Stock corrections. | [trade](#trade) | — |
| ORIG-285 | L575: - Credit notes. | [trade](#trade) | — |
| ORIG-286 | L576: - Debit notes. | [trade](#trade) | — |
| ORIG-287 | L577: - Refunds. | [trade](#trade) | — |
| ORIG-288 | L578: - Account adjustments. | [trade](#trade) | — |
| ORIG-289 | L580: Every return must correctly update inventory and accounting records. | [trade](#trade) | — |
| ORIG-290 | L586: Create a dedicated reporting center. | [reports](#reports) | — |
| ORIG-291 | L588: Required reports: | [reports](#reports) | — |
| R01.01 | L591: - Current stock report. | [reports](#reports) | — |
| R01.02 | L592: - Stock movement report. | [reports](#reports) | — |
| R01.03 | L593: - Stock valuation. | [reports](#reports) | — |
| R01.04 | L594: - Low-stock report. | [reports](#reports) | — |
| R01.05 | L595: - Out-of-stock report. | [reports](#reports) | — |
| R01.06 | L596: - Batch-wise stock. | [reports](#reports) | — |
| R01.07 | L597: - Warehouse-wise stock. | [reports](#reports) | — |
| R01.08 | L598: - Damaged stock report. | [reports](#reports) | — |
| R01.09 | L601: - Daily sales. | [reports](#reports) | — |
| R01.10 | L602: - Weekly sales. | [reports](#reports) | — |
| R01.11 | L603: - Monthly sales. | [reports](#reports) | — |
| R01.12 | L604: - Annual sales. | [reports](#reports) | — |
| R01.13 | L605: - Customer-wise sales. | [reports](#reports) | — |
| R01.14 | L606: - Product-wise sales. | [reports](#reports) | — |
| R01.15 | L607: - Profit margin report. | [reports](#reports) | — |
| R01.16 | L608: - Credit sales report. | [reports](#reports) | — |
| R01.17 | L609: - Cash sales report. | [reports](#reports) | — |
| R01.18 | L612: - Supplier-wise purchases. | [reports](#reports) | — |
| R01.19 | L613: - Product-wise purchases. | [reports](#reports) | — |
| R01.20 | L614: - Purchase returns. | [reports](#reports) | — |
| R01.21 | L615: - Outstanding purchases. | [reports](#reports) | — |
| R01.22 | L616: - Purchase history. | [reports](#reports) | — |
| R01.23 | L619: - Customer ledger. | [reports](#reports) | — |
| R01.24 | L620: - Supplier ledger. | [reports](#reports) | — |
| R01.25 | L621: - General ledger. | [reports](#reports) | — |
| R01.26 | L622: - Cash book. | [reports](#reports) | — |
| R01.27 | L623: - Bank book. | [reports](#reports) | — |
| R01.28 | L624: - Trial balance. | [reports](#reports) | — |
| R01.29 | L625: - Profit and loss. | [reports](#reports) | — |
| R01.30 | L626: - Balance sheet. | [reports](#reports) | — |
| R01.31 | L627: - Cash flow. | [reports](#reports) | — |
| R01.32 | L628: - Receivables aging. | [reports](#reports) | — |
| R01.33 | L629: - Payables aging. | [reports](#reports) | — |
| R01.34 | L632: - Daily production. | [reports](#reports) | — |
| R01.35 | L633: - Batch-wise production. | [reports](#reports) | — |
| R01.36 | L634: - Manufacturing cost. | [reports](#reports) | — |
| R01.37 | L635: - Raw material consumption. | [reports](#reports) | — |
| R01.38 | L636: - Production wastage. | [reports](#reports) | — |
| R01.39 | L637: - Finished goods. | [reports](#reports) | — |
| R01.40 | L638: - Batch profitability. | [reports](#reports) | — |
| ORIG-332 | L640: Allow filtering by date range, product, customer, supplier, category, and warehouse. | [reports](#reports) | — |
| ORIG-333 | L642: Provide PDF and Excel export functionality. | [reports](#reports) | — |
| ORIG-334 | L648: Implement secure authentication and role-based access control. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-335 | L650: Suggested roles: | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-336 | L652: - Super Admin. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-337 | L653: - Business Owner. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-338 | L654: - Manager. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-339 | L655: - Accountant. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-340 | L656: - Inventory Manager. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-341 | L657: - Sales Operator. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-342 | L658: - Purchase Operator. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-343 | L659: - Production Manager. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-344 | L660: - Read-only User. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-345 | L662: Permissions should be configurable by module and action. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-346 | L664: For example: | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-347 | L666: - View. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-348 | L667: - Create. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-349 | L668: - Edit. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-350 | L669: - Delete. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-351 | L670: - Approve. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-352 | L671: - Export. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-353 | L672: - Manage Financial Records. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-354 | L674: Implement an audit log for sensitive operations. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| ORIG-355 | L680: The frontend must look like a modern, professional commercial ERP dashboard. | [ui](#ui) | — |
| ORIG-356 | L682: Design requirements: | [ui](#ui) | — |
| ORIG-357 | L684: - Clean and professional interface. | [ui](#ui) | — |
| ORIG-358 | L685: - Responsive layout. | [ui](#ui) | — |
| ORIG-359 | L686: - Sidebar navigation. | [ui](#ui) | — |
| ORIG-360 | L687: - Top navigation bar. | [ui](#ui) | — |
| ORIG-361 | L688: - Dashboard cards. | [ui](#ui) | — |
| ORIG-362 | L689: - Interactive charts. | [ui](#ui) | — |
| ORIG-363 | L690: - Advanced searchable tables. | [ui](#ui) | — |
| ORIG-364 | L691: - Pagination. | [ui](#ui) | — |
| ORIG-365 | L692: - Date range filters. | [ui](#ui) | — |
| ORIG-366 | L693: - Dropdown filters. | [ui](#ui) | — |
| ORIG-367 | L694: - Professional forms. | [ui](#ui) | — |
| ORIG-368 | L695: - Confirmation dialogs. | [ui](#ui) | — |
| ORIG-369 | L696: - Loading states. | [ui](#ui) | — |
| ORIG-370 | L697: - Error handling. | [ui](#ui) | — |
| ORIG-371 | L698: - Toast notifications. | [ui](#ui) | — |
| ORIG-372 | L699: - Dark and light mode. | [ui](#ui) | — |
| ORIG-373 | L701: Use a consistent design system with reusable components. | [ui](#ui) | — |
| ORIG-374 | L703: Prioritize usability and data visibility. The application must be easy for accountants, shop operators, inventory managers, and business owners to operate. | [ui](#ui) | — |
| ORIG-375 | L709: Use PostgreSQL with properly normalized relational database tables. | [architecture](#architecture) | — |
| ORIG-376 | L711: Create appropriate relationships, indexes, foreign keys, constraints, and transaction boundaries. | [architecture](#architecture) | — |
| ORIG-377 | L713: Important entities should include: | [architecture](#architecture) | — |
| ORIG-378 | L715: - Users | [architecture](#architecture) | — |
| ORIG-379 | L716: - Roles | [architecture](#architecture) | — |
| ORIG-380 | L717: - Permissions | [architecture](#architecture) | — |
| ORIG-381 | L718: - Products | [architecture](#architecture) | — |
| ORIG-382 | L719: - Categories | [architecture](#architecture) | — |
| ORIG-383 | L720: - Brands | [architecture](#architecture) | — |
| ORIG-384 | L721: - Warehouses | [architecture](#architecture) | — |
| ORIG-385 | L722: - Inventory Transactions | [architecture](#architecture) | — |
| ORIG-386 | L723: - Stock Balances | [architecture](#architecture) | — |
| ORIG-387 | L724: - Batches | [architecture](#architecture) | — |
| ORIG-388 | L725: - Manufacturing Orders | [architecture](#architecture) | — |
| ORIG-389 | L726: - Production Records | [architecture](#architecture) | — |
| ORIG-390 | L727: - Raw Materials | [architecture](#architecture) | — |
| ORIG-391 | L728: - Bills of Materials | [architecture](#architecture) | — |
| ORIG-392 | L729: - Customers | [architecture](#architecture) | — |
| ORIG-393 | L730: - Suppliers | [architecture](#architecture) | — |
| ORIG-394 | L731: - Vendors | [architecture](#architecture) | — |
| ORIG-395 | L732: - Purchase Orders | [architecture](#architecture) | — |
| ORIG-396 | L733: - Purchase Items | [architecture](#architecture) | — |
| ORIG-397 | L734: - Sales Invoices | [architecture](#architecture) | — |
| ORIG-398 | L735: - Sales Items | [architecture](#architecture) | — |
| ORIG-399 | L736: - Payments | [architecture](#architecture) | — |
| ORIG-400 | L737: - Expenses | [architecture](#architecture) | — |
| ORIG-401 | L738: - Accounts | [architecture](#architecture) | — |
| ORIG-402 | L739: - Journal Entries | [architecture](#architecture) | — |
| ORIG-403 | L740: - Journal Entry Lines | [architecture](#architecture) | — |
| ORIG-404 | L741: - Customer Ledgers | [architecture](#architecture) | — |
| ORIG-405 | L742: - Supplier Ledgers | [architecture](#architecture) | — |
| ORIG-406 | L743: - Returns | [architecture](#architecture) | — |
| ORIG-407 | L744: - Audit Logs | [architecture](#architecture) | — |
| ORIG-408 | L746: Use database transactions for operations that update multiple related records. | [architecture](#architecture) | — |
| ORIG-409 | L748: Prevent duplicate invoices, invalid stock movements, unbalanced journal entries, and inconsistent account balances. | [architecture](#architecture) | — |
| ORIG-410 | L750: Maintain historical transaction records rather than permanently deleting finalized financial or inventory transactions. | [architecture](#architecture) | — |
| ORIG-411 | L756: The following rules must be followed: | [architecture](#architecture) | — |
| ORIG-412 | L758: 1. Every purchase and sale must be traceable. | [architecture](#architecture) | — |
| ORIG-413 | L759: 2. Every finalized stock movement must update inventory. | [architecture](#architecture) | — |
| ORIG-414 | L760: 3. Every credit transaction must update the relevant outstanding balance. | [architecture](#architecture) | — |
| ORIG-415 | L761: 4. Every cash transaction must update the relevant cash account. | [architecture](#architecture) | — |
| ORIG-416 | L762: 5. Partial payments must be supported. | [architecture](#architecture) | — |
| ORIG-417 | L763: 6. Every financial transaction must maintain double-entry accounting integrity. | [architecture](#architecture) | — |
| ORIG-418 | L764: 7. Manufacturing must create batch-wise finished goods. | [architecture](#architecture) | — |
| ORIG-419 | L765: 8. Raw material consumption must reduce raw material inventory. | [architecture](#architecture) | — |
| ORIG-420 | L766: 9. Finished goods production must increase finished goods inventory. | [architecture](#architecture) | — |
| ORIG-421 | L767: 10. Sales must reduce the correct product and batch stock. | [architecture](#architecture) | — |
| ORIG-422 | L768: 11. Returns must reverse the appropriate inventory and financial effects. | [architecture](#architecture) | — |
| ORIG-423 | L769: 12. Every important operation must have an audit trail. | [architecture](#architecture) | — |
| ORIG-424 | L770: 13. Use decimal-based financial calculations, never floating-point arithmetic for money. | [architecture](#architecture) | — |
| ORIG-425 | L771: 14. Prevent negative stock unless explicitly enabled by an authorized administrator. | [architecture](#architecture) | — |
| ORIG-426 | L772: 15. Historical reports must remain accurate even when product prices change. | [architecture](#architecture) | — |
| ORIG-427 | L778: Do not attempt to build the entire system in one step. | [architecture](#architecture) | — |
| ORIG-428 | L780: Follow a phased development approach. | [architecture](#architecture) | — |
| ORIG-429 | L783: - Project initialization. | [foundation](#foundation) | — |
| ORIG-430 | L784: - Frontend and backend setup. | [foundation](#foundation) | — |
| ORIG-431 | L785: - PostgreSQL connection. | [foundation](#foundation) | — |
| ORIG-432 | L786: - Database configuration. | [foundation](#foundation) | — |
| ORIG-433 | L787: - Authentication. | [foundation](#foundation) | — |
| ORIG-434 | L788: - Dashboard layout. | [foundation](#foundation) | — |
| ORIG-435 | L789: - Initial database migrations. | [foundation](#foundation) | — |
| ORIG-436 | L792: - Products. | [master](#master) | — |
| ORIG-437 | L793: - Categories. | [master](#master) | — |
| ORIG-438 | L794: - Units. | [master](#master) | — |
| ORIG-439 | L795: - Brands. | [master](#master) | — |
| ORIG-440 | L796: - Customers. | [master](#master) | — |
| ORIG-441 | L797: - Suppliers. | [master](#master) | — |
| ORIG-442 | L798: - Vendors. | [master](#master) | — |
| ORIG-443 | L799: - Warehouses. | [master](#master) | — |
| ORIG-444 | L802: - Stock opening. | [inventory](#inventory) | — |
| ORIG-445 | L803: - Stock in/out. | [inventory](#inventory) | — |
| ORIG-446 | L804: - Inventory movements. | [inventory](#inventory) | — |
| ORIG-447 | L805: - Stock transfers. | [inventory](#inventory) | — |
| ORIG-448 | L806: - Stock valuation. | [inventory](#inventory) | — |
| ORIG-449 | L807: - Low-stock alerts. | [inventory](#inventory) | — |
| ORIG-450 | L810: - Purchase orders. | [trade](#trade) | — |
| ORIG-451 | L811: - Receiving. | [trade](#trade) | — |
| ORIG-452 | L812: - Sales invoices. | [trade](#trade) | — |
| ORIG-453 | L813: - POS. | [trade](#trade) | — |
| ORIG-454 | L814: - Cash and credit transactions. | [trade](#trade) | — |
| ORIG-455 | L815: - Returns. | [trade](#trade) | — |
| ORIG-456 | L818: - Chart of accounts. | [accounting](#accounting) | — |
| ORIG-457 | L819: - Double-entry accounting. | [accounting](#accounting) | — |
| ORIG-458 | L820: - Customer and supplier ledgers. | [accounting](#accounting) | — |
| ORIG-459 | L821: - Payments. | [accounting](#accounting) | — |
| ORIG-460 | L822: - Expenses. | [accounting](#accounting) | — |
| ORIG-461 | L823: - Financial statements. | [accounting](#accounting) | — |
| ORIG-462 | L826: - Production planning. | [manufacturing](#manufacturing) | — |
| ORIG-463 | L827: - Raw materials. | [manufacturing](#manufacturing) | — |
| ORIG-464 | L828: - BOM. | [manufacturing](#manufacturing) | — |
| ORIG-465 | L829: - Manufacturing orders. | [manufacturing](#manufacturing) | — |
| ORIG-466 | L830: - Batch management. | [manufacturing](#manufacturing) | — |
| ORIG-467 | L831: - Production costing. | [manufacturing](#manufacturing) | — |
| ORIG-468 | L832: - Quality control. | [manufacturing](#manufacturing) | — |
| ORIG-469 | L835: - Business dashboard. | [reports](#reports) | — |
| ORIG-470 | L836: - Inventory reports. | [reports](#reports) | — |
| ORIG-471 | L837: - Financial reports. | [reports](#reports) | — |
| ORIG-472 | L838: - Manufacturing reports. | [reports](#reports) | — |
| ORIG-473 | L839: - PDF and Excel exports. | [reports](#reports) | — |
| ORIG-474 | L842: - Unit testing. | [operations](#operations) | — |
| ORIG-475 | L843: - API testing. | [operations](#operations) | — |
| ORIG-476 | L844: - Integration testing. | [operations](#operations) | — |
| ORIG-477 | L845: - Database integrity testing. | [operations](#operations) | — |
| ORIG-478 | L846: - Performance optimization. | [operations](#operations) | — |
| ORIG-479 | L847: - Security checks. | [operations](#operations) | — |
| ORIG-480 | L848: - Deployment preparation. | [operations](#operations) | — |
| ORIG-481 | L854: Follow these instructions strictly: | [architecture](#architecture) | — |
| ORIG-482 | L856: 1. First, inspect the requirements and propose the complete system architecture. | [architecture](#architecture) | — |
| ORIG-483 | L857: 2. Execute the frontend and backend setup commands. | [architecture](#architecture) | — |
| ORIG-484 | L858: 3. Create the professional folder structure. | [architecture](#architecture) | — |
| ORIG-485 | L859: 4. Explain the purpose of each major folder and layer. | [architecture](#architecture) | — |
| ORIG-486 | L860: 5. Design the database schema before implementing business modules. | [architecture](#architecture) | — |
| ORIG-487 | L861: 6. Establish relationships between inventory, accounting, sales, purchases, and manufacturing. | [architecture](#architecture) | — |
| ORIG-488 | L862: 7. Implement reusable services and components. | [architecture](#architecture) | — |
| ORIG-489 | L863: 8. Use proper validation and error handling. | [architecture](#architecture) | — |
| ORIG-490 | L864: 9. Document every API endpoint. | [architecture](#architecture) | — |
| ORIG-491 | L865: 10. Use Swagger/OpenAPI through FastAPI. | [architecture](#architecture) | — |
| ORIG-492 | L866: 11. Write tests for critical business operations. | [architecture](#architecture) | — |
| ORIG-493 | L867: 12. Do not create fake or disconnected functionality. | [architecture](#architecture) | — |
| ORIG-494 | L868: 13. Do not hardcode business data. | [architecture](#architecture) | — |
| ORIG-495 | L869: 14. Do not put all logic into a single file. | [architecture](#architecture) | — |
| ORIG-496 | L870: 15. Do not skip database migrations. | [architecture](#architecture) | — |
| ORIG-497 | L871: 16. Maintain clean, readable, maintainable, production-oriented code. | [architecture](#architecture) | — |
| ORIG-498 | L873: For every phase: | [architecture](#architecture) | — |
| ORIG-499 | L875: - Explain what will be developed. | [architecture](#architecture) | — |
| ORIG-500 | L876: - Identify the database tables involved. | [architecture](#architecture) | — |
| ORIG-501 | L877: - Identify the APIs required. | [architecture](#architecture) | — |
| ORIG-502 | L878: - Implement the backend. | [architecture](#architecture) | — |
| ORIG-503 | L879: - Implement the frontend. | [architecture](#architecture) | — |
| ORIG-504 | L880: - Connect both sides. | [architecture](#architecture) | — |
| ORIG-505 | L881: - Test the functionality. | [architecture](#architecture) | — |
| ORIG-506 | L882: - Document the completed work. | [architecture](#architecture) | — |
| ORIG-507 | L884: Do not move to the next phase until the current phase is implemented and tested. | [architecture](#architecture) | — |
| ORIG-508 | L888: Build a complete, reliable, professional, and scalable ERP system that can manage the entire business from one centralized platform. | [architecture](#architecture) | — |
| ORIG-509 | L890: The system should provide complete visibility into: | [architecture](#architecture) | — |
| ORIG-510 | L892: - What products are available? | [architecture](#architecture) | — |
| ORIG-511 | L893: - How much stock is available? | [architecture](#architecture) | — |
| ORIG-512 | L894: - What was purchased? | [architecture](#architecture) | — |
| ORIG-513 | L895: - What was sold? | [architecture](#architecture) | — |
| ORIG-514 | L896: - How much cash was received? | [architecture](#architecture) | — |
| ORIG-515 | L897: - How much money is outstanding? | [architecture](#architecture) | — |
| ORIG-516 | L898: - How much is owed to suppliers? | [architecture](#architecture) | — |
| ORIG-517 | L899: - What was manufactured today? | [architecture](#architecture) | — |
| ORIG-518 | L900: - Which batches were produced? | [architecture](#architecture) | — |
| ORIG-519 | L901: - What is the manufacturing cost? | [architecture](#architecture) | — |
| ORIG-520 | L902: - What is the actual profit? | [architecture](#architecture) | — |
| ORIG-521 | L903: - What are the total assets, liabilities, income, and expenses? | [architecture](#architecture) | — |
| ORIG-522 | L905: The final product should be suitable for real-world business operations, with accurate accounting, inventory tracking, manufacturing traceability, and comprehensive reporting. | [architecture](#architecture) | — |

### 00_Project_Standards.md

62 indexed source units. [Read the complete document](erp-source/00_Project_Standards.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| STD-001 | L3: These requirements apply to every phase. | [architecture](#architecture) | — |
| STD-002 | L7:  /  Layer  /  Required technologies  /  | [architecture](#architecture) | — |
| STD-003 | L9:  /  Frontend  /  React, Vite, JavaScript ES6+, Tailwind CSS v4, React Router DOM  /  | [architecture](#architecture) | — |
| STD-004 | L10:  /  Forms and requests  /  React Hook Form, Zod, Axios  /  | [architecture](#architecture) | — |
| STD-005 | L11:  /  Visual components  /  Recharts, Lucide React, date-fns  /  | [architecture](#architecture) | — |
| STD-006 | L12:  /  Backend  /  Python, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic  /  | [architecture](#architecture) | — |
| STD-007 | L13:  /  Database  /  PostgreSQL  /  | [architecture](#architecture) | — |
| STD-008 | L14:  /  Authentication  /  JWT with server-enforced permissions  /  | [architecture](#architecture) | — |
| STD-009 | L15:  /  Background work  /  Redis and Celery or a documented equivalent  /  | [architecture](#architecture) | — |
| STD-010 | L16:  /  Operations  /  Docker, Docker Compose, environment configuration, structured logs  /  | [architecture](#architecture) | — |
| STD-011 | L18: Select compatible dependency versions during implementation and commit lockfiles. The original setup commands are preserved in the requirements file; review compatibility before execution. This documentation task does not execu… | [architecture](#architecture) | — |
| STD-012 | L22: Use business-erp/frontend and business-erp/backend, with root-level operational configuration and documentation. | [architecture](#architecture) | — |
| STD-013 | L24: - Frontend: components/common, forms, tables, charts, modals and layout; pages by business module; layouts, services, hooks, context, utils, constants, validations and routes. | [architecture](#architecture) | — |
| STD-014 | L25: - Backend: app/api/v1/endpoints, core, database, models, schemas, repositories, services, dependencies and utils; alembic and tests. | [architecture](#architecture) | — |
| STD-015 | L26: - Routers handle transport and authorization dependencies. Pydantic schemas handle request and response validation. | [architecture](#architecture) | — |
| STD-016 | L27: - Repositories handle persistence; services enforce business rules and coordinate transactions. Avoid repositories that silently commit. | [architecture](#architecture) | — |
| STD-017 | L28: - The initiating service owns the database transaction. Commit related document, stock, financial and audit records together. | [architecture](#architecture) | — |
| STD-018 | L29: - Background workers handle exports, reminders and alerts after commit. They must not be the only mechanism guaranteeing stock or financial integrity. | [architecture](#architecture) | — |
| STD-019 | L31: Document APIs with FastAPI OpenAPI and meaningful response models. | [architecture](#architecture) | — |
| STD-020 | L35: 1. Use PostgreSQL NUMERIC and Python Decimal for money, quantities and rates with explicitly chosen scales. Exchange decimal values as strings where JavaScript arithmetic could lose precision. | [architecture](#architecture) | — |
| STD-021 | L36: 2. Store dated business events and UTC timestamps. Apply the configured business timezone when grouping days and generating schedules. | [architecture](#architecture) | — |
| STD-022 | L37: 3. Give operational documents unique business-scoped numbers; use internal immutable identifiers for relationships. | [architecture](#architecture) | — |
| STD-023 | L38: 4. Snapshot transaction prices, discounts, taxes, unit conversion factors and costs. Later edits to master data must not rewrite history. | [architecture](#architecture) | — |
| STD-024 | L39: 5. Keep finalized stock and financial history immutable. Corrections use linked reversals, returns or adjustment documents. | [architecture](#architecture) | — |
| STD-025 | L40: 6. Require balanced journal entries for financial events. Validate balance at the posting boundary and prevent later direct edits. | [architecture](#architecture) | — |
| STD-026 | L41: 7. Reject negative stock unless an authorized administrator explicitly enables it. Audit policy changes and enforce the same rules across every entry point. | [architecture](#architecture) | — |
| STD-027 | L42: 8. Prevent concurrent overselling with transaction locking or another demonstrated equivalent; a frontend stock check is insufficient. | [architecture](#architecture) | — |
| STD-028 | L43: 9. Use idempotency keys on posting/finalization, payments, returns and production completion. Persist the request fingerprint and result; reject conflicting reuse. | [architecture](#architecture) | — |
| STD-029 | L44: 10. Preserve transaction references and actor identity across documents, inventory movements, batch movements, journal entries and audit records. | [architecture](#architecture) | — |
| STD-030 | L45: 11. Make stock balances and party balances reconcile to their authoritative movement and financial records. | [architecture](#architecture) | — |
| STD-031 | L46: 12. Verify object access and module/action permissions on the backend. Hidden buttons do not authorize requests. | [architecture](#architecture) | — |
| STD-032 | L50: Use a stock transaction header and immutable movement lines. Record product, warehouse, base-unit quantity, unit cost, value, batch where relevant, source document, effective date and actor. Maintain stock balances transactiona… | [architecture](#architecture) | — |
| STD-033 | L52: Keep stock allocation separate from valuation. Physical FIFO selects older stock; FEFO selects the earliest eligible expiry. The financial valuation method is a separate business setting. Do not silently change it after posted … | [architecture](#architecture) | — |
| STD-034 | L54: Use journal entries with at least two journal lines, account, debit or credit, source document and posting date. Entries must balance at configured precision. Business documents reference their posting records. | [architecture](#architecture) | — |
| STD-035 | L56: Customer and supplier ledgers are controlled views or subledgers backed by posted financial events. Do not maintain an unrelated editable balance field as the source of truth. | [architecture](#architecture) | — |
| STD-036 | L58: Recommended document flow: draft → approved where configured → posted/finalized. Document cancellation either discards an unposted draft or creates a linked reversal of a posted document. Define the exact allowed transitions fo… | [architecture](#architecture) | — |
| STD-037 | L62: All phase routes below are proposed contracts under /api/v1. Resolve names consistently in OpenAPI during implementation. | [architecture](#architecture) | — |
| STD-038 | L64: - Use bounded pagination, explicit filters and stable ordering on lists. | [architecture](#architecture) | — |
| STD-039 | L65: - Return consistent validation and business-error envelopes with a request identifier. | [architecture](#architecture) | — |
| STD-040 | L66: - Use 401 for missing/invalid authentication, 403 for forbidden actions, 404 for inaccessible/missing resources, and 409 for state or idempotency conflicts where appropriate. | [architecture](#architecture) | — |
| STD-041 | L67: - Validate quantities, payment allocation totals, dates, statuses and required fields on the server. | [architecture](#architecture) | — |
| STD-042 | L68: - Restrict export, approval, reversal and configuration operations explicitly. | [architecture](#architecture) | — |
| STD-043 | L69: - Version important updates or lock records to reject stale edits. | [architecture](#architecture) | — |
| STD-044 | L70: - Do not expose stack traces, credentials or token values in errors or logs. | [architecture](#architecture) | — |
| STD-045 | L74: Provide a responsive dashboard layout, sidebar, top bar, reusable forms, searchable paginated tables, date and dropdown filters, confirmation dialogs, loading and empty states, useful validation, toast notifications, accessible… | [ui](#ui) | — |
| STD-046 | L76: Every action must call a real API or clearly display that it is unavailable. Disable duplicate submission while requests are pending, then display persisted results from the API. Keep accounting terminology clear for shop opera… | [ui](#ui) | — |
| STD-047 | L80: Define a posting service that accepts a typed business event and source identifier and returns a posting reference. Validate account mappings, period status and idempotency before stock or financial mutations become final. | [architecture](#architecture) | — |
| STD-048 | L82: Typical events include opening_inventory, stock_adjustment, goods_received, supplier_invoice, sale_posted, payment_received, payment_sent, sales_return, purchase_return, production_consumed and production_completed. | [architecture](#architecture) | — |
| STD-049 | L84:  /  Event  /  Example debit  /  Example credit  /  | [architecture](#architecture) | — |
| STD-050 | L86:  /  Opening inventory  /  Inventory  /  Opening balance clearing/equity  /  | [architecture](#architecture) | — |
| STD-051 | L87:  /  Goods received before invoice  /  Inventory  /  Goods received not invoiced clearing  /  | [architecture](#architecture) | — |
| STD-052 | L88:  /  Matched supplier invoice  /  Receipt clearing and recoverable tax where configured  /  Accounts payable  /  | [architecture](#architecture) | — |
| STD-053 | L89:  /  Credit sale  /  Accounts receivable  /  Sales and output tax where configured  /  | [architecture](#architecture) | — |
| STD-054 | L90:  /  Sale cost  /  Cost of goods sold  /  Inventory  /  | [architecture](#architecture) | — |
| STD-055 | L91:  /  Customer payment  /  Cash/bank  /  Accounts receivable  /  | [architecture](#architecture) | — |
| STD-056 | L92:  /  Supplier payment  /  Accounts payable  /  Cash/bank  /  | [architecture](#architecture) | — |
| STD-057 | L93:  /  Production consumption  /  Work in progress  /  Raw material inventory  /  | [architecture](#architecture) | — |
| STD-058 | L94:  /  Production completion  /  Finished goods inventory  /  Work in progress  /  | [architecture](#architecture) | — |
| STD-059 | L96: These are implementation examples, not jurisdiction-specific accounting policy. Discounts, purchase costs, variances, tax recoverability, wastage and opening balances need explicit configured treatment. Recognize receiving and … | [architecture](#architecture) | — |
| STD-060 | L100: Critical checks cover authorization, database constraints, atomic rollback, duplicate requests, concurrent requests, decimal rounding and historical reporting. Test against PostgreSQL for locking and database behavior. | [operations](#operations) | — |
| STD-061 | L102: Document meaningful success and failure cases in each phase. Keep a repeatable fixture set for cash/credit sales, partial receipts, partial settlements, returns and production. Record actual test results only after execution. | [operations](#operations) | — |
| STD-062 | L104: Never advance with broken posting integrity, disconnected frontend workflows, unapplied migrations or undocumented material blockers. | [operations](#operations) | — |

### 01_Phase_1_Foundation.md

47 indexed source units. [Read the complete document](erp-source/01_Phase_1_Foundation.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P1-001 | L5: Create a runnable, modular ERP foundation with PostgreSQL, authentication, permissions, initial migrations and a professional dashboard layout. Establish shared data integrity and financial posting infrastructure before transac… | [foundation](#foundation) | — |
| P1-002 | L9: Read the original requirements and shared standards. Inspect any existing repository before generating files. Confirm the business configuration assumptions and select compatible dependencies without hardcoding credentials. | [foundation](#foundation) | — |
| P1-003 | L13: 1. Initialize the React/Vite frontend and FastAPI backend under business-erp. | [foundation](#foundation) | — |
| P1-004 | L14: 2. Configure Tailwind CSS v4 through its Vite plugin, routing, Axios, forms, validation, icons and charts. | [foundation](#foundation) | — |
| P1-005 | L15: 3. Create the required backend layers and frontend module folders. | [foundation](#foundation) | — |
| P1-006 | L16: 4. Configure PostgreSQL, SQLAlchemy sessions, Alembic and environment-based settings. | [foundation](#foundation) | — |
| P1-007 | L17: 5. Add authentication, server-side permissions, audit infrastructure and the minimal journal posting contract. | [foundation](#foundation) | — |
| P1-008 | L18: 6. Build the responsive dashboard shell, login screens, theme toggle and reusable UI primitives. | [foundation](#foundation) | — |
| P1-009 | L19: 7. Add Docker Compose, health checks, structured logging and developer documentation. | [foundation](#foundation) | — |
| P1-010 | L21: Use Redis and worker service configuration when required. Separate public web, API, worker and database responsibilities; workers must use the same domain services as synchronous operations. | [foundation](#foundation) | — |
| P1-011 | L25:  /  Tables  /  Responsibility  /  | [foundation](#foundation) | — |
| P1-012 | L27:  /  businesses, business_settings  /  Base currency, timezone, fiscal year and operational configuration  /  | [foundation](#foundation) | — |
| P1-013 | L28:  /  users, roles, permissions, user_roles, role_permissions  /  Identity and action-level access  /  | [foundation](#foundation) | — |
| P1-014 | L29:  /  refresh_sessions  /  Refresh token/session revocation when this strategy is selected  /  | [foundation](#foundation) | — |
| P1-015 | L30:  /  audit_logs  /  Actor, operation, resource and timestamp for sensitive events  /  | [foundation](#foundation) | — |
| P1-016 | L31:  /  document_sequences, idempotency_records  /  Unique references and safe retry infrastructure  /  | [foundation](#foundation) | — |
| P1-017 | L32:  /  accounts, journal_entries, journal_entry_lines  /  Minimal balanced posting kernel, expanded in Phase 5  /  | [foundation](#foundation) | — |
| P1-018 | L34: Create migrations with foreign keys, uniqueness, amount checks and appropriate indexes. Define role defaults: Super Admin, Business Owner, Manager, Accountant, Inventory Manager, Sales Operator, Purchase Operator, Production Ma… | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| P1-019 | L36: The accounting kernel must enforce balancing through a controlled posting service; a row-level CHECK alone cannot sum all journal lines. Keep journal tables protected from direct uncontrolled writes. | [foundation](#foundation) | — |
| P1-020 | L40:  /  Method  /  Route  /  Behavior  /  | [foundation](#foundation) | — |
| P1-021 | L42:  /  GET  /  /health/live  /  Process health  /  | [foundation](#foundation) | — |
| P1-022 | L43:  /  GET  /  /health/ready  /  Required dependency readiness  /  | [foundation](#foundation) | — |
| P1-023 | L44:  /  POST  /  /auth/login  /  Verify credentials and establish authentication  /  | [foundation](#foundation) | — |
| P1-024 | L45:  /  POST  /  /auth/refresh  /  Rotate/renew authentication under the selected strategy  /  | [foundation](#foundation) | — |
| P1-025 | L46:  /  POST  /  /auth/logout  /  Revoke refresh/session credentials  /  | [foundation](#foundation) | — |
| P1-026 | L47:  /  GET  /  /auth/me  /  Current user and effective permissions  /  | [foundation](#foundation) | — |
| P1-027 | L48:  /  GET/POST  /  /users  /  Authorized user listing and creation  /  | [foundation](#foundation) | — |
| P1-028 | L49:  /  GET/PATCH  /  /users/{id}  /  View or update an authorized user  /  | [foundation](#foundation) | — |
| P1-029 | L50:  /  GET/POST/PATCH  /  /roles and /roles/{id}  /  Permission administration  /  | [foundation](#foundation) | — |
| P1-030 | L51:  /  GET/PATCH  /  /settings/business  /  Authorized business configuration  /  | [foundation](#foundation) | — |
| P1-031 | L52:  /  GET  /  /dashboard/summary  /  Real initial metrics or a clear no-data response  /  | [foundation](#foundation) | — |
| P1-032 | L54: All routes except health checks and authentication entry points require appropriate authorization. | [foundation](#foundation) | — |
| P1-033 | L58: Implement configuration validation, password hashing, token expiration, refresh/session handling, CORS configuration, request IDs and a common error format. Never issue known default passwords or log tokens. Use a controlled fi… | [foundation](#foundation) | — |
| P1-034 | L60: Create service boundaries for inventory and accounting even before full workflows exist. Define the posting event contract, source uniqueness, period validation extension points, and transaction ownership. Account mappings used… | [foundation](#foundation) | — |
| P1-035 | L64: Implement AuthLayout and DashboardLayout, protected routes, sidebar navigation and a top bar with user controls. Build reusable inputs, selects, buttons, tables, modals, date filters, toast messages and loading/empty/error comp… | [foundation](#foundation) | — |
| P1-036 | L66: Show business dashboard placeholders as “No transactions yet” when appropriate. Do not populate business metrics with fabricated values. Display permission-based navigation while retaining backend enforcement. | [foundation](#foundation) | — |
| P1-037 | L70: - A fresh developer can start the services from the documented instructions. | [foundation](#foundation) | — |
| P1-038 | L71: - Alembic creates a clean database successfully and the application connects. | [foundation](#foundation) | — |
| P1-039 | L72: - Valid login works; invalid credentials and expired authentication fail consistently. | [foundation](#foundation) | — |
| P1-040 | L73: - A Read-only User cannot create users or update settings through direct API calls. | [foundation](#foundation) | OVR-ROLES-01: apply confirmed nine role names; read-only acceptance applies to Viewer |
| P1-041 | L74: - Session revocation/refresh behavior matches the documented strategy. | [foundation](#foundation) | — |
| P1-042 | L75: - Posting an unbalanced journal fails without committing journal or audit fragments. | [foundation](#foundation) | — |
| P1-043 | L76: - Reusing the same posting source cannot create a second finalized posting. | [foundation](#foundation) | — |
| P1-044 | L77: - Responsive navigation, keyboard focus and theme persistence work. | [foundation](#foundation) | — |
| P1-045 | L78: - Health responses and logs do not expose secrets. | [foundation](#foundation) | — |
| P1-046 | L82: Deliver the initialized repository, dependency lockfiles, .env.example, Docker configuration, migration history, authentication API documentation and a working connected dashboard shell. | [foundation](#foundation) | — |
| P1-047 | L84: Record actual verification results and setup steps. Exit only when authentication, permission boundaries, clean database initialization and the posting contract are demonstrably usable by later phases. | [foundation](#foundation) | — |

### 02_Phase_2_Master_Data.md

45 indexed source units. [Read the complete document](erp-source/02_Phase_2_Master_Data.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P2-001 | L5: Create the reliable shared records required by inventory, purchasing, sales, manufacturing and accounting. | [master](#master) | — |
| P2-002 | L9: Phase 1 passes its exit criteria. Shared forms, tables, authorization and migrations are available. Decide the base unit and quantity precision rules before stock is introduced. | [master](#master) | — |
| P2-003 | L15: Support unique SKU, name, barcode/QR identifiers, category and subcategory, brand/manufacturer, description, purchase reference price, wholesale/retail price, minimum selling price, minimum stock, image, supplier associations a… | [master](#master) | — |
| P2-004 | L17: Products may represent motorcycle spare parts, electrical meters, accessories, general trading goods, raw materials and finished goods. Model commercial classification separately from inventory/manufacturing behavior where useful. | [master](#master) | — |
| P2-005 | L19: Current stock is calculated from inventory records in Phase 3. Product editing must never directly overwrite it. Product history includes material master-data changes and links to later business transactions. | [master](#master) | — |
| P2-006 | L23: Support units, product-specific conversions, categories with parent-child relationships, brands/manufacturers and warehouses. Document whether fractional quantities are allowed for each unit. | [master](#master) | — |
| P2-007 | L27: Support profiles, contacts, addresses, credit limits where relevant, due-date/payment-term configuration and opening-balance input staged for controlled accounting posting. One party may have both customer and supplier roles wi… | [master](#master) | — |
| P2-008 | L29: Opening receivable/payable balances must remain drafts until the accounting posting service validates and posts them. Final historical totals are derived from transactions. | [master](#master) | — |
| P2-009 | L33:  /  Tables  /  Responsibility  /  | [master](#master) | — |
| P2-010 | L35:  /  units, product_unit_conversions  /  Base units, allowed quantities and conversions  /  | [master](#master) | — |
| P2-011 | L36:  /  categories, brands, manufacturers  /  Classification  /  | [master](#master) | — |
| P2-012 | L37:  /  products, product_images, product_suppliers  /  Catalog and vendor associations  /  | [master](#master) | — |
| P2-013 | L38:  /  parties, party_roles, party_contacts, party_addresses  /  Shared customer/supplier/vendor identity  /  | [master](#master) | — |
| P2-014 | L39:  /  customer_profiles, supplier_profiles, vendor_profiles  /  Role-specific terms and limits  /  | [master](#master) | — |
| P2-015 | L40:  /  warehouses  /  Stock locations  /  | [master](#master) | — |
| P2-016 | L41:  /  opening_balance_drafts  /  Controlled party opening balance preparation  /  | [master](#master) | — |
| P2-017 | L43: A normalized shared party model is a proposed implementation choice. Separate customer/supplier tables are also acceptable if shared identities and reconciliation remain explicit. | [master](#master) | — |
| P2-018 | L45: Enforce business-scoped SKU uniqueness, valid prices, positive conversion factors and unique configured identifiers. Block category cycles. Archive referenced master records rather than deleting transaction history. | [master](#master) | — |
| P2-019 | L49:  /  Method  /  Route  /  Behavior  /  | [master](#master) | — |
| P2-020 | L51:  /  GET/POST  /  /products  /  Search/filter products or create  /  | [master](#master) | — |
| P2-021 | L52:  /  GET/PATCH  /  /products/{id}  /  Product details and authorized edits  /  | [master](#master) | — |
| P2-022 | L53:  /  POST  /  /products/{id}/archive  /  Deactivate with audit  /  | [master](#master) | — |
| P2-023 | L54:  /  GET  /  /products/{id}/history  /  Product change and transaction history  /  | [master](#master) | — |
| P2-024 | L55:  /  POST/DELETE  /  /products/{id}/images and /products/{id}/images/{image_id}  /  Manage images  /  | [master](#master) | — |
| P2-025 | L56:  /  GET/POST/PATCH  /  /categories, /brands, /units, /manufacturers  /  Maintain catalog lookups  /  | [master](#master) | — |
| P2-026 | L57:  /  GET/POST/PATCH  /  /warehouses and /warehouses/{id}  /  Maintain warehouses  /  | [master](#master) | — |
| P2-027 | L58:  /  GET/POST/PATCH  /  /customers, /suppliers, /vendors  /  Maintain party roles and profiles  /  | [master](#master) | — |
| P2-028 | L59:  /  GET  /  /parties/{id}/summary  /  Available activity totals with clear initial state  /  | [master](#master) | — |
| P2-029 | L60:  /  POST  /  /parties/{id}/opening-balance-drafts  /  Prepare opening balance for controlled posting  /  | [master](#master) | — |
| P2-030 | L61:  /  GET  /  /products/{id}/barcode  /  Produce printable barcode/QR representation  /  | [master](#master) | — |
| P2-031 | L63: Define item routes for updates consistently rather than updating an entire collection. | [master](#master) | — |
| P2-032 | L67: Implement validated models, schemas, repositories and services. Restrict image types and size, store images through a configurable storage abstraction, and prevent user-supplied file paths from controlling storage locations. | [master](#master) | — |
| P2-033 | L69: Prevent deletion of referenced units, warehouses and parties. Do not allow base-unit conversion changes to reinterpret historical quantities. Return paginated search results and server-derived totals. | [master](#master) | — |
| P2-034 | L73: Build searchable product and party tables, detail pages, create/edit forms, image previews, archive confirmation and status filters. Include product unit conversions and supplier associations. | [master](#master) | — |
| P2-035 | L75: Show customer credit limits and configured terms clearly. Mark opening balances as pending until posted. Display barcode/QR previews and print support. Use consistent server and client validation with useful field-level errors. | [master](#master) | — |
| P2-036 | L79: - Duplicate SKU or configured unique barcode is rejected, including concurrent requests. | [master](#master) | — |
| P2-037 | L80: - Invalid prices, zero/negative conversion factors and circular categories fail. | [master](#master) | — |
| P2-038 | L81: - A party can hold customer and supplier roles while balances stay separate. | [master](#master) | — |
| P2-039 | L82: - Referenced records are archived or blocked from deletion safely. | [master](#master) | — |
| P2-040 | L83: - Image validation and permission checks work. | [master](#master) | — |
| P2-041 | L84: - Searching, filtering and pagination use real backend data. | [master](#master) | — |
| P2-042 | L85: - Product stock cannot be changed through a catalog update. | [master](#master) | — |
| P2-043 | L86: - Opening-balance drafts do not silently change financial statements. | [master](#master) | — |
| P2-044 | L87: - Permission-denied actions fail through direct API requests. | [master](#master) | — |
| P2-045 | L91: Deliver connected master-data screens, migrations, documented APIs and a documented unit/party model. Exit when validated catalog, party and warehouse records are available to downstream modules without manual database editing. | [master](#master) | — |

### 03_Phase_3_Inventory.md

48 indexed source units. [Read the complete document](erp-source/03_Phase_3_Inventory.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P3-001 | L5: Track every stock change with a reference, batch/location context, valuation and audit trail. Maintain accurate opening, available, reserved and closing stock. | [inventory](#inventory) | — |
| P3-002 | L9: Phases 1–2 pass. Products, units and warehouses exist. Configure the negative-stock policy, valuation method, quantity precision and inventory account mappings. | [inventory](#inventory) | — |
| P3-003 | L11: Although detailed batch manufacturing comes later, this phase must support purchased batches and optional expiry dates now. | [inventory](#inventory) | — |
| P3-004 | L15: Implement opening stock, authorized stock in/out, adjustments, damage handling, returns-related movement types, reservations, warehouse transfers, physical counts and reconciliation. | [inventory](#inventory) | — |
| P3-005 | L17: Distinguish on-hand, reserved and available quantities. Exclude quarantined/rejected/expired stock from availability according to configured policy. | [inventory](#inventory) | — |
| P3-006 | L19: Opening and closing reports are period calculations from dated movements. They must not reset stock history. | [inventory](#inventory) | — |
| P3-007 | L21: Support low-stock and reorder alerts, product/warehouse stock visibility, and complete movement history. Support FIFO and FEFO physical allocation when applicable, with explicit handling for batches without expiry. | [inventory](#inventory) | — |
| P3-008 | L25:  /  Tables  /  Responsibility  /  | [inventory](#inventory) | — |
| P3-009 | L27:  /  inventory_transactions, inventory_movements  /  Immutable stock events and signed base-unit movement lines  /  | [inventory](#inventory) | — |
| P3-010 | L28:  /  stock_balances, stock_reservations  /  Transactionally maintained availability  /  | [inventory](#inventory) | — |
| P3-011 | L29:  /  batches, batch_stock_balances  /  Purchased batch identity, dates and warehouse quantities  /  | [inventory](#inventory) | — |
| P3-012 | L30:  /  stock_transfers, stock_transfer_lines  /  Movement between warehouses  /  | [inventory](#inventory) | — |
| P3-013 | L31:  /  stock_counts, stock_count_lines  /  Count sessions and approved variances  /  | [inventory](#inventory) | — |
| P3-014 | L32:  /  inventory_cost_layers or inventory_cost_state  /  Selected valuation implementation  /  | [inventory](#inventory) | — |
| P3-015 | L33:  /  alert_rules, alert_events  /  Reorder configuration and notification history  /  | [inventory](#inventory) | — |
| P3-016 | L35: Link movement records to product, warehouse, batch, source document and journal reference where financially relevant. Constrain balance identity and batch-product consistency. | [inventory](#inventory) | — |
| P3-017 | L39:  /  Method  /  Route  /  Behavior  /  | [inventory](#inventory) | — |
| P3-018 | L41:  /  GET  /  /inventory/balances  /  Filter product, warehouse and batch balances  /  | [inventory](#inventory) | — |
| P3-019 | L42:  /  GET  /  /inventory/movements  /  Paginated movement history and references  /  | [inventory](#inventory) | — |
| P3-020 | L43:  /  POST  /  /inventory/openings  /  Create controlled opening stock  /  | [inventory](#inventory) | — |
| P3-021 | L44:  /  POST  /  /inventory/adjustments  /  Record approved correction or damage  /  | [inventory](#inventory) | — |
| P3-022 | L45:  /  POST  /  /inventory/reservations  /  Reserve available stock for a source  /  | [inventory](#inventory) | — |
| P3-023 | L46:  /  POST  /  /inventory/reservations/{id}/release  /  Release remaining reservation  /  | [inventory](#inventory) | — |
| P3-024 | L47:  /  GET/POST  /  /inventory/transfers  /  View/create transfer drafts  /  | [inventory](#inventory) | — |
| P3-025 | L48:  /  POST  /  /inventory/transfers/{id}/post  /  Atomically post a transfer  /  | [inventory](#inventory) | — |
| P3-026 | L49:  /  GET/POST  /  /inventory/counts  /  View/create physical count sessions  /  | [inventory](#inventory) | — |
| P3-027 | L50:  /  POST  /  /inventory/counts/{id}/finalize  /  Post approved count variances  /  | [inventory](#inventory) | — |
| P3-028 | L51:  /  GET/POST  /  /batches  /  View/create eligible purchased batches  /  | [inventory](#inventory) | — |
| P3-029 | L52:  /  GET  /  /inventory/valuation  /  Value stock as of a specified date  /  | [inventory](#inventory) | — |
| P3-030 | L53:  /  GET  /  /inventory/alerts  /  Low-stock and reorder visibility  /  | [inventory](#inventory) | — |
| P3-031 | L57: Build one inventory service for all modules. Validate product, unit conversion, warehouse, batch status and quantity before posting. Lock balance/cost records consistently to avoid overselling or deadlocks. | [inventory](#inventory) | — |
| P3-032 | L59: Post source and destination transfer lines atomically. A synchronous transfer moves stock immediately; a future dispatched/in-transit/received workflow needs separate state and transit stock, not a hidden subtraction. | [inventory](#inventory) | — |
| P3-033 | L61: Opening stock and value-changing adjustments require balanced accounting postings in the same transaction. A same-business warehouse transfer normally changes location rather than total asset value; preserve source costs. | [inventory](#inventory) | — |
| P3-034 | L63: Finalize physical counts against an explicit count cutoff or reconcile intervening movements. Do not overwrite live balances with an old count. | [inventory](#inventory) | — |
| P3-035 | L65: Record reversals rather than deleting finalized movement lines. Background alerts run after commit and deduplicate repeated notifications. | [inventory](#inventory) | — |
| P3-036 | L69: Build stock overview, product movement detail, opening stock, adjustment forms, batch detail, transfer workflow, count/reconciliation screens and alert views. | [inventory](#inventory) | — |
| P3-037 | L71: Show on-hand, reserved and available separately. Display original unit and converted base quantity. Require a reason and confirmation for adjustments; show financial impact when available. Make unavailable or expired batches cl… | [inventory](#inventory) | — |
| P3-038 | L75: - Opening 100 units and issuing 10 leaves 90 with linked stock and financial references. | [inventory](#inventory) | — |
| P3-039 | L76: - A transfer conserves total business quantity and value while updating both warehouses. | [inventory](#inventory) | — |
| P3-040 | L77: - A failing destination movement rolls back the entire transfer. | [inventory](#inventory) | — |
| P3-041 | L78: - Two concurrent requests cannot consume more than available stock. | [inventory](#inventory) | — |
| P3-042 | L79: - Reservations reduce availability without reducing physical on-hand. | [inventory](#inventory) | — |
| P3-043 | L80: - A count posted after intervening movements produces a correct adjustment. | [inventory](#inventory) | — |
| P3-044 | L81: - FEFO selects the earliest eligible expiry and excludes unusable stock. | [inventory](#inventory) | — |
| P3-045 | L82: - A retry does not duplicate movement or journal lines. | [inventory](#inventory) | — |
| P3-046 | L83: - Historical valuation uses recorded costs, not the current product purchase price. | [inventory](#inventory) | — |
| P3-047 | L84: - Unauthorized users cannot adjust or enable negative stock. | [inventory](#inventory) | — |
| P3-048 | L88: Deliver the shared inventory service, connected stock/batch screens, migrations, valuation decision documentation and concurrency/rollback verification. Exit when stock balances reconcile to movements and value-changing events … | [inventory](#inventory) | — |

### 04_Phase_4_Purchases_and_Sales.md

52 indexed source units. [Read the complete document](erp-source/04_Phase_4_Purchases_and_Sales.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P4-001 | L5: Implement end-to-end purchasing, receiving, wholesale/retail billing, POS, settlements and returns with immediate, consistent inventory and financial effects. | [trade](#trade) | — |
| P4-002 | L9: Phases 1–3 pass. Product/party/location records, inventory allocation, idempotency and the balanced posting kernel work. | [trade](#trade) | — |
| P4-003 | L11: Implement the transaction-specific accounting postings in this phase. Phase 5 adds full accounting management; it does not defer the financial effects of already finalized purchases or sales. | [trade](#trade) | — |
| P4-004 | L15: Support purchase orders, supplier invoices, partial/full receiving, cash and credit purchases, discounts, tax configuration, additional purchase expenses, payment status, supplier history and purchase returns. | [trade](#trade) | — |
| P4-005 | L17: Separate purchase ordering, physical receiving, supplier invoicing and payment. Posting a supplier invoice for goods already received must not add the inventory again. Use receipt clearing and explicit matching when receiving p… | [trade](#trade) | — |
| P4-006 | L19: Track ordered, received, returned and remaining quantities. Reject over-receipt unless a configured authorized tolerance permits it. Allocate landed purchase costs by a documented rule. | [trade](#trade) | — |
| P4-007 | L23: Support sales invoices, a fast POS screen, wholesale/retail price selection, cash/credit sales, partial/full payments, discounts, minimum price rules, cancellation, customer/product history and profit per invoice/product. | [trade](#trade) | — |
| P4-008 | L25: Support cash, bank transfer and configurable payment channels. Validate credit limits, available stock and batch eligibility. Provide printable invoices. | [trade](#trade) | — |
| P4-009 | L27: A credit sale increases receivables; cash increases only when a payment is actually posted. Do not treat an invoice as a receipt of cash. | [trade](#trade) | — |
| P4-010 | L31:  /  Tables  /  Responsibility  /  | [trade](#trade) | — |
| P4-011 | L33:  /  purchase_orders, purchase_order_lines  /  Supplier commitments  /  | [trade](#trade) | — |
| P4-012 | L34:  /  goods_receipts, goods_receipt_lines  /  Actual quantities received  /  | [trade](#trade) | — |
| P4-013 | L35:  /  supplier_invoices, supplier_invoice_lines, receipt_invoice_matches  /  Payables and receipt matching  /  | [trade](#trade) | — |
| P4-014 | L36:  /  sales_invoices, sales_invoice_lines, sales_allocations  /  Billing and batch allocation  /  | [trade](#trade) | — |
| P4-015 | L37:  /  payment_methods, payments, payment_allocations  /  Settlements linked to invoices/parties  /  | [trade](#trade) | — |
| P4-016 | L38:  /  sales_returns, sales_return_lines  /  Customer returns and disposition  /  | [trade](#trade) | — |
| P4-017 | L39:  /  purchase_returns, purchase_return_lines  /  Supplier returns  /  | [trade](#trade) | — |
| P4-018 | L40:  /  credit_notes, debit_notes  /  Financial adjustments with source links  /  | [trade](#trade) | — |
| P4-019 | L41:  /  document_taxes, document_charges  /  Snapshotted taxes and extra costs  /  | [trade](#trade) | — |
| P4-020 | L43: Reuse inventory, journal, idempotency and audit tables. Snapshot prices, costs, terms and taxes. | [trade](#trade) | — |
| P4-021 | L47:  /  Method  /  Route  /  Behavior  /  | [trade](#trade) | — |
| P4-022 | L49:  /  GET/POST  /  /purchases/orders  /  Search/create purchase orders  /  | [trade](#trade) | — |
| P4-023 | L50:  /  GET/PATCH  /  /purchases/orders/{id}  /  View/edit allowed draft fields  /  | [trade](#trade) | — |
| P4-024 | L51:  /  POST  /  /purchases/orders/{id}/approve  /  Approve where configured  /  | [trade](#trade) | — |
| P4-025 | L52:  /  POST  /  /purchases/receipts  /  Post receipt against eligible order lines  /  | [trade](#trade) | — |
| P4-026 | L53:  /  GET/POST  /  /purchases/invoices  /  View/create supplier invoices  /  | [trade](#trade) | — |
| P4-027 | L54:  /  POST  /  /purchases/invoices/{id}/post  /  Post invoice and payable  /  | [trade](#trade) | — |
| P4-028 | L55:  /  GET/POST  /  /sales/invoices  /  View/create sales drafts  /  | [trade](#trade) | — |
| P4-029 | L56:  /  POST  /  /sales/invoices/{id}/post  /  Finalize stock and financial effects  /  | [trade](#trade) | — |
| P4-030 | L57:  /  GET  /  /sales/invoices/{id}/print  /  Printable invoice  /  | [trade](#trade) | — |
| P4-031 | L58:  /  POST  /  /sales/checkout  /  Atomic POS sale and optional settlement  /  | [trade](#trade) | — |
| P4-032 | L59:  /  POST  /  /payments  /  Post receipt/payment and allocations  /  | [trade](#trade) | — |
| P4-033 | L60:  /  GET/POST  /  /sales/returns and /purchases/returns  /  Review/create linked returns  /  | [trade](#trade) | — |
| P4-034 | L61:  /  POST  /  /sales/invoices/{id}/reverse  /  Authorized linked cancellation/reversal  /  | [trade](#trade) | — |
| P4-035 | L62:  /  GET  /  /customers/{id}/transactions and /suppliers/{id}/transactions  /  Party history  /  | [trade](#trade) | — |
| P4-036 | L66: Calculate totals on the server. Validate discounts, taxes and totals using Decimal and explicit rounding. Recalculate outstanding amounts from posted allocations. | [trade](#trade) | — |
| P4-037 | L68: Post document state, inventory movements, journal entries, settlement allocations and audit events within one transaction. For external payment services, introduce explicit pending/confirmed states and reconciliation rather tha… | [trade](#trade) | — |
| P4-038 | L70: Prevent duplicate invoice numbers, double posting, overpayment allocations and returns exceeding eligible original quantities. Returns reference original costs and tax treatment. Separate resalable, damaged and quarantined retu… | [trade](#trade) | — |
| P4-039 | L72: If stock was received but the supplier invoice is pending, preserve the receipt clearing balance. Reversals must consider subsequent allocations and settled amounts; block invalid transitions or require linked corrective docume… | [trade](#trade) | — |
| P4-040 | L76: Build order entry, receiving, supplier billing, sales invoicing, POS product search/barcode input, payment dialogs, invoice print preview and returns screens. | [trade](#trade) | — |
| P4-041 | L78: Show cash received separately from invoice total and remaining balance. Display stock, batch selection, wholesale/retail prices and credit-limit warnings. Show partial receiving and payment states. Disable duplicate posting whi… | [trade](#trade) | — |
| P4-042 | L82: - Receive 4 of 10 ordered units; the order shows 6 outstanding. | [trade](#trade) | — |
| P4-043 | L83: - Invoicing those 4 units does not increase stock a second time. | [trade](#trade) | — |
| P4-044 | L84: - A credit sale of 100 with payment of 40 leaves receivables of 60 and cash increased by 40. | [trade](#trade) | — |
| P4-045 | L85: - A cash sale posts sales, cash and cost-of-goods entries correctly. | [trade](#trade) | — |
| P4-046 | L86: - Concurrent POS requests cannot oversell remaining stock. | [trade](#trade) | — |
| P4-047 | L87: - A failed posting rolls back document, inventory, journal and allocation changes. | [trade](#trade) | — |
| P4-048 | L88: - A return restores only eligible stock and reverses the appropriate revenue/cost/tax effects. | [trade](#trade) | — |
| P4-049 | L89: - Returning a sale made at an old cost preserves historical costing. | [trade](#trade) | — |
| P4-050 | L90: - Repeated checkout/finalization requests return the original result. | [trade](#trade) | — |
| P4-051 | L91: - Operators cannot exceed their price, refund, reversal or approval permissions. | [trade](#trade) | — |
| P4-052 | L95: Deliver connected purchase, sales, POS, payment and return workflows; printable invoices; migrations; API documentation; and verification of atomic stock/accounting behavior. Exit when cash, credit, partial settlements and retu… | [trade](#trade) | — |

### 05_Phase_5_Accounting.md

52 indexed source units. [Read the complete document](erp-source/05_Phase_5_Accounting.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P5-001 | L5: Expand the existing posting kernel into a full double-entry accounting workspace with receivables, payables, payments, expenses, reconciliations and financial statements. | [accounting](#accounting) | — |
| P5-002 | L9: Phases 1–4 pass, including balanced postings from inventory, purchasing and sales. Review and reconcile existing opening inventory, receipt clearing, receivables and payables before exposing financial statements. | [accounting](#accounting) | — |
| P5-003 | L13: Implement Chart of Accounts, General Ledger, Cash Book, Bank Book, journals, cash receipts/payments, AR/AP, income/expenses, Day Book, trial balance, profit and loss, balance sheet, cash flow, opening/closing balances, partial … | [accounting](#accounting) | — |
| P5-004 | L15: Support multiple cash/bank accounts, deposits, withdrawals, bank transfers, daily cash closing, cash reconciliation and bank reconciliation. | [accounting](#accounting) | — |
| P5-005 | L17: Support expense categories such as rent, electricity, salaries, transportation, fuel, maintenance, manufacturing, packaging and miscellaneous expenses. Attach receipts, dates, categories and payment method. | [accounting](#accounting) | — |
| P5-006 | L19: Support due dates, aging, customer/supplier statements and payment reminders. Reminders are authorized business notifications; configure recipients, templates and delivery channels before enabling external sending. | [accounting](#accounting) | — |
| P5-007 | L23:  /  Tables  /  Responsibility  /  | [accounting](#accounting) | — |
| P5-008 | L25:  /  accounts, account_mappings, fiscal_periods  /  Account hierarchy, event mappings and period controls  /  | [accounting](#accounting) | — |
| P5-009 | L26:  /  journal_entries, journal_entry_lines  /  Authoritative balanced postings  /  | [accounting](#accounting) | — |
| P5-010 | L27:  /  cash_bank_accounts  /  Cash/bank identity linked to GL accounts  /  | [accounting](#accounting) | — |
| P5-011 | L28:  /  payments, payment_allocations  /  Settlements, advances and allocations  /  | [accounting](#accounting) | — |
| P5-012 | L29:  /  expense_categories, expenses, expense_attachments  /  Expense capture and supporting receipts  /  | [accounting](#accounting) | — |
| P5-013 | L30:  /  bank_statement_imports, bank_statement_lines  /  Imported statement data and deduplication  /  | [accounting](#accounting) | — |
| P5-014 | L31:  /  reconciliation_sessions, reconciliation_matches  /  Cash/bank comparison and matching  /  | [accounting](#accounting) | — |
| P5-015 | L32:  /  cash_closings  /  Expected, counted and variance records  /  | [accounting](#accounting) | — |
| P5-016 | L33:  /  reminder_rules, reminder_deliveries  /  Authorized reminder history  /  | [accounting](#accounting) | — |
| P5-017 | L35: Prefer ledger views derived from journal lines and party links. If materialized subledger tables exist, reconcile them to the GL and prevent uncontrolled edits. | [accounting](#accounting) | — |
| P5-018 | L39:  /  Method  /  Route  /  Behavior  /  | [accounting](#accounting) | — |
| P5-019 | L41:  /  GET/POST/PATCH  /  /accounting/accounts and /accounting/accounts/{id}  /  Chart of Accounts  /  | [accounting](#accounting) | — |
| P5-020 | L42:  /  GET/POST  /  /accounting/journals  /  Search/create draft journals  /  | [accounting](#accounting) | — |
| P5-021 | L43:  /  POST  /  /accounting/journals/{id}/post  /  Validate and post  /  | [accounting](#accounting) | — |
| P5-022 | L44:  /  POST  /  /accounting/journals/{id}/reverse  /  Linked reversal  /  | [accounting](#accounting) | — |
| P5-023 | L45:  /  GET  /  /accounting/general-ledger  /  Account/date ledger  /  | [accounting](#accounting) | — |
| P5-024 | L46:  /  GET  /  /customers/{id}/ledger and /suppliers/{id}/ledger  /  Party ledgers  /  | [accounting](#accounting) | — |
| P5-025 | L47:  /  GET  /  /accounting/receivables and /accounting/payables  /  Outstanding invoices and aging  /  | [accounting](#accounting) | — |
| P5-026 | L48:  /  GET/POST  /  /expenses  /  View/create expenses  /  | [accounting](#accounting) | — |
| P5-027 | L49:  /  POST  /  /expenses/{id}/post  /  Post expense and payment/payable effect  /  | [accounting](#accounting) | — |
| P5-028 | L50:  /  POST  /  /accounting/transfers  /  Transfer between cash/bank accounts  /  | [accounting](#accounting) | — |
| P5-029 | L51:  /  GET/POST  /  /accounting/reconciliations  /  Create/review reconciliation  /  | [accounting](#accounting) | — |
| P5-030 | L52:  /  POST  /  /accounting/reconciliations/{id}/finalize  /  Close approved reconciliation  /  | [accounting](#accounting) | — |
| P5-031 | L53:  /  POST  /  /accounting/cash-closings  /  Record daily count and approved variance  /  | [accounting](#accounting) | — |
| P5-032 | L54:  /  GET  /  /accounting/statements/{type}  /  Trial balance, P&L, balance sheet or cash flow  /  | [accounting](#accounting) | — |
| P5-033 | L55:  /  POST  /  /accounting/periods/{id}/close  /  Close a reconciled period  /  | [accounting](#accounting) | — |
| P5-034 | L56:  /  POST  /  /accounting/periods/{id}/reopen  /  Privileged, audited reopening  /  | [accounting](#accounting) | — |
| P5-035 | L60: Implement account types, posting restrictions, mapping validation and period locks. Require every journal to balance at currency precision, with exactly one debit/credit direction per line and valid posting accounts. | [accounting](#accounting) | — |
| P5-036 | L62: A transfer debits the receiving cash/bank account and credits the sending account; it does not create income. Allocate receipts/payments without exceeding available amounts. Keep advances visible as unapplied balances until cor… | [accounting](#accounting) | — |
| P5-037 | L64: Stage opening balances, validate total debits equal credits and post them once. Distinguish prior opening balances from ordinary revenue. Do not duplicate stock, customer or supplier openings entered in earlier phases. | [accounting](#accounting) | — |
| P5-038 | L66: Produce statements from posted data with a documented account mapping. Balance sheet assets must reconcile to liabilities plus equity, including current earnings. Derive cash flow from cash movements with configured classificat… | [accounting](#accounting) | — |
| P5-039 | L68: Use as-of dates for aging and statements, including reversals/allocations effective by that date. Protect finalized documents and closed periods. Audit journal posting, mappings, opening balances, reconciliation and period chan… | [accounting](#accounting) | — |
| P5-040 | L72: Build accounting navigation, account tree, journal editor, cash/bank books, party ledgers, outstanding invoice views, allocation dialogs, expense forms, reconciliation matching and statement screens. | [accounting](#accounting) | — |
| P5-041 | L74: Show debits/credits, opening/running/closing balances and statement filters clearly. Display unpaid invoices separately from cash movements. Show unallocated advances and block incomplete journals before submission, with server… | [accounting](#accounting) | — |
| P5-042 | L78: - Unbalanced journals fail and leave no committed lines. | [accounting](#accounting) | — |
| P5-043 | L79: - Credit sales/purchases affect AR/AP without falsely changing cash. | [accounting](#accounting) | — |
| P5-044 | L80: - A partial payment reduces the correct invoice balance once. | [accounting](#accounting) | — |
| P5-045 | L81: - A cash-to-bank transfer preserves total liquid assets and creates no income. | [accounting](#accounting) | — |
| P5-046 | L82: - Aged balances match an as-of-date fixture even after later payments. | [accounting](#accounting) | — |
| P5-047 | L83: - Party subledgers reconcile to control accounts. | [accounting](#accounting) | — |
| P5-048 | L84: - Trial balance debits equal credits; the balance sheet equation holds. | [accounting](#accounting) | — |
| P5-049 | L85: - Repeated opening balance or payment requests do not duplicate postings. | [accounting](#accounting) | — |
| P5-050 | L86: - Bank statement duplicates cannot be imported twice without explicit handling. | [accounting](#accounting) | — |
| P5-051 | L87: - Closed-period backdating and unauthorized reopening fail. | [accounting](#accounting) | — |
| P5-052 | L91: Deliver a connected accounting workspace, documented posting/account mappings, reconciliations, financial statements and integrity verification. Exit only when operational subledgers, inventory valuation and the GL reconcile fo… | [accounting](#accounting) | — |

### 06_Phase_6_Manufacturing.md

50 indexed source units. [Read the complete document](erp-source/06_Phase_6_Manufacturing.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P6-001 | L5: Plan daily or weekly production, consume raw materials, produce traceable finished batches, capture quality outcomes and calculate actual production costs. | [manufacturing](#manufacturing) | — |
| P6-002 | L9: Phases 1–5 pass. Inventory batches, cost tracking, stock transactions, work-in-progress accounts and accounting postings are operational. | [manufacturing](#manufacturing) | — |
| P6-003 | L13: Implement raw materials, Bills of Materials, versioned recipes, manufacturing orders, production planning, configurable weekly/day schedules, daily entries, batch creation, material consumption, finished output, labor, overhead… | [manufacturing](#manufacturing) | — |
| P6-004 | L15: Support specific recurring weekdays such as Friday through configuration. Store schedule timezone, effective date range and exception dates; avoid hardcoded weekdays. | [manufacturing](#manufacturing) | — |
| P6-005 | L17: Every finished batch has a unique business-scoped identifier, product, manufacturing/production date, optional expiry, produced quantity, consumed material references, production cost and status. Show remaining, sold, returned … | [manufacturing](#manufacturing) | — |
| P6-006 | L21:  /  Tables  /  Responsibility  /  | [manufacturing](#manufacturing) | — |
| P6-007 | L23:  /  bills_of_materials, bom_versions, bom_lines  /  Versioned material quantities, units and yields  /  | [manufacturing](#manufacturing) | — |
| P6-008 | L24:  /  production_schedules, production_schedule_exceptions  /  Weekly/daily recurrence and overrides  /  | [manufacturing](#manufacturing) | — |
| P6-009 | L25:  /  manufacturing_orders, manufacturing_order_lines  /  Planned products, quantity and approved BOM snapshot  /  | [manufacturing](#manufacturing) | — |
| P6-010 | L26:  /  production_records  /  Dated production executions  /  | [manufacturing](#manufacturing) | — |
| P6-011 | L27:  /  material_consumptions, material_consumption_lines  /  Actual raw material batch issues  /  | [manufacturing](#manufacturing) | — |
| P6-012 | L28:  /  production_outputs  /  Finished, rejected, rework and scrap output  /  | [manufacturing](#manufacturing) | — |
| P6-013 | L29:  /  production_labor_costs, production_overheads  /  Cost components and allocation references  /  | [manufacturing](#manufacturing) | — |
| P6-014 | L30:  /  quality_checks, quality_check_results  /  Inspection, disposition and release  /  | [manufacturing](#manufacturing) | — |
| P6-015 | L31:  /  batch_genealogy  /  Material-batch to output-batch traceability  /  | [manufacturing](#manufacturing) | — |
| P6-016 | L33: Reuse batches, inventory movements and journals. Distinguish raw materials, work in progress, finished goods and scrap accounts where configured. | [manufacturing](#manufacturing) | — |
| P6-017 | L37:  /  Method  /  Route  /  Behavior  /  | [manufacturing](#manufacturing) | — |
| P6-018 | L39:  /  GET/POST  /  /manufacturing/boms  /  View/create BOMs  /  | [manufacturing](#manufacturing) | — |
| P6-019 | L40:  /  POST  /  /manufacturing/boms/{id}/versions  /  Create a new recipe version  /  | [manufacturing](#manufacturing) | — |
| P6-020 | L41:  /  POST  /  /manufacturing/bom-versions/{id}/approve  /  Approve a valid BOM  /  | [manufacturing](#manufacturing) | — |
| P6-021 | L42:  /  GET/POST/PATCH  /  /manufacturing/schedules and /manufacturing/schedules/{id}  /  Configure production recurrence  /  | [manufacturing](#manufacturing) | — |
| P6-022 | L43:  /  GET/POST  /  /manufacturing/orders  /  Plan production  /  | [manufacturing](#manufacturing) | — |
| P6-023 | L44:  /  POST  /  /manufacturing/orders/{id}/release  /  Snapshot BOM and reserve required material  /  | [manufacturing](#manufacturing) | — |
| P6-024 | L45:  /  POST  /  /manufacturing/orders/{id}/consume  /  Post actual material consumption  /  | [manufacturing](#manufacturing) | — |
| P6-025 | L46:  /  POST  /  /manufacturing/orders/{id}/record-output  /  Record production quantities and batches  /  | [manufacturing](#manufacturing) | — |
| P6-026 | L47:  /  POST  /  /manufacturing/orders/{id}/quality-checks  /  Record quality/disposition  /  | [manufacturing](#manufacturing) | — |
| P6-027 | L48:  /  POST  /  /manufacturing/orders/{id}/complete  /  Finalize eligible output and costs  /  | [manufacturing](#manufacturing) | — |
| P6-028 | L49:  /  GET  /  /manufacturing/orders/{id}/costs  /  Planned/actual cost breakdown  /  | [manufacturing](#manufacturing) | — |
| P6-029 | L50:  /  GET  /  /batches/{id}/traceability  /  Upstream and downstream batch links  /  | [manufacturing](#manufacturing) | — |
| P6-030 | L51:  /  GET  /  /manufacturing/daily-summary  /  Daily production visibility  /  | [manufacturing](#manufacturing) | — |
| P6-031 | L55: Validate BOM units, positive quantities, yields and references. Block circular dependencies for assemblies and snapshot the approved BOM on released orders so later changes do not alter existing plans. | [manufacturing](#manufacturing) | — |
| P6-032 | L57: Allow documented partial consumption and partial output. Deduplicate schedule-generated orders using schedule occurrence identity; restarting a worker must not create duplicate Friday orders. | [manufacturing](#manufacturing) | — |
| P6-033 | L59: Consume the selected raw material batches at their historical inventory cost. Move material value into work in progress. Accumulate approved labor/overhead without recording the same expense twice. Use documented absorption or … | [manufacturing](#manufacturing) | — |
| P6-034 | L61: On completion, move eligible output cost from work in progress to finished inventory. Define normal waste, abnormal loss, rework and scrap treatment explicitly. Prevent division by zero, overshooting remaining planned quantitie… | [manufacturing](#manufacturing) | — |
| P6-035 | L63: Keep rejected or quarantined goods out of sellable stock until released. Record material and output links so a raw material batch can be traced to every affected finished batch and sale. | [manufacturing](#manufacturing) | — |
| P6-036 | L65: Batch profitability is based on attributable revenue, cost and recorded losses; unsold stock is not recognized as sales revenue. | [manufacturing](#manufacturing) | — |
| P6-037 | L69: Build BOM editor/version history, production calendar, daily production screen, material availability panel, manufacturing order detail, consumption form, output/batch form, labor/overhead capture, quality checklist and batch t… | [manufacturing](#manufacturing) | — |
| P6-038 | L71: Show planned versus actual quantities and costs, remaining material, accepted/rejected output, batch expiry and order status. Provide clear controlled actions for release, consume, inspect and complete. | [manufacturing](#manufacturing) | — |
| P6-039 | L75: - Releasing an order snapshots the correct BOM version. | [manufacturing](#manufacturing) | — |
| P6-040 | L76: - Production is blocked when required materials are unavailable. | [manufacturing](#manufacturing) | — |
| P6-041 | L77: - Consuming materials reduces the right raw batches and posts work-in-progress value. | [manufacturing](#manufacturing) | — |
| P6-042 | L78: - A completed batch increases eligible finished stock exactly once. | [manufacturing](#manufacturing) | — |
| P6-043 | L79: - Partial production retains remaining quantities and unfinished work-in-progress value. | [manufacturing](#manufacturing) | — |
| P6-044 | L80: - Labor/overhead allocation reconciles to source costs without duplication. | [manufacturing](#manufacturing) | — |
| P6-045 | L81: - Rejected output remains unavailable for sale. | [manufacturing](#manufacturing) | — |
| P6-046 | L82: - Traceability connects supplier receipt → raw batch → manufacturing order → finished batch → sale. | [manufacturing](#manufacturing) | — |
| P6-047 | L83: - A recurring Friday schedule generates one order per configured occurrence. | [manufacturing](#manufacturing) | — |
| P6-048 | L84: - Failed completion rolls back inventory, journal, status and batch updates. | [manufacturing](#manufacturing) | — |
| P6-049 | L85: - Concurrent or repeated completion cannot create duplicate finished batches. | [manufacturing](#manufacturing) | — |
| P6-050 | L89: Deliver connected production planning and execution, cost and quality workflows, batch genealogy, migrations and scenario evidence. Exit when material usage, finished quantities, wastage and accounting values reconcile for a re… | [manufacturing](#manufacturing) | — |

### 07_Phase_7_Reports_and_Analytics.md

42 indexed source units. [Read the complete document](erp-source/07_Phase_7_Reports_and_Analytics.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P7-001 | L5: Provide accurate business visibility through dashboards, inventory/financial/manufacturing reports and shareable PDF/Excel exports. | [reports](#reports) | — |
| P7-002 | L9: Phases 1–6 pass. Underlying operational and accounting transactions reconcile. Agree on metric definitions and date behavior before implementing charts. | [reports](#reports) | — |
| P7-003 | L13: Show total products, stock quantity/value, today's sales/purchases, cash received, credit sales, customer receivables, supplier payables, expenses, gross/net profit, production summary, low/out-of-stock items and recent transac… | [reports](#reports) | — |
| P7-004 | L15: Support daily, weekly, monthly and yearly views, date ranges and relevant warehouse/product/party filters. Label invoice-based metrics separately from cash-based metrics. Mixed units must not be added into a misleading single p… | [reports](#reports) | — |
| P7-005 | L19:  /  Family  /  Reports  /  | [reports](#reports) | — |
| P7-006 | L21:  /  Inventory  /  Current stock, stock movement, valuation, low-stock, out-of-stock, batch-wise, warehouse-wise and damaged stock  /  | [reports](#reports) | — |
| P7-007 | L22:  /  Sales  /  Daily, weekly, monthly, annual, customer-wise, product-wise, profit margin, cash sales and credit sales  /  | [reports](#reports) | — |
| P7-008 | L23:  /  Purchases  /  Supplier-wise, product-wise, returns, outstanding purchases and purchase history  /  | [reports](#reports) | — |
| P7-009 | L24:  /  Accounting  /  Customer/supplier ledger, GL, cash book, bank book, trial balance, P&L, balance sheet, cash flow, AR aging and AP aging  /  | [reports](#reports) | — |
| P7-010 | L25:  /  Manufacturing  /  Daily production, batch-wise production, manufacturing cost, material consumption, wastage, finished goods and batch profitability  /  | [reports](#reports) | — |
| P7-011 | L27: Provide applicable filters for date range, product, customer, supplier, category and warehouse. Distinguish “purchased but unpaid” from “ordered but not received” in outstanding purchase views. | [reports](#reports) | — |
| P7-012 | L31: Use posted documents, journal lines, inventory movements, batch genealogy and payment allocations as the authoritative sources. Add report_export_jobs and report_export_files for asynchronous exports. Add aggregate/materialized… | [reports](#reports) | — |
| P7-013 | L33: Historical reports must use transaction snapshots and as-of logic rather than current catalog prices or current balances. | [reports](#reports) | — |
| P7-014 | L37:  /  Method  /  Route  /  Behavior  /  | [reports](#reports) | — |
| P7-015 | L39:  /  GET  /  /dashboard/summary  /  Filtered headline metrics  /  | [reports](#reports) | — |
| P7-016 | L40:  /  GET  /  /dashboard/trends  /  Date-bucketed chart series  /  | [reports](#reports) | — |
| P7-017 | L41:  /  GET  /  /reports/inventory/{report}  /  Inventory report dataset  /  | [reports](#reports) | — |
| P7-018 | L42:  /  GET  /  /reports/sales/{report}  /  Sales report dataset  /  | [reports](#reports) | — |
| P7-019 | L43:  /  GET  /  /reports/purchases/{report}  /  Purchasing report dataset  /  | [reports](#reports) | — |
| P7-020 | L44:  /  GET  /  /reports/accounting/{report}  /  Financial report dataset  /  | [reports](#reports) | — |
| P7-021 | L45:  /  GET  /  /reports/manufacturing/{report}  /  Production report dataset  /  | [reports](#reports) | — |
| P7-022 | L46:  /  POST  /  /reports/exports  /  Request PDF or Excel with explicit filters  /  | [reports](#reports) | — |
| P7-023 | L47:  /  GET  /  /reports/exports/{id}  /  Job status and failure details  /  | [reports](#reports) | — |
| P7-024 | L48:  /  GET  /  /reports/exports/{id}/download  /  Authorized download  /  | [reports](#reports) | — |
| P7-025 | L50: Share aggregation services with Phase 5 financial statement routes so two screens cannot calculate different trial balances. | [reports](#reports) | — |
| P7-026 | L54: Specify whether each metric uses document date, posting date, settlement date or production date. Apply business timezone boundaries consistently and use half-open timestamp ranges for day/month queries. | [reports](#reports) | — |
| P7-027 | L56: Implement optimized queries with bounded pagination, suitable indexes and database aggregation. Avoid per-row database calls. Scope both report generation and downloads to the requesting user's permissions. | [reports](#reports) | — |
| P7-028 | L58: Use background export jobs for expensive output, recording requester, filters, format, generation timestamp and source cutoff. Generate small exports synchronously only when safe. Cache with business, authorization scope, date … | [reports](#reports) | — |
| P7-029 | L60: For Excel, preserve numeric financial cells and guard against formula execution in untrusted text cells. For PDF, include readable columns, page breaks, totals, units/currency and filter context. Do not silently truncate large … | [reports](#reports) | — |
| P7-030 | L64: Build a reporting center with grouped reports, saved filter state, searchable/paginated results, totals, drill-down links and export controls. Use Recharts for trends with clear axes, currency/units and loading/error states. | [reports](#reports) | — |
| P7-031 | L66: Allow users to move from dashboard totals to the supporting transactions. Show when data is stale, a report is empty or an export is still processing. | [reports](#reports) | — |
| P7-032 | L70: - Dashboard totals match the underlying transaction lists for identical filters. | [reports](#reports) | — |
| P7-033 | L71: - AR/AP aging matches the historical reference dataset. | [reports](#reports) | — |
| P7-034 | L72: - A later catalog price change leaves historical profit and inventory value unchanged. | [reports](#reports) | — |
| P7-035 | L73: - Credit sales do not appear as cash received. | [reports](#reports) | — |
| P7-036 | L74: - Inventory reports reconcile with stock movements and GL inventory value. | [reports](#reports) | — |
| P7-037 | L75: - Manufacturing reports reconcile consumption, output, wastage and finished batch costs. | [reports](#reports) | — |
| P7-038 | L76: - Month/day filters handle timezone boundaries correctly. | [reports](#reports) | — |
| P7-039 | L77: - Export totals match on-screen totals for the same source cutoff. | [reports](#reports) | — |
| P7-040 | L78: - Users cannot download another unauthorized user's export by changing an identifier. | [reports](#reports) | — |
| P7-041 | L79: - Large datasets paginate and exports finish without silent row loss. | [reports](#reports) | — |
| P7-042 | L83: Deliver the full report center, dashboard metrics, drill-downs, PDF/Excel exports, data definitions and measured query results. Exit when every required report has a real source, documented formulas and reconciliation evidence. | [reports](#reports) | — |

### 08_Phase_8_Testing_and_Optimization.md

53 indexed source units. [Read the complete document](erp-source/08_Phase_8_Testing_and_Optimization.md).

| ID | Source line and requirement/context | Workstream | Override |
|---|---|---|---|
| P8-001 | L5: Verify the complete ERP as an integrated system, improve measured bottlenecks and prepare a repeatable deployment and recovery process. | [operations](#operations) | — |
| P8-002 | L9: Phases 1–7 pass their individual checks. All required workflows use connected APIs and persisted data. Maintain a list of unresolved issues and production configuration decisions. | [operations](#operations) | — |
| P8-003 | L11: Testing also happens throughout earlier phases; this phase adds system-wide and operational verification. | [operations](#operations) | — |
| P8-004 | L15:  /  Area  /  Required evidence  /  | [operations](#operations) | — |
| P8-005 | L17:  /  Unit  /  Money/quantity rounding, costing, allocation, totals, BOM scaling and status rules  /  | [operations](#operations) | — |
| P8-006 | L18:  /  API  /  Validation, auth, permissions, filtering, pagination and error behavior  /  | [operations](#operations) | — |
| P8-007 | L19:  /  Integration  /  Inventory/accounting/document atomicity, payments, returns and production  /  | [operations](#operations) | — |
| P8-008 | L20:  /  Database  /  Constraints, migrations, idempotency, locks and concurrency  /  | [operations](#operations) | — |
| P8-009 | L21:  /  Frontend  /  Key workflows, form errors, loading/empty states and permission behavior  /  | [operations](#operations) | — |
| P8-010 | L22:  /  Reports  /  As-of totals, balance equations, subledger/GL reconciliation and exports  /  | [operations](#operations) | — |
| P8-011 | L23:  /  Operations  /  Startup, migrations, worker retries, backups, restore and monitoring  /  | [operations](#operations) | — |
| P8-012 | L24:  /  Performance  /  Representative dataset/query measurements and agreed load targets  /  | [operations](#operations) | — |
| P8-013 | L26: Use PostgreSQL for tests that depend on real locking, numeric behavior and constraints. Keep pure unit tests separate from integration tests for useful feedback. | [operations](#operations) | — |
| P8-014 | L30: 1. Configure business settings, accounts, roles, units and warehouses. | [operations](#operations) | — |
| P8-015 | L31: 2. Create products, raw materials, customers and suppliers. | [operations](#operations) | — |
| P8-016 | L32: 3. Post balanced opening stock and party balances without duplication. | [operations](#operations) | — |
| P8-017 | L33: 4. Order 100 units; receive 40 and later 60, matching invoices once. | [operations](#operations) | — |
| P8-018 | L34: 5. Post a credit sale, receive a partial payment and verify receivables. | [operations](#operations) | — |
| P8-019 | L35: 6. Complete a cash POS sale and verify revenue, cash, cost and stock. | [operations](#operations) | — |
| P8-020 | L36: 7. Post a customer return and supplier return with correct disposition. | [operations](#operations) | — |
| P8-021 | L37: 8. Transfer stock, perform a physical count and approve a variance. | [operations](#operations) | — |
| P8-022 | L38: 9. Manufacture a finished batch using material batches, labor and overhead. | [operations](#operations) | — |
| P8-023 | L39: 10. Record wastage and rejected output, then release acceptable goods. | [operations](#operations) | — |
| P8-024 | L40: 11. Reconcile cash/bank records and close a fiscal period. | [operations](#operations) | — |
| P8-025 | L41: 12. Compare stock valuation, party ledgers, trial balance, P&L, balance sheet and cash flow. | [operations](#operations) | — |
| P8-026 | L42: 13. Generate PDF/Excel reports and verify totals. | [operations](#operations) | — |
| P8-027 | L43: 14. Restore a backup into an isolated environment and repeat reconciliation. | [operations](#operations) | — |
| P8-028 | L47: - Repeat finalization, payment, return and production completion requests after simulated response loss. | [operations](#operations) | — |
| P8-029 | L48: - Reject idempotency key reuse with a different payload. | [operations](#operations) | — |
| P8-030 | L49: - Race sales against the last available stock; only permissible quantities commit. | [operations](#operations) | — |
| P8-031 | L50: - Simulate an accounting failure after stock changes are staged; the full transaction rolls back. | [operations](#operations) | — |
| P8-032 | L51: - Simulate worker retries without duplicate scheduled production, reminders or exports. | [operations](#operations) | — |
| P8-033 | L52: - Verify expired/revoked authentication and direct unauthorized object access. | [operations](#operations) | — |
| P8-034 | L53: - Reject invalid units, missing account mappings, closed-period postings and invalid batch assignments. | [operations](#operations) | — |
| P8-035 | L54: - Verify period controls cannot be bypassed through imports or backdated operational APIs. | [operations](#operations) | — |
| P8-036 | L55: - Reconcile raw materials, work in progress, finished stock and losses after partial production. | [operations](#operations) | — |
| P8-037 | L59: Use representative data volumes and agree on expected concurrency/response targets. Capture baseline measurements before adding indexes, eager loading, cache or aggregates. | [operations](#operations) | — |
| P8-038 | L61: Review query plans, N+1 access, slow reports, payload size, stock-lock duration, worker throughput and frontend rendering. Preserve audit, transaction and accounting controls while improving performance. Re-run only relevant be… | [operations](#operations) | — |
| P8-039 | L65: Review password/token handling, CORS, permissions, file upload validation, export authorization, rate limiting, secret management, dependency findings and log redaction. | [operations](#operations) | — |
| P8-040 | L67: Create environment-specific configuration, HTTPS/reverse-proxy setup as needed, database migration procedure, health checks, monitoring and alerts. Keep credentials outside source control. | [operations](#operations) | — |
| P8-041 | L69: Back up database and required attachments, document retention objectives and prove a restore. Record recovery-time/recovery-point objectives agreed with the business rather than inventing guarantees. | [operations](#operations) | — |
| P8-042 | L71: Provide a deployment runbook with preflight validation, backup, migration, application/worker startup, readiness checks, smoke tests and rollback/recovery actions. Treat data migrations as potentially non-reversible; an applica… | [operations](#operations) | — |
| P8-043 | L75: No new major business module is required. Add operational job metadata or request tracing only if justified. Existing health/readiness endpoints and permission-aware monitoring should support deployment checks. Avoid exposing i… | [operations](#operations) | — |
| P8-044 | L79: - Executable critical test suite and recorded results. | [operations](#operations) | — |
| P8-045 | L80: - Representative fixtures and reconciliation report. | [operations](#operations) | — |
| P8-046 | L81: - Resolved defect list with any accepted limitations. | [operations](#operations) | — |
| P8-047 | L82: - Performance measurements and changes justified by evidence. | [operations](#operations) | — |
| P8-048 | L83: - Clean-install and upgrade migration evidence. | [operations](#operations) | — |
| P8-049 | L84: - Docker/environment configuration and deployment runbook. | [operations](#operations) | — |
| P8-050 | L85: - Backup/restore verification and monitoring configuration. | [operations](#operations) | — |
| P8-051 | L86: - User/admin documentation for core workflows. | [operations](#operations) | — |
| P8-052 | L90: All critical business and permission checks pass. Stock, batches, receivables/payables and GL reconcile. Cash/credit behavior and historical reports remain correct. Fresh installation and upgrade work. Backup restoration is dem… | [operations](#operations) | — |
| P8-053 | L92: This documentation pack does not authorize publishing or claim that a live deployment occurred; actual implementation and release actions are separate work. | [operations](#operations) | — |

## Report acceptance and unresolved work

The exact report inventory is **8 inventory + 9 sales + 5 purchase + 11 accounting + 7 manufacturing = 40**. [Report verification](report-verification.md) defines separate totals, filters, permissions, drill-down, history and PDF/Excel cases for each report. None of those business checks has passed yet: report services and operational sources are not implemented.

See [source reconciliation](source-reconciliation.md) for concrete path/layout differences and [screen/action inventory](stage-2-screen-action-inventory.md) for every current workspace's connection state. Full operational, accounting, manufacturing, worker and recovery acceptance remains pending. Missing source documents are no longer a blocker.

Regenerate/check this index with `make traceability` / `make verify-sources`. These commands verify specification consistency only; they do not post transactions or verify report totals.
