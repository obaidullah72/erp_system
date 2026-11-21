# Database implementation and domain blueprint

The complete cross-module blueprint is [domain-model.md](domain-model.md). This file records what is migrated today.

`0001_foundation` preserves the original empty baseline. `0002_foundation_tables` creates businesses, business_settings, users, roles, permissions, user_roles, role_permissions, auth_sessions, audit_logs, document_sequences, idempotency_records, accounts, journal_entries and journal_entry_lines. This is 15 tables, plus Alembic's version table. Later business tables must arrive in incremental revisions.

The migration contains frozen PostgreSQL DDL independent of mutable ORM definitions. It installs immutable journal/audit triggers, a same-transaction line insertion guard, and deferred aggregate journal balance checks. A journal's internal `transaction_id` records the creating PostgreSQL transaction so a later transaction cannot append lines. The runtime database role must not own/disable triggers; production DDL uses a separate migration role.

Composite `(business_id,id)` keys and composite foreign keys prevent cross-business membership, session, actor, journal and account references. Source uniqueness is `(business_id,source_type,source_id,event)`; idempotency uniqueness is `(business_id,operation,key)`. Email is lowercased and unique within a business. Financial money uses NUMERIC(20,6), with exact two-decimal base-currency posting enforced by the Stage 1 event contract.

Role and permission rows are seeded by the controlled bootstrap in the same transaction as the first business/user. This keeps migrations free of production identity values. Reusable `seed_roles` inserts missing catalogue and roles without overwriting configured grants. No accounts, balances or journals are fabricated by bootstrap.

Run `make migrate`, then `cd backend && venv/bin/python -m alembic current`. The test suite applies both migrations in a fresh schema per test. Never run ORM `create_all` in application startup. Downgrade destroys the foundation tables; use only on disposable databases. Operational rollback normally restores a tested backup or uses a forward repair migration.
