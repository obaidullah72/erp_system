# Report definitions and verification baseline

The exact 40 reports come from original requirements §6 and source Phase 7. The user-confirmed list resolves the earlier source gap. These are **planned definitions and acceptance cases**, not implemented query results. No report totals, report permissions, drill-downs, historical behavior or exports have been verified yet. The accounting/valuation treatment must be implemented and reconciled before these cases can pass.

## Contracts and authorization

Each report has its own proposed GET `/api/v1/reports/{family}/{report}`; the existing screen URL stays stable. All 40 are absent from implemented OpenAPI. Proposed exports: POST `/api/v1/reports/exports`, GET `/api/v1/reports/exports/{id}`, GET `/api/v1/reports/exports/{id}/download`. A successful response must come from a persisted job/artifact. Both PDF and XLSX are required for every report.

Read requires `reports:read`; export additionally requires `reports:export`. Scope every query/job/cache/file to business and live authorization. Validate source-detail permission on drill-downs; a report grant alone does not authorize unrelated detail APIs. Recheck authorization before job execution/status/download, including after grant revocation. Viewer stays read-only; the role name does not bypass permission checks. Domain-specific report grants remain a design decision before connection; `domain_scope` identifies the responsible module, not an implemented extra grant.

## Shared dates, filters and historical rules

Use inclusive business dates for document/posting dates; convert timestamp intervals to business-local half-open `[start, next-day)` ranges. Distinguish document date (sales/purchases), posting/effective date (GL/valuation/settlements), production date and recorded timestamp. Opening balances precede the selected start; closing/as-of balances include effective events through the end. A source cutoff additionally limits recorded events so UI and export can reproduce the same snapshot even when a backdated entry is added later. A cutoff timestamp alone is not a proven snapshot under concurrent commits; implementation must use a durable snapshot/watermark or equivalent tested mechanism.

Proposed week buckets start Monday; annual sales use calendar year; configurable fiscal-year statements must be separately labeled. These are implementation baseline choices, not quoted source mandates. Include base currency and unit on every relevant amount/quantity. Do not add incompatible physical units. Define rounding centrally with Decimal; never calculate financial totals from client floats.

The registry lists relevant date/as-of, product, customer, supplier, category, warehouse and additional account/batch filters for each report. Apply every supported filter before aggregation, count and pagination. Product/category/location filters do not apply to every journal-level statement; reject unsupported dimensions rather than invent an allocation or silently ignore them. Preserve filters in drill-down and export requests. Empty datasets use genuine zero/no-data results only after a successful authorized query.

## Independent fixtures

These fixture specifications are not seeded runtime/demo data and have not executed. Use separate isolated scenarios; do not add their balances together. Tax/discount, quality, partial production and cutoff variants supplement the arithmetic baselines. Expected values are calculated explicitly here rather than copied from production aggregation code.

### INV fixture

Isolated stock fixture: Bolt (ea), warehouses A/B; opening 100 at 10.00, receipt 20 at 10.00, issue 10, resalable return 2 at original 10.00, written-off damage 3, transfer 5 A→B. No reservation in baseline. Opening batch ends 89; receipt batch 20. Separate Zero product, low-stock threshold 150, and kg product prevent unit-mixing. Add held/reserved/expired variants before acceptance.

### SALE fixture

Isolated sales fixture: customer A, one product costing 10.00/ea; credit invoice 10 at 20.00 (200.00), credit receipt 40.00, cash invoice 5 at 20.00 (100.00) with receipt 100.00, resalable credit return 2 at 20.00 (40.00) costing 20.00. No tax/discount in arithmetic baseline; add configured tax/discount variants. Event date 2026-01-31 in Asia/Karachi; out-of-range control sale at 2026-01-31T19:00:00Z is February locally.

### BUY fixture

Isolated purchase fixture: order 100 ea; receipt 20 at 10.00; matched supplier invoice 200.00 (must not receive twice); return 2 at original 10.00 with debit note 20.00; payment 80.00. Remaining unreceived 80 ea, AP 100.00. No tax/charges in baseline; add snapshotted tax/landed-cost variants.

### ACC fixture

Independent accounting fixture: opening inventory/equity 1000.00; purchase invoice/receipt 200.00; purchase return 20.00; supplier payment 80.00; credit sales 200.00; cash sales 100.00; customer credit return 40.00 (cost 20.00); sales COGS before return 150.00; credit receipt 40.00; cash-sale receipt 100.00; cash expense 20.00. Ending inventory 1050.00, cash 40.00, AR 120.00, AP 100.00, net revenue 260.00, COGS 130.00, expense 20.00, equity 1000.00. Due Jan 15, as-of Jan 31. February receipts/payments 50.00/30.00 must not change January aging.

### MFG fixture

Isolated manufacturing fixture: consumed 20 kg at 5.00 (100.00), including 2 kg normal process waste; labor 20.00, overhead 30.00; output 10 accepted ea at 15.00. Sell 4 at 25.00 (revenue 100.00, cost 60.00), write off 1 finished ea (15.00), remaining 5 at 15.00 (75.00). WIP clears on completion; later sale/damage do not rewrite produced quantity or cost. Add partial output, quarantine/rejection and zero-yield variants.

## Forty reports

| Requirement | Family / report | Planned formula | Independent baseline expectation |
|---|---|---|---|
| R01.01 | Inventory — Current stock | Sum signed posted base quantities by product/unit/location through cutoff; show reserved and eligible available separately. | Bolt 109 ea; Warehouse A 104, B 5; never sum ea and kg. |
| R01.02 | Inventory — Stock movement | List immutable movement lines, opening + signed movements = closing; internal transfer signs cancel business-wide. | Opening 100 + receipt 20 - sale 10 + return 2 - damage 3 = 109 ea; transfer -5/+5 nets zero. |
| R01.03 | Inventory — Stock valuation | Sum historical remaining costs at cutoff; do not multiply by current master price. | 109 ea at recorded 10.00 = 1090.00; changing reference price to 99.00 has no effect. |
| R01.04 | Inventory — Low-stock | Compare eligible available quantity with configured threshold in the same product base unit. | Bolt available 109 < threshold 150 is included; a product above threshold is excluded. |
| R01.05 | Inventory — Out-of-stock | Select active stock products with eligible available quantity <= 0; distinguish zero on-hand from reserved/unusable stock. | Zero product has 0 available and is included; Bolt is excluded. |
| R01.06 | Inventory — Batch-wise stock | Aggregate dated movements per batch/product/location with eligibility and expiry. | Opening batch 89 ea, receipt batch 20 ea; total 109; transfers preserve batch identity. |
| R01.07 | Inventory — Warehouse-wise stock | Aggregate movements per warehouse/product/base unit; reconcile location totals to business total. | A 104 ea + B 5 ea = 109 ea; values 1040.00 + 50.00 = 1090.00. |
| R01.08 | Inventory — Damaged stock | Show damage events and disposition by batch/location; distinguish written-off quantities from quarantined holdings. | Written-off damage 3 ea / 30.00, source-linked; not counted as sellable stock. |
| R01.09 | Sales — Daily sales | Bucket net posted sales by business-local document day; subtract effective returns; cash receipts are separate. | Selected local day gross 300.00, returns 40.00, net 260.00; receipts 140.00. |
| R01.10 | Sales — Weekly sales | Aggregate net sales into business-local Monday-start weeks (proposed baseline); include only selected date range. | Selected week net 260.00; all source rows reconcile to daily totals. |
| R01.11 | Sales — Monthly sales | Bucket net sales by business-local calendar month; exclude next-month boundary fixture. | January net 260.00; February boundary sale 50.00 is excluded. |
| R01.12 | Sales — Annual sales | Bucket net sales by business-local calendar year; fiscal-year reporting must be separately labeled. | Selected calendar-year/range net 260.00 for the baseline rows; exclude out-of-range controls. |
| R01.13 | Sales — Customer-wise sales | Group snapshotted net sales by customer identity, keeping anonymous POS sales explicit. | Customer A gross 300.00 minus returns 40.00 = 260.00. |
| R01.14 | Sales — Product-wise sales | Group net quantities/revenue by snapshotted product/base unit; preserve historical prices and costs. | Product sale 15 ea minus return 2 = 13 ea; net 260.00; COGS 130.00. |
| R01.15 | Sales — Profit margin | Net sales excluding tax minus attributable recorded COGS; margin = profit / net sales; zero denominator returns null. | Revenue 260.00 - COGS 130.00 = gross profit 130.00; margin 50.00%. |
| R01.16 | Sales — Credit sales | Filter invoice payment terms, not current settlement status; show invoice amounts, effective returns and outstanding separately. | Credit net sales 160.00; payment 40.00; remaining AR 120.00. Not cash received 160.00. |
| R01.17 | Sales — Cash sales | Filter fully settled cash-sale classification; keep later receipts against credit invoices separate. | Cash-sale revenue/receipt 100.00; credit-customer payment 40.00 is not another cash sale. |
| R01.18 | Purchases — Supplier-wise purchases | Group posted supplier invoice amounts net of effective purchase returns; receiving is a separate quantity event. | Supplier A invoice 200.00 - return 20.00 = net purchases 180.00. |
| R01.19 | Purchases — Product-wise purchases | Group invoice/matched purchase lines by product/unit using recorded costs and allocated charges. | 20 ea invoiced - 2 returned = net 18 ea / 180.00; no second receipt on invoice posting. |
| R01.20 | Purchases — Purchase returns | List effective return quantities and original cost/tax credits with source invoice/receipt references. | Return 2 ea / 20.00; linked original unit cost 10.00. |
| R01.21 | Purchases — Outstanding purchases | Show unpaid posted invoices separately from ordered-but-unreceived quantities; apply effective allocations as of cutoff. | AP 100.00 = invoice 200.00 - return 20.00 - payment 80.00; unreceived order 80 ea is separate. |
| R01.22 | Purchases — Purchase history | Chronological linked order, receipt, invoice, return and settlement events; totals must not double count receiving and invoicing. | Order 100 ea; receipt 20; invoice 200.00; return 2/20.00; payment 80.00; AP 100.00. |
| R01.23 | Accounting — Customer ledger | Opening AR plus effective debit events minus credit notes/payments; include source and running balance. | Customer A AR 200.00 - credit 40.00 - receipt 40.00 = 120.00 at cutoff. |
| R01.24 | Accounting — Supplier ledger | Opening AP plus effective invoices minus debit notes/payments; label debit/credit directions. | Supplier A AP 200.00 - debit note 20.00 - payment 80.00 = 100.00 at cutoff. |
| R01.25 | Accounting — General Ledger | Opening plus posted journal debits/credits by account through cutoff; no mutable master balance. | Inventory 1050.00 debit, cash 40.00 debit, AR 120.00 debit, AP 100.00 credit; all source journals balanced. |
| R01.26 | Accounting — Cash Book | Classified cash-account journal movements with opening/running/closing balances; never invoice totals. | Receipts 140.00 - supplier payment 80.00 - expense 20.00 = cash 40.00. |
| R01.27 | Accounting — Bank Book | Only selected bank-account journal movements; cash-to-bank transfers have equal opposite liquid-asset legs. | Baseline bank is 0.00; separate transfer variant: cash -10.00 / bank +10.00, no income. |
| R01.28 | Accounting — Trial balance | Aggregate debit/credit balances from posted journals including opening entries at cutoff. | Ending debits 1360.00 = credits 1360.00; turnover is labeled separately. |
| R01.29 | Accounting — Profit and loss | Net recognized revenue less recorded COGS and expenses under account mappings, excluding opening equity. | 260.00 - 130.00 - 20.00 = profit 110.00. |
| R01.30 | Accounting — Balance sheet | Assets = liabilities + equity including retained/current earnings at cutoff. | Assets 1210.00 = liabilities 100.00 + opening equity 1000.00 + earnings 110.00. |
| R01.31 | Accounting — Cash flow | Aggregate classified cash/bank journal movements; eliminate internal transfers; reconcile opening-to-closing liquid funds. | Operating net cash 40.00; financing/investing 0.00; opening 0.00 to closing 40.00. |
| R01.32 | Accounting — Receivables aging | As-of unpaid AR by contractual due date; apply only allocations/credits effective by cutoff. | AR 120.00 in 1–30 days overdue (due Jan 15, cutoff Jan 31); February receipt excluded. |
| R01.33 | Accounting — Payables aging | As-of unpaid AP by contractual due date; apply only allocations/debits effective by cutoff. | AP 100.00 in 1–30 days overdue; February supplier payment excluded. |
| R01.34 | Manufacturing — Daily production | Group effective accepted/rejected production quantities by local production date and compatible units. | 10 accepted finished ea on production day; historical cost 150.00. |
| R01.35 | Manufacturing — Batch-wise production | Produced quantities and recorded material/labor/overhead by output batch; distinguish production from remaining stock. | Batch G: produced 10 ea / cost 150.00; sold 4, damaged 1, remaining 5. |
| R01.36 | Manufacturing — Manufacturing cost | Recorded consumed material + allocated labor/overhead, with explicit WIP and output cost reconciliation. | 100.00 raw + 20.00 labor + 30.00 overhead = 150.00; 10 ea unit cost 15.00; no duplicated expense. |
| R01.37 | Manufacturing — Raw material consumption | Sum actual batch issues in base units and their historical inventory costs, linked to orders/output genealogy. | 20 kg at 5.00 = 100.00; 2 kg normal waste is already included, not another issue. |
| R01.38 | Manufacturing — Production wastage | Separate normal waste, abnormal loss, scrap/rework and finished damage with explicit disposition/cost treatment. | Normal raw waste 2 kg / 10.00 included in production cost; finished damage 1 ea / 15.00 is a separate loss. |
| R01.39 | Manufacturing — Finished goods | Output and eligible finished stock by batch/location at cutoff; subtract actual sales/damage, not planned output. | Produced 10 ea; sold 4; damage 1; remaining 5 ea / 75.00. |
| R01.40 | Manufacturing — Batch profitability | Attributable net realized revenue minus sold recorded cost and separately recorded attributable losses; unsold stock is not revenue. | Revenue 100.00 - sold cost 60.00 - damage loss 15.00 = 25.00; remaining stock value 75.00. |

## Per-report execution checklist

All **240 cases below are not run**. The [machine-readable cases](report-test-cases.json) specify role, source, prerequisites, fixture/input, steps, expected API/UI result, stock/journal effects, actual result/status and evidence. A test may only be marked passed after linking an executable case and actual run artifact. Shared test helpers may parameterize cases but must not replace report-specific expectations.

| Report | Totals | Filters | Permissions | Drill-downs | History | PDF + XLSX |
|---|---|---|---|---|---|---|
| Current stock | R01.01.totals | R01.01.filters | R01.01.permissions | R01.01.drilldowns | R01.01.history | R01.01.exports |
| Stock movement | R01.02.totals | R01.02.filters | R01.02.permissions | R01.02.drilldowns | R01.02.history | R01.02.exports |
| Stock valuation | R01.03.totals | R01.03.filters | R01.03.permissions | R01.03.drilldowns | R01.03.history | R01.03.exports |
| Low-stock | R01.04.totals | R01.04.filters | R01.04.permissions | R01.04.drilldowns | R01.04.history | R01.04.exports |
| Out-of-stock | R01.05.totals | R01.05.filters | R01.05.permissions | R01.05.drilldowns | R01.05.history | R01.05.exports |
| Batch-wise stock | R01.06.totals | R01.06.filters | R01.06.permissions | R01.06.drilldowns | R01.06.history | R01.06.exports |
| Warehouse-wise stock | R01.07.totals | R01.07.filters | R01.07.permissions | R01.07.drilldowns | R01.07.history | R01.07.exports |
| Damaged stock | R01.08.totals | R01.08.filters | R01.08.permissions | R01.08.drilldowns | R01.08.history | R01.08.exports |
| Daily sales | R01.09.totals | R01.09.filters | R01.09.permissions | R01.09.drilldowns | R01.09.history | R01.09.exports |
| Weekly sales | R01.10.totals | R01.10.filters | R01.10.permissions | R01.10.drilldowns | R01.10.history | R01.10.exports |
| Monthly sales | R01.11.totals | R01.11.filters | R01.11.permissions | R01.11.drilldowns | R01.11.history | R01.11.exports |
| Annual sales | R01.12.totals | R01.12.filters | R01.12.permissions | R01.12.drilldowns | R01.12.history | R01.12.exports |
| Customer-wise sales | R01.13.totals | R01.13.filters | R01.13.permissions | R01.13.drilldowns | R01.13.history | R01.13.exports |
| Product-wise sales | R01.14.totals | R01.14.filters | R01.14.permissions | R01.14.drilldowns | R01.14.history | R01.14.exports |
| Profit margin | R01.15.totals | R01.15.filters | R01.15.permissions | R01.15.drilldowns | R01.15.history | R01.15.exports |
| Credit sales | R01.16.totals | R01.16.filters | R01.16.permissions | R01.16.drilldowns | R01.16.history | R01.16.exports |
| Cash sales | R01.17.totals | R01.17.filters | R01.17.permissions | R01.17.drilldowns | R01.17.history | R01.17.exports |
| Supplier-wise purchases | R01.18.totals | R01.18.filters | R01.18.permissions | R01.18.drilldowns | R01.18.history | R01.18.exports |
| Product-wise purchases | R01.19.totals | R01.19.filters | R01.19.permissions | R01.19.drilldowns | R01.19.history | R01.19.exports |
| Purchase returns | R01.20.totals | R01.20.filters | R01.20.permissions | R01.20.drilldowns | R01.20.history | R01.20.exports |
| Outstanding purchases | R01.21.totals | R01.21.filters | R01.21.permissions | R01.21.drilldowns | R01.21.history | R01.21.exports |
| Purchase history | R01.22.totals | R01.22.filters | R01.22.permissions | R01.22.drilldowns | R01.22.history | R01.22.exports |
| Customer ledger | R01.23.totals | R01.23.filters | R01.23.permissions | R01.23.drilldowns | R01.23.history | R01.23.exports |
| Supplier ledger | R01.24.totals | R01.24.filters | R01.24.permissions | R01.24.drilldowns | R01.24.history | R01.24.exports |
| General Ledger | R01.25.totals | R01.25.filters | R01.25.permissions | R01.25.drilldowns | R01.25.history | R01.25.exports |
| Cash Book | R01.26.totals | R01.26.filters | R01.26.permissions | R01.26.drilldowns | R01.26.history | R01.26.exports |
| Bank Book | R01.27.totals | R01.27.filters | R01.27.permissions | R01.27.drilldowns | R01.27.history | R01.27.exports |
| Trial balance | R01.28.totals | R01.28.filters | R01.28.permissions | R01.28.drilldowns | R01.28.history | R01.28.exports |
| Profit and loss | R01.29.totals | R01.29.filters | R01.29.permissions | R01.29.drilldowns | R01.29.history | R01.29.exports |
| Balance sheet | R01.30.totals | R01.30.filters | R01.30.permissions | R01.30.drilldowns | R01.30.history | R01.30.exports |
| Cash flow | R01.31.totals | R01.31.filters | R01.31.permissions | R01.31.drilldowns | R01.31.history | R01.31.exports |
| Receivables aging | R01.32.totals | R01.32.filters | R01.32.permissions | R01.32.drilldowns | R01.32.history | R01.32.exports |
| Payables aging | R01.33.totals | R01.33.filters | R01.33.permissions | R01.33.drilldowns | R01.33.history | R01.33.exports |
| Daily production | R01.34.totals | R01.34.filters | R01.34.permissions | R01.34.drilldowns | R01.34.history | R01.34.exports |
| Batch-wise production | R01.35.totals | R01.35.filters | R01.35.permissions | R01.35.drilldowns | R01.35.history | R01.35.exports |
| Manufacturing cost | R01.36.totals | R01.36.filters | R01.36.permissions | R01.36.drilldowns | R01.36.history | R01.36.exports |
| Raw material consumption | R01.37.totals | R01.37.filters | R01.37.permissions | R01.37.drilldowns | R01.37.history | R01.37.exports |
| Production wastage | R01.38.totals | R01.38.filters | R01.38.permissions | R01.38.drilldowns | R01.38.history | R01.38.exports |
| Finished goods | R01.39.totals | R01.39.filters | R01.39.permissions | R01.39.drilldowns | R01.39.history | R01.39.exports |
| Batch profitability | R01.40.totals | R01.40.filters | R01.40.permissions | R01.40.drilldowns | R01.40.history | R01.40.exports |

Also required: R02 dashboard reconciliation; R03 historical master-data changes; R04 timezone/as-of boundaries; R05 artifact fidelity; R06 full-row pagination/exports; R07 access controls; R08 job failure/retry recovery. No completed report count may be derived from route count or case count.
