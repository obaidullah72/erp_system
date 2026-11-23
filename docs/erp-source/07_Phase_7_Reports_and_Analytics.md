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
