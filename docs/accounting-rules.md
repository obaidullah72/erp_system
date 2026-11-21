# Accounting rules

Stage 1 implements the internal double-entry kernel with exact decimal inputs, same-business active account mappings, base-currency validation, source uniqueness, idempotency and caller-owned transactions. PostgreSQL enforces one positive side per line, deferred aggregate balance and immutable journal history. At least two lines are required; no partial successful posting survives a failed command. See `app/modules/accounting/posting.py` and migration 0002.

The initial kernel accepts two-decimal base-currency amounts only. FX, other minor-unit scales, tax rounding, periods, chart management and reversal workflows remain future accounting extensions. The explicit default `OpenPeriodPolicy` must be replaced by a locking period policy when fiscal periods arrive; no closed-period protection is claimed today.

Future source commands must atomically commit source state, stock/cost movements, journals, allocations, audit and idempotency. Corrections use linked reversals, never edits/deletes of posted facts. Customer/supplier/general ledgers and statements derive from journals and allocations, never independent editable balances. No public journal-posting endpoint is exposed in Stage 1.
