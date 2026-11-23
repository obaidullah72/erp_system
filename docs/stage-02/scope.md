# Stage 2 scope inventory — baseline before module implementation

Source: user-supplied Stage 2 brief, sections 1–10, and docs/api.md/domain-model.md. No AGENTS.md or additional shared instruction file exists in this checkout. Source Phase 3–7 files are empty; Phase 7 is titled Manufacturing and contains no report list. Original source-phase parity and the exact report catalogue remain unresolved specification gaps. Requested source text is pending; do not claim full Stage 2 completion without reconciling it.

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
| H Reports | Individual named inventory/sales/purchase/accounting/manufacturing reports derived from explicit brief; original Phase 7 list pending | Filters/period/currency/units; results/totals/pagination; source drill-down; PDF/Excel export progress/failure/download/unavailable |
| I Administration | Settings; users; roles/grants; mappings; audit; reminders; alerts | Connected foundation list/create/update; protected controls; future mapping/configuration actions visibly unavailable |

## Implementation boundaries

Existing health/auth/user/role/business-settings endpoints are connected using their actual DTOs. All operational module endpoints are planned, not implemented. A resource with an existing Stage 1 baseline maps to that contract. Missing endpoint/method/DTO definitions are marked contract gaps; no guessed request is sent. Local draft review checks input only and explicitly does not save, post, settle or export. Existing-record edits require a real loaded record. No runtime fixture or fallback business data.

Shared components: labeled fields and errors; searchable multi-select; dates; decimal-preserving values; line editors; tables with URL filters/sort/pagination; dialogs/drawers with focus management; status badges; charts/metrics; attachment preview; notifications; print previews; all loading/empty/unavailable/denied/error states. Forms use RHF/Zod, submission locks, backend field mapping and unsaved-change protection.

Detailed route/action/permission/contract traceability will be generated from the same resource catalogue used by the frontend and verified against route tests. The original source-phase gap remains distinct from pending backend connections.
