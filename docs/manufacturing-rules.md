# Manufacturing rules (future implementation contract)

Freeze the BOM revision on a released work order. Record material issue lots, quantities and actual costs against production batches. Track raw material → WIP → finished goods, with explicit labor/overhead allocation, scrap, rework and variance. Completion and related stock/cost/journal postings commit together.

Record parent/child lot genealogy, split/merge and partial consumption; reject lineage cycles. Supplier receipts, quality inspections/quarantine releases, production lots, serials, shipments and returns must remain traceable in both directions. Quality quarantine blocks saleable stock. Electrical meter serial identities are separate from lot identities. None of these workflows is implemented in Phase 1.
