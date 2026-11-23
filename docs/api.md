# /api/v1 contract baseline

OpenAPI at `/openapi.json` and `/docs` (development only) describes **implemented HTTP routes only**. Planned paths below intentionally return 404 today. The internal posting and inventory contracts are Python contracts, not public HTTP endpoints. The committed `docs/openapi.json` snapshot is regenerated with `make contracts`. This baseline is version 1; incompatible wire changes require a new API version.

## Implemented routes

| Method/path (prefix /api/v1) | Permission | Request / result |
|---|---|---|
| GET /health/live | public | coarse service status; no database dependency |
| GET /health/ready | public | database connectivity; 503 if unavailable |
| POST /auth/login | public, CSRF header/origin check | `{business,email,password}` → bearer access token, expiry seconds, current user; HttpOnly refresh cookie |
| POST /auth/refresh | refresh cookie, CSRF check | rotates refresh secret, returns same token/user envelope; invalid/replayed secret returns 401 |
| POST /auth/logout | bearer + CSRF check | immediate session revocation; 204; clears refresh cookie |
| GET /auth/me | bearer | `{id,business_id,email,name,roles,permissions}` |
| GET /users | users:read | paginated; q (email substring), active boolean |
| POST /users | users:create | `{email,name,password,role_ids}` → safe user, 201 |
| PATCH /users/{id} | users:update | `{version,name?,active?,password?,role_ids?}` → safe user; protects last Super Admin |
| GET /roles | roles:read | paginated roles with explicit permission codes |
| GET /roles/permissions | roles:read | complete module/action catalogue; includes planned capabilities |
| POST /roles | roles:create plus Super Admin | `{name,permissions}` → custom role, 201 |
| PATCH /roles/{id} | roles:update plus Super Admin | `{version,permissions}`; protected admin grants; Viewer remains read-only |
| GET /business-settings | settings:read | `{business_id,currency,timezone,version}` |
| PATCH /business-settings | settings:update | `{version,currency,timezone}`; currency immutable after posting |

User read DTO: `{id,email,name,active,version,role_ids}`. Role DTO: `{id,name,system,version,permissions}`. Password hashes and refresh hashes are never serialized. IDs are UUID strings. Cross-business item access returns 404, permission denial 403, unauthenticated/expired/revoked session 401. Admin cannot create, assign, disable or edit administrators; role configuration is Super Admin-only even if a grant is misconfigured. Responsibility roles are configurable without gaining administrative writes.

## Common wire rules

- Lists: `?page=1&page_size=25`; page ≥ 1, size 1–100. Response `{items:[],total:0,page:1,page_size:25}`. Stable sort with UUID tie-breaker; implemented users sort email/id and roles name/id. Filtering happens before pagination and counting.
- Planned document filters: `q`, `status`, `date_from`, `date_to`, `partner_id`, `warehouse_id`, `product_id`, `source_id` as appropriate. Dates inclusive, date_from ≤ date_to. Planned `sort` is an allowlisted field, prefixed `-` for descending; never interpolate arbitrary SQL. Unsupported sort/filter fields must return 422 when implemented.
- Money/quantity/FX: decimal **strings**, never JSON float. Example `"123.45"`; no NaN/infinity. Dates `YYYY-MM-DD`; instants RFC3339 UTC with offset. UUIDs canonical strings. No locale-specific numeric formats.
- PATCH on mutable resources requires integer `version`. Successful change increments it. Stale version returns 409 `version_conflict`; fetch fresh data and reconcile. Omitted optional PATCH properties remain unchanged. Null values are not deletion commands.
- Errors: `{ "error": { "code":"version_conflict", "message":"Reload settings before updating", "details":null }, "request_id":"UUID" }`. Validation uses 422 `validation_error` with field locations/types only; never input values. Expected business conflicts use stable codes; integrity conflicts use 409 `constraint_conflict`; unexpected failures use redacted 500 `internal_error`. Every HTTP response has `X-Request-ID`.
- Auth sends `Authorization: Bearer <access token>`. Login/refresh/logout also send `X-ERP-CSRF: 1`; browser cookies use credentials mode. Explicit Origin allowlist. Frontend access token is memory-only. Refresh cookie is HttpOnly, SameSite=Strict, restricted to `/api/v1/auth`, Secure in production. Cross-site frontend deployments are not supported by this cookie policy; prefer same-origin proxy.
- No automatic mutation retry in the API client. It may refresh then replay a rejected 401 once; authorization rejection happens before mutation. Refresh calls are coalesced within a tab and serialized across supporting browsers using Web Locks. No automatic retry for 403/409/422. GET may be manually retried on connection failure. Do not assume a timeout means a mutation failed.
- Planned document posting requires `Idempotency-Key` (1–128 chars), source identity, expected document version, and canonical request hash. Same key/payload returns original result; changed payload returns 409. Different key/same source returns 409. Financial idempotency records are retained with journals. Internal kernel already enforces this policy.
- Transient SQLSTATE 40001/40P01: future orchestration may retry the entire command at most three times with jitter and unchanged idempotency key. Stage 1 kernel leaves retry ownership to the caller; it never commits or retries a partial transaction.
- Request transaction commits **before** sending the response (`Depends(..., scope='function')`); exceptions roll back writes, audit and idempotency together. Permission is checked server-side on every request from the live database, never trusted from token role claims.

## Planned module resources

Each row requires its module `:read` for reads; write commands require `:create`, `:update`, `:approve`, `:post`, `:reverse`, or `:export` as applicable. Possessing a grant does not imply implementation. No business POST in this table exists yet.

| Module | Proposed routes/resources | Command semantics / dependencies |
|---|---|---|
| products | /products, /units, /product-unit-conversions, /fitments | versioned CRUD; catalogue references |
| categories, brands | /categories, /brands | tenant codes, category tree validation |
| warehouses | /warehouses, /bins | locations; forbid deletion with history |
| customers, suppliers, vendors | /customers, /suppliers, /vendors, /partners | role views over shared partner identity |
| employees | /employees | optional user link; employee permissions |
| raw_materials | /raw-materials | product-kind view, no duplicate stock master |
| inventory | /inventory/balances, /inventory/movements, /inventory/reservations, /inventory/transfers | read movements; reserve/release; transfer dispatch/receive; no direct balance PATCH |
| batches | /batches, /lots, /serials, /batches/{id}/genealogy | read traceability; lot registration and status events |
| purchases | /purchase-orders, /goods-receipts, /supplier-invoices | approve/receive/post/reverse; stock and journal atomic |
| sales | /sales-orders, /shipments, /sales-invoices | approve/fulfill/post/reverse; stock and journal atomic |
| pos | /pos/sessions, /pos/sales, /pos/tenders | open/close session; sale posting includes tender |
| returns_adjustments | /returns, /stock-adjustments | original source references; approve/post/reverse |
| accounting | /journal-entries, /journal-entries/{id}/reversal | authorized posting orchestration around existing kernel |
| chart_of_accounts | /accounts, /account-mappings, /fiscal-periods | versioned masters; audited close/reopen policy |
| cash_bank | /bank-accounts, /bank-transactions, /payments, /receipts, /reconciliations | post/reconcile; unique bank references |
| credit_debit | /credit-notes, /debit-notes | link original invoice; post/reverse |
| expenses | /expenses | approve/post; attachment references |
| receivables, payables | /receivables, /payables, /payment-allocations | read outstanding; create/reverse allocations under locks |
| customer_ledgers, supplier_ledgers | /customer-ledgers/{partner_id}, /supplier-ledgers/{partner_id} | immutable journal/allocation projections; date filters |
| general_ledger | /general-ledger | account/date/source filters; no mutable balance API |
| financial_statements | /financial-statements/trial-balance, /profit-loss, /balance-sheet, /cash-flow | accounting-date and currency filters; as-of timestamp |
| bom | /boms, /boms/{id}/versions | approve/retire immutable revisions |
| production_planning | /work-orders, /production-schedules | release/schedule, frozen BOM snapshot |
| manufacturing | /material-issues, /production-completions, /scrap, /rework | post atomically with inventory, genealogy and WIP |
| quality_control | /quality-inspections, /quality-releases | inspected→pass/fail; quarantine ownership |
| production_costing | /cost-runs, /cost-allocations, /production-variances | reconcile and post linked adjustments |
| audit_logs | /audit-logs | read/export, business/date/actor/source filters; no write/delete routes |
| dashboard | /dashboard/summary | permission-filtered, real aggregates; unavailable metrics null with availability reason |
| reports | /reports, /exports | authorized query and future asynchronous export jobs; no worker business tasks today |

Example planned posting: `POST /sales-invoices/{id}/post`, header `Idempotency-Key`, body `{ "version":3, "accounting_date":"2026-11-21" }`; response `{ "id":"UUID", "status":"posted", "version":4, "journal_entry_id":"UUID" }`. This example is a future contract, not an implemented endpoint.
