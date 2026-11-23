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
