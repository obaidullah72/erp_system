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
