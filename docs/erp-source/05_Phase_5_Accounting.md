# Phase 5 — Accounting

## Goal

Expand the existing posting kernel into a full double-entry accounting workspace with receivables, payables, payments, expenses, reconciliations and financial statements.

## Prerequisites

Phases 1–4 pass, including balanced postings from inventory, purchasing and sales. Review and reconcile existing opening inventory, receipt clearing, receivables and payables before exposing financial statements.

## Functional scope

Implement Chart of Accounts, General Ledger, Cash Book, Bank Book, journals, cash receipts/payments, AR/AP, income/expenses, Day Book, trial balance, profit and loss, balance sheet, cash flow, opening/closing balances, partial settlements, advances and controlled adjustments.

Support multiple cash/bank accounts, deposits, withdrawals, bank transfers, daily cash closing, cash reconciliation and bank reconciliation.

Support expense categories such as rent, electricity, salaries, transportation, fuel, maintenance, manufacturing, packaging and miscellaneous expenses. Attach receipts, dates, categories and payment method.

Support due dates, aging, customer/supplier statements and payment reminders. Reminders are authorized business notifications; configure recipients, templates and delivery channels before enabling external sending.

## Database tables

| Tables | Responsibility |
| --- | --- |
| accounts, account_mappings, fiscal_periods | Account hierarchy, event mappings and period controls |
| journal_entries, journal_entry_lines | Authoritative balanced postings |
| cash_bank_accounts | Cash/bank identity linked to GL accounts |
| payments, payment_allocations | Settlements, advances and allocations |
| expense_categories, expenses, expense_attachments | Expense capture and supporting receipts |
| bank_statement_imports, bank_statement_lines | Imported statement data and deduplication |
| reconciliation_sessions, reconciliation_matches | Cash/bank comparison and matching |
| cash_closings | Expected, counted and variance records |
| reminder_rules, reminder_deliveries | Authorized reminder history |

Prefer ledger views derived from journal lines and party links. If materialized subledger tables exist, reconcile them to the GL and prevent uncontrolled edits.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET/POST/PATCH | /accounting/accounts and /accounting/accounts/{id} | Chart of Accounts |
| GET/POST | /accounting/journals | Search/create draft journals |
| POST | /accounting/journals/{id}/post | Validate and post |
| POST | /accounting/journals/{id}/reverse | Linked reversal |
| GET | /accounting/general-ledger | Account/date ledger |
| GET | /customers/{id}/ledger and /suppliers/{id}/ledger | Party ledgers |
| GET | /accounting/receivables and /accounting/payables | Outstanding invoices and aging |
| GET/POST | /expenses | View/create expenses |
| POST | /expenses/{id}/post | Post expense and payment/payable effect |
| POST | /accounting/transfers | Transfer between cash/bank accounts |
| GET/POST | /accounting/reconciliations | Create/review reconciliation |
| POST | /accounting/reconciliations/{id}/finalize | Close approved reconciliation |
| POST | /accounting/cash-closings | Record daily count and approved variance |
| GET | /accounting/statements/{type} | Trial balance, P&L, balance sheet or cash flow |
| POST | /accounting/periods/{id}/close | Close a reconciled period |
| POST | /accounting/periods/{id}/reopen | Privileged, audited reopening |

## Backend work

Implement account types, posting restrictions, mapping validation and period locks. Require every journal to balance at currency precision, with exactly one debit/credit direction per line and valid posting accounts.

A transfer debits the receiving cash/bank account and credits the sending account; it does not create income. Allocate receipts/payments without exceeding available amounts. Keep advances visible as unapplied balances until correctly allocated.

Stage opening balances, validate total debits equal credits and post them once. Distinguish prior opening balances from ordinary revenue. Do not duplicate stock, customer or supplier openings entered in earlier phases.

Produce statements from posted data with a documented account mapping. Balance sheet assets must reconcile to liabilities plus equity, including current earnings. Derive cash flow from cash movements with configured classification; profit is not a substitute for cash flow.

Use as-of dates for aging and statements, including reversals/allocations effective by that date. Protect finalized documents and closed periods. Audit journal posting, mappings, opening balances, reconciliation and period changes.

## Frontend work

Build accounting navigation, account tree, journal editor, cash/bank books, party ledgers, outstanding invoice views, allocation dialogs, expense forms, reconciliation matching and statement screens.

Show debits/credits, opening/running/closing balances and statement filters clearly. Display unpaid invoices separately from cash movements. Show unallocated advances and block incomplete journals before submission, with server validation as final authority.

## Acceptance checks

- Unbalanced journals fail and leave no committed lines.
- Credit sales/purchases affect AR/AP without falsely changing cash.
- A partial payment reduces the correct invoice balance once.
- A cash-to-bank transfer preserves total liquid assets and creates no income.
- Aged balances match an as-of-date fixture even after later payments.
- Party subledgers reconcile to control accounts.
- Trial balance debits equal credits; the balance sheet equation holds.
- Repeated opening balance or payment requests do not duplicate postings.
- Bank statement duplicates cannot be imported twice without explicit handling.
- Closed-period backdating and unauthorized reopening fail.

## Deliverables and exit criteria

Deliver a connected accounting workspace, documented posting/account mappings, reconciliations, financial statements and integrity verification. Exit only when operational subledgers, inventory valuation and the GL reconcile for the agreed reference dataset.
