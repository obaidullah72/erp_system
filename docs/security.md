# Identity, sessions and authorization

Passwords use Argon2id with library defaults and unique salts, never reversible encryption. User creation/bootstrap require 12–256 characters. Login performs a dummy hash verification for unknown users and returns the same invalid-credentials message. Bootstrap is a CLI-only one-time operation serialized by a PostgreSQL advisory lock; no default password or HTTP bootstrap route exists.

Access JWTs use HS256 with explicit issuer/audience, subject, issued-at and expiry. Default lifetime is 15 minutes (configurable 1–60). `sid` binds each access token to an `auth_sessions` record. Every protected request checks that session, its absolute expiry, active user/business, and live database grants. Password changes, disabling users, logout and refresh replay revoke sessions; access tokens then fail immediately even before their JWT expiry.

Refresh secrets are cryptographically random and only their SHA256 hashes are stored. The browser cookie is HttpOnly, SameSite=Strict, path `/api/v1/auth`, and Secure in production. Refresh rotates the secret under a row lock without extending the absolute seven-day default session lifetime (configurable 1–30 days). Reusing an old refresh secret revokes that session and commits revocation before returning 401. Other sessions are unaffected. Logout revokes the current session and clears the cookie. No refresh tokens, access tokens or passwords are stored in localStorage; only theme preference is persisted there.

Cookie commands require `X-ERP-CSRF: 1` and reject an Origin outside the exact configured allowlist. Non-browser clients may omit Origin but must send the custom header. Same-origin deployment is recommended; SameSite=Strict intentionally excludes cross-site refresh. Browser refresh requests coalesce per tab and use Web Locks where supported to avoid cross-tab rotation races. A lost refresh response may require a new sign-in; replay detection takes precedence over silently accepting old secrets.

## Role policy

Names follow the revised user-approved Stage 1 list exactly:

| Role | Default responsibility |
|---|---|
| Super Admin | All module/action grants; protected user/role controls; configure responsibility roles |
| Admin | Ordinary administration and operational grants; no role configuration or administrator assignment/editing |
| Accountant | Accounting, chart, cash/bank, expenses, credit/debit, allocations, ledgers, statements, reports |
| Sales Manager | Sales/customers/POS/returns; product/inventory/dashboard reads |
| Purchase Manager | Purchasing/suppliers/vendors; product/inventory/dashboard reads |
| Inventory Manager | Products/categories/brands/raw materials, stock/warehouses/batches; dashboard reads |
| Production Manager | BOM/planning/manufacturing/quality/costing; stock/product/raw-material/batch reads |
| Cashier | POS read/create/post; sales/customers/products/dashboard reads |
| Viewer | Dashboard/reports/products/inventory reads only |

`core/permissions.py` is the exact module/action catalogue and initial matrix. Super Admin and Admin grants are protected by service policy. Super Admin may configure other roles; Viewer cannot receive write grants. Custom/responsibility roles cannot gain administrative writes. All roles are business-scoped, including Super Admin. There is no implicit cross-business authority. The last active Super Admin cannot be disabled or lose that role. Membership changes serialize on the business record and use optimistic versions. UI hiding is never the authorization boundary; API dependencies and service policies enforce access directly.

## Logs, secrets and operational boundary

Ignored environment files or a secret manager supply credentials. JWT keys require ≥32 characters and reject example placeholders. Production requires a signing key and database credentials. Explicit HTTP(S) CORS origins cannot contain wildcards, userinfo or paths. Database URLs require the PostgreSQL psycopg driver. Access/refresh lifetimes are bounded. Frontend VITE values are public.

Request logs are structured JSON with generated request ID, method, route template, status and elapsed milliseconds. They omit request/response bodies, headers, query strings, concrete path values and database parameters. Exceptions return coarse messages and validation field locations/types, never raw submitted values. Audit logs store only actor/action/resource/request ID; database triggers prevent update/delete. Health does not reveal credentials, addresses, schema or configuration.

Before internet exposure, deploy TLS and ingress login rate limits, protect Redis on a private network, separate runtime and migration database roles, rotate secrets, audit dependencies and exercise backups. Stage 1 does not implement MFA, password reset, email verification, account lockout, distributed login throttling or multi-business membership. These are explicit follow-on security work, not hidden capabilities. Compose is a development deployment; the production override only enables production settings and Secure cookies.
