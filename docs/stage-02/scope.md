# Stage 2 scope inventory — baseline before module implementation

Source: user-supplied Stage 2 and Stages 2–5 briefs, plus the ten populated documents extracted from `Business_ERP_All_Phases.zip` into [docs/erp-source](../erp-source/00_README.md). This includes the original requirements, shared standards and source Phases 1–8. The old empty files under `docs/phases` are not requirements sources. Source availability is resolved; implementation and verification remain separate. See [source reconciliation](../source-reconciliation.md) and [requirements traceability](../requirements-traceability.md).

## Screen/action families

| Brief | Screen inventory | Action inventory |
|---|---|---|
| A Dashboard | Inventory value/product counts; physical stock by unit; sales/purchases; received/paid cash; credit sales; AR/AP; expenses; gross/net profit; production; low/out-of-stock alerts; recent transactions/trends | Date filtering, drill-downs, refresh; all aggregates pending |
| B Master data | Products; categories/subcategories; units/conversions; brands/manufacturers; warehouses; customers/suppliers/vendors; employees/contacts; opening balance drafts | List/detail/new/edit/archive; images/attachments; barcode/QR and print; histories; terms/credit limits |
| C Inventory | Balances; opening stock; movements; adjustments; damaged stock; reservations; transfers; counts; reconciliation; valuation; lots/batches/expiry; alerts | Prepare/approve/post/reverse; reserve/release; dispatch/receive; variance review; source drill-down |
| D Purchases | Orders; goods receipts; supplier invoices; invoice matching; settlements; purchase returns | Approval; partial/full receipt separately from invoice; charges/discounts/taxes; payments; supplier history |
| E Sales | Orders/shipments; invoices; pricing; POS; stock/batch eligibility; returns/refunds | Barcode search; credit check; partial/full payment; reversal; print; customer/product history |
| F Accounting | Chart/tree; journals; GL/day/cash/bank books; AR/AP; partner ledgers; aging; advances/allocations; expenses; transfers; cash closing; bank imports/reconciliation; periods; TB/P&L/BS/cash flow | Draft/post/reverse; allocation; reconcile; import; close/reopen; print/export, server-owned totals |
| G Manufacturing | BOM/version history; schedule/calendar; orders; material availability; consumption; partial output; finished batches; labor/overhead; waste/rejected/rework; quality; planned/actual costs; traceability | Approve BOM; release order; consume; record output; quality release; cost review and genealogy drill-down |
| H Reports | Exactly 40 reports from original §6 and source Phase 7: 8 inventory, 9 sales, 5 purchase, 11 accounting, 7 manufacturing | Applicable date/product/customer/supplier/category/warehouse filters; units/currency; totals/pagination; source drill-down; PDF/Excel export progress/failure/download/unavailable |
| I Administration | Settings; users; roles/grants; mappings; audit; reminders; alerts | Connected foundation list/create/update; protected controls; future mapping/configuration actions visibly unavailable |

## Implementation boundaries

Existing health/auth/user/role/business-settings endpoints are connected using their actual DTOs. All operational module endpoints are planned, not implemented. A resource with an existing Stage 1 baseline maps to that contract. Missing endpoint/method/DTO definitions are marked contract gaps; no guessed request is sent. Local draft review checks input only and explicitly does not save, post, settle or export. Existing-record edits require a real loaded record. No runtime fixture or fallback business data.

Shared components: labeled fields and errors; searchable multi-select; dates; decimal-preserving values; line editors; tables with URL filters/sort/pagination; dialogs/drawers with focus management; status badges; charts/metrics; attachment preview; notifications; print previews; all loading/empty/unavailable/denied/error states. Forms use RHF/Zod, submission locks, backend field mapping and unsaved-change protection.

The [screen/action inventory](../stage-2-screen-action-inventory.md) is generated from the frontend resource catalog. [Report definitions and verification](../report-verification.md) records report-specific expected results and six planned checks per report. These inventories do not establish runtime correctness. The exact nine roles confirmed by the user supersede older suggested names in the source pack; the original files remain unchanged for provenance.
