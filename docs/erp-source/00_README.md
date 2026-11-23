# Business ERP — Complete Phased Development Pack

Prepared: 20 November 2026  
Project context: OB ST  
Basis: the supplied “Complete Business Management, Inventory, Accounting & Manufacturing ERP System” specification.

## Purpose

This pack translates the supplied specification into eight implementation guides, preserving its phase names and order. These are development instructions and acceptance criteria; they do not claim that application code, migrations, tests, or deployment have already been completed.

The ERP covers motorcycle spare parts, electrical meters, accessories, general trading, wholesale and retail, and daily or scheduled batch manufacturing.

## Files and order

| Order | Guide | Result |
| --- | --- | --- |
| 1 | 01_Phase_1_Foundation.md | Running platform, authentication, permissions, schema foundation and dashboard shell |
| 2 | 02_Phase_2_Master_Data.md | Products, units, categories, brands, parties and warehouses |
| 3 | 03_Phase_3_Inventory.md | Traceable inventory movements, transfers, valuation and alerts |
| 4 | 04_Phase_4_Purchases_and_Sales.md | Receiving, billing, POS, payments, returns and transactional postings |
| 5 | 05_Phase_5_Accounting.md | Full accounting workflows, ledgers, reconciliations and financial statements |
| 6 | 06_Phase_6_Manufacturing.md | BOMs, planning, batches, production costing and quality control |
| 7 | 07_Phase_7_Reports_and_Analytics.md | Business dashboard, report center and PDF/Excel exports |
| 8 | 08_Phase_8_Testing_and_Optimization.md | System verification, optimization, recovery checks and deployment readiness |

Start with 00_Project_Standards.md. The original specification is included as 00_Original_Requirements.md. Business_ERP_All_Phases.md combines the standards and all eight guides for convenient sharing.

## Important dependency

Phase 4 requires working accounting postings even though the full accounting user interface is scheduled for Phase 5. Phase 1 therefore defines the posting contract and minimal journal infrastructure. Phase 3 adds the postings required for opening stock and adjustments. Phase 4 implements balanced purchase, sale, settlement and return postings as part of those transactions. Phase 5 expands this into complete accounting operations and statements. No finalized transaction may temporarily bypass the accounting rules.

Batch identification and optional expiry fields begin with inventory in Phase 3; Phase 6 adds manufacturing-specific batch creation and traceability. This allows purchased batches and FEFO allocation to work before manufacturing.

## Working process

Implement one phase at a time. For each phase, inspect the existing repository, review the relevant original requirements, design or update migrations, implement services and APIs, connect real frontend workflows, execute the listed acceptance checks, and record evidence. Proceed only when the phase exit criteria pass.

A phase completion note must identify delivered features, changed tables and migrations, documented API routes, verification results, screenshots or workflow evidence where useful, and remaining blockers. Never describe mock data or disconnected buttons as completed business functionality.

## Scope assumptions

- Begin with one business and multiple warehouses; retain explicit business ownership in domain records. Multi-company consolidation is a separate future requirement.
- Use a configurable base currency, timezone, fiscal year and tax configuration. Do not assume a currency or current tax rate.
- Start with a selected inventory valuation policy and keep it distinct from FIFO/FEFO physical batch allocation.
- Support employees as user/contact records and salary expenses where required. Payroll, HR attendance and statutory payroll calculations are not specified.
- Confirm jurisdiction-specific financial and tax reporting requirements before production configuration.
- No calendar delivery estimates are invented. The exit criteria determine readiness.
