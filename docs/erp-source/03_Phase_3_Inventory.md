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
