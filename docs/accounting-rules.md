# Accounting rules (future implementation contract)

Use double-entry base-currency journals, decimal strings over APIs, Python Decimal and PostgreSQL NUMERIC. Posted entries must balance before commit and have exactly one positive debit or credit per line. Currency rounding is explicit per currency/document policy. Keep original currency, FX rate and base amount.

One business transaction includes source state, stock/cost changes, journal, allocations, audit and idempotency result. Journals and posted lines cannot be edited or deleted; use linked reversals and corrected documents. Locked periods reject new backdated postings. Customer/supplier ledgers derive from journals and allocations, never editable running balances. Service and database protections arrive in Phase 6. Phase 1 has no financial posting implementation.
