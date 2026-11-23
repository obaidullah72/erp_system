# Phase 1 — Foundation

## Goal

Create a runnable, modular ERP foundation with PostgreSQL, authentication, permissions, initial migrations and a professional dashboard layout. Establish shared data integrity and financial posting infrastructure before transactional modules depend on it.

## Prerequisites

Read the original requirements and shared standards. Inspect any existing repository before generating files. Confirm the business configuration assumptions and select compatible dependencies without hardcoding credentials.

## Scope and implementation order

1. Initialize the React/Vite frontend and FastAPI backend under business-erp.
2. Configure Tailwind CSS v4 through its Vite plugin, routing, Axios, forms, validation, icons and charts.
3. Create the required backend layers and frontend module folders.
4. Configure PostgreSQL, SQLAlchemy sessions, Alembic and environment-based settings.
5. Add authentication, server-side permissions, audit infrastructure and the minimal journal posting contract.
6. Build the responsive dashboard shell, login screens, theme toggle and reusable UI primitives.
7. Add Docker Compose, health checks, structured logging and developer documentation.

Use Redis and worker service configuration when required. Separate public web, API, worker and database responsibilities; workers must use the same domain services as synchronous operations.

## Database tables

| Tables | Responsibility |
| --- | --- |
| businesses, business_settings | Base currency, timezone, fiscal year and operational configuration |
| users, roles, permissions, user_roles, role_permissions | Identity and action-level access |
| refresh_sessions | Refresh token/session revocation when this strategy is selected |
| audit_logs | Actor, operation, resource and timestamp for sensitive events |
| document_sequences, idempotency_records | Unique references and safe retry infrastructure |
| accounts, journal_entries, journal_entry_lines | Minimal balanced posting kernel, expanded in Phase 5 |

Create migrations with foreign keys, uniqueness, amount checks and appropriate indexes. Define role defaults: Super Admin, Business Owner, Manager, Accountant, Inventory Manager, Sales Operator, Purchase Operator, Production Manager and Read-only User.

The accounting kernel must enforce balancing through a controlled posting service; a row-level CHECK alone cannot sum all journal lines. Keep journal tables protected from direct uncontrolled writes.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET | /health/live | Process health |
| GET | /health/ready | Required dependency readiness |
| POST | /auth/login | Verify credentials and establish authentication |
| POST | /auth/refresh | Rotate/renew authentication under the selected strategy |
| POST | /auth/logout | Revoke refresh/session credentials |
| GET | /auth/me | Current user and effective permissions |
| GET/POST | /users | Authorized user listing and creation |
| GET/PATCH | /users/{id} | View or update an authorized user |
| GET/POST/PATCH | /roles and /roles/{id} | Permission administration |
| GET/PATCH | /settings/business | Authorized business configuration |
| GET | /dashboard/summary | Real initial metrics or a clear no-data response |

All routes except health checks and authentication entry points require appropriate authorization.

## Backend work

Implement configuration validation, password hashing, token expiration, refresh/session handling, CORS configuration, request IDs and a common error format. Never issue known default passwords or log tokens. Use a controlled first-admin bootstrap process.

Create service boundaries for inventory and accounting even before full workflows exist. Define the posting event contract, source uniqueness, period validation extension points, and transaction ownership. Account mappings used by later phases must fail explicitly when missing.

## Frontend work

Implement AuthLayout and DashboardLayout, protected routes, sidebar navigation and a top bar with user controls. Build reusable inputs, selects, buttons, tables, modals, date filters, toast messages and loading/empty/error components.

Show business dashboard placeholders as “No transactions yet” when appropriate. Do not populate business metrics with fabricated values. Display permission-based navigation while retaining backend enforcement.

## Acceptance checks

- A fresh developer can start the services from the documented instructions.
- Alembic creates a clean database successfully and the application connects.
- Valid login works; invalid credentials and expired authentication fail consistently.
- A Read-only User cannot create users or update settings through direct API calls.
- Session revocation/refresh behavior matches the documented strategy.
- Posting an unbalanced journal fails without committing journal or audit fragments.
- Reusing the same posting source cannot create a second finalized posting.
- Responsive navigation, keyboard focus and theme persistence work.
- Health responses and logs do not expose secrets.

## Deliverables and exit criteria

Deliver the initialized repository, dependency lockfiles, .env.example, Docker configuration, migration history, authentication API documentation and a working connected dashboard shell.

Record actual verification results and setup steps. Exit only when authentication, permission boundaries, clean database initialization and the posting contract are demonstrably usable by later phases.
