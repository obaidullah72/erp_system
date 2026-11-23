# Authoritative sources and reconciliation

Reconciled on **2026-11-24** against the user-provided `Business_ERP_All_Phases.zip`, found at `/Users/mac/Downloads/Business_ERP_All_Phases.zip`. Its `Business_ERP_Phases/` Markdown documents are extracted into `docs/erp-source/`. All twelve extracted documents match the ZIP byte-for-byte. The ten required documents below are populated; the missing-source issue is resolved.

| Authoritative source | Role |
|---|---|
| [00_Original_Requirements.md](erp-source/00_Original_Requirements.md) | Original modules, business rules, UI and exact 40-report list in §6 |
| [00_Project_Standards.md](erp-source/00_Project_Standards.md) | Shared architecture, integrity, API and delivery standards |
| [01_Phase_1_Foundation.md](erp-source/01_Phase_1_Foundation.md) | Foundation, identity, permissions and posting kernel |
| [02_Phase_2_Master_Data.md](erp-source/02_Phase_2_Master_Data.md) | Products, units, parties and warehouses |
| [03_Phase_3_Inventory.md](erp-source/03_Phase_3_Inventory.md) | Movements, reservations, batches, valuation and controls |
| [04_Phase_4_Purchases_and_Sales.md](erp-source/04_Phase_4_Purchases_and_Sales.md) | Receipts, invoices, POS, payments and returns |
| [05_Phase_5_Accounting.md](erp-source/05_Phase_5_Accounting.md) | Accounts, ledgers, statements, periods and reconciliation |
| [06_Phase_6_Manufacturing.md](erp-source/06_Phase_6_Manufacturing.md) | BOMs, schedules, consumption/output, quality and genealogy |
| [07_Phase_7_Reports_and_Analytics.md](erp-source/07_Phase_7_Reports_and_Analytics.md) | All 40 reports, dashboard, filters, history and PDF/Excel exports |
| [08_Phase_8_Testing_and_Optimization.md](erp-source/08_Phase_8_Testing_and_Optimization.md) | End-to-end reconciliation, security, performance, operations and recovery |

`00_README.md` and `Business_ERP_All_Phases.md` are retained as supporting documents. The combined file duplicates the standards/phases and is not counted as extra feature coverage. [manifest.json](erp-source/manifest.json) records every archive member, length and SHA-256, plus the archive checksum. The originals are preserved unchanged; implementation decisions and overrides live outside the source files.

## Authority and confirmed overrides

Use the latest explicit user instructions, then these populated sources. Earlier empty files under `docs/phases/` are legacy placeholders, not specifications. The existing Stage 1 completion note remains historical evidence, not a substitute for source acceptance. The source pack's Phases 1–8 describe business dependencies; the user's delivery Stages 2–5 mean frontend, backend, integration and comprehensive verification. These are different numbering systems.

**OVR-ROLES-01** supersedes the older suggested role names in original §7, source Phase 1, and the combined source copy:

1. Super Admin
2. Admin
3. Accountant
4. Sales Manager
5. Purchase Manager
6. Inventory Manager
7. Production Manager
8. Cashier
9. Viewer

Super Admin has full access, including user and role management. Admin excludes restricted Super Admin controls. Viewer is read-only. Other responsibility roles have configurable module/action grants. Read-only acceptance checks referring to the older role name apply to Viewer. Backend `ROLE_GRANTS`, database `seed_roles`, frontend role names and current security documentation already use this list. Original source quotations retain old names solely for provenance; they must not seed runtime roles.

The existing root `frontend/` and `backend/` structure is retained during reconciliation. Source standards request `business-erp/frontend` and `business-erp/backend`. This **layout deviation remains explicit**, rather than falsely claiming literal path compliance or creating a second application. Responsibilities are documented in `architecture.md` and `folder-structure.md`.

## Contract differences

Source phase routes are proposed `/api/v1` contracts; they do not authorize a claim that handlers exist. Prefer their namespace when implementing new modules. Existing foundation routes retain their working contract. The earlier Stage 1 planned-path table and nonreport UI metadata have unresolved differences listed here; do not connect them until DTOs, states, authorization and tests are implemented.

| Area | Earlier baseline / current UI metadata | Populated source contract / resolution |
|---|---|---|
| Business settings | `/business-settings` implemented | Source proposes `/settings/business`; retain implemented path and document alias decision if needed |
| User/role detail | No GET item handler; UI reads supported lists | Source proposes GET item; explicit gap, not a fictitious endpoint |
| Dashboard | UI shows unavailable metrics | `/dashboard/summary` and `/dashboard/trends` still unimplemented |
| Catalog | Manufacturers missing specific contract | `/manufacturers` now has a source proposal; product history/images/barcode have explicit source routes; DTOs/handlers pending |
| Parties | `/partners` in early domain design | Source `/parties/{id}/summary`, opening-balance drafts and shared identity; settle naming before migration/API registration |
| Inventory | Several missing paths and early dispatch/receive transfer actions | Source `/inventory/openings`, `/inventory/adjustments`, `/inventory/counts`, `/inventory/valuation`, `/inventory/alerts`; transfer baseline is atomic `/inventory/transfers/{id}/post`. A dispatched/transit workflow needs explicit transit stock and is not supplied by the source baseline |
| Purchases | `/purchase-orders`, `/goods-receipts`, `/supplier-invoices` | `/purchases/orders`, `/purchases/receipts`, `/purchases/invoices`; matching/clearing required; none implemented |
| Sales/POS | `/sales-invoices`, `/pos/sales` | `/sales/invoices`, `/sales/checkout`, invoice print/reverse; none implemented |
| Returns | Shared `/returns` proposal | `/sales/returns` and `/purchases/returns`, linked to original costs and taxes |
| Accounting | `/accounts`, `/journal-entries`, `/general-ledger`, `/financial-statements/*` | Source `/accounting/accounts`, `/accounting/journals`, `/accounting/general-ledger`, `/accounting/statements/{type}`; source period/reconciliation/transfer routes require services beyond the internal posting kernel |
| Party ledgers | `/customer-ledgers/{partner_id}`, `/supplier-ledgers/{partner_id}` | `/customers/{id}/ledger`, `/suppliers/{id}/ledger`; actual projections pending |
| Manufacturing | `/boms`, `/work-orders`, `/material-issues`, `/production-completions` | `/manufacturing/boms`, `/manufacturing/orders/{id}/release`, `/consume`, `/record-output`, `/quality-checks`, `/complete`; schedule and BOM-version routes in Phase 6 |
| Genealogy | `/batches/{id}/genealogy` | Source `/batches/{id}/traceability`; source identity must span receipt through sale |
| Reports | Generic `/reports` namespace, 40 routes previously marked contract gaps | Each report now maps to source `/reports/{family}/{report}` with a specific slug in `report-catalog.json`; metadata status is **planned**, not connected |
| Export jobs | `/exports` early proposal | `/reports/exports`, `/{id}`, `/{id}/download`; no job/table/worker implementation exists yet |

Methods/payloads for commands not specified in the source remain design work. No source text or UI definition should be promoted into OpenAPI until an authorized handler and meaningful response model exist. `docs/openapi.json` remains the implemented contract snapshot.

## Report baseline

| Family | Required reports |
|---|---:|
| Inventory | 8 |
| Sales | 9 |
| Purchases | 5 |
| Accounting | 11 |
| Manufacturing | 7 |
| **Total** | **40** |

The [catalog](report-catalog.json) preserves the exact source order, source line, stable R01 ID, screen, planned API, applicable filters, columns, read/export permissions and PDF/XLSX formats. [Report verification](report-verification.md) adds explicit formulas and independent fixture expectations. The formula choices are an implementation baseline, not proof of approval or runtime correctness. Each report has six individually identified cases: totals, filters, permissions, drill-downs, historical accuracy, and PDF/Excel fidelity. All 240 are **not run**, because the required business/report services are missing. API path consistency and UI filter tests do not verify financial correctness.

## Verification and coverage rules

`make verify-sources` checks checksums, the ten-file authority set, the complete source-unit index, 40 names/order/counts, proposed paths versus OpenAPI, 240 case IDs and exact frontend/backend roles. For repeatable ZIP comparison:

```sh
python3 scripts/source_traceability.py --archive /path/to/Business_ERP_All_Phases.zip
```

`make traceability` regenerates the source index and workspace inventory after review. It does not mark tests passed. Source paragraphs, bullets, table rows and examples are indexed individually; compound paragraphs may require multiple executable cases. The map identifies current code or planned ownership, database objects and evidence gaps. Broad workstream mappings must be refined with actual executable evidence before claiming each source requirement complete.

The prior foundation check results are retained in `docs/testing.md` and the Stage 1 record. They are not rerun by source verification and do not certify later modules. Current full-ERP readiness remains unverified: business services/migrations, report calculations/exports, transaction reconciliation, comprehensive browser flows, full-data restore and operational load evidence are outstanding. These are implementation gaps, not missing-source blockers.

## Checks executed for this reconciliation

| Check | Observed result on 2026-11-24 |
|---|---|
| Source verifier with original ZIP | Passed: 12 byte-identical extracted documents; 10 authoritative sources; 973 indexed source units; 40 exact reports; 240 planned case IDs; nine matching backend/frontend roles |
| `make verify-sources` | Passed; generated source map and screen/action inventory match the inputs |
| `npm run test --prefix frontend` | 14 tests passed in 3 files, including report-specific filter reset and honest unavailable-service behavior |
| `npm run lint --prefix frontend` | Passed |
| `npm run build --prefix frontend` | Passed; existing main bundle exceeds the 500 kB warning threshold; no performance acceptance claim |
| `git diff --check` | Passed |
| Business report reconciliation / report API authorization / historical totals / PDF and Excel artifacts | **Not run**; corresponding business services and exports are not implemented |

The source-consistency checks do not execute PostgreSQL or browser workflows. Prior foundation integration results remain historical evidence. This update resolves specification provenance and report enumeration; it does not mark delivery Stages 2–5 complete.
