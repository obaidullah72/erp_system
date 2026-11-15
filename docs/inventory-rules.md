# Inventory rules (future implementation contract)

Stock movements are append-only. Balance projections update atomically under locks. Reservations reduce availability without changing on-hand or value. Reject negative stock initially; keep quarantine distinct from saleable stock. A transfer has equal/opposite quantity legs and preserves cost.

Initial proposed policy is perpetual moving weighted average per product/warehouse. Use Decimal/NUMERIC, not float; clear residual carrying value on depletion. Returns reference original movement cost. Landed-cost changes and corrections are additional linked postings. No rewriting closed-period valuations. Count adjustments require reason, permission, and accounting linkage. See architecture and database blueprint for posting/concurrency boundaries. None of these business rules is implemented in Phase 1.
