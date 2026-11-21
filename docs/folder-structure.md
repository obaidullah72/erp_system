# Layer and directory map

- `frontend/src/app`: route tree and navigation. `auth`: connected identity/session provider, route guard, permission affordance.
- `frontend/src/layouts`: AuthLayout and DashboardLayout/AppLayout. `components/layout`: sidebar and top bar. `components/ui`: shared button/input/empty/error controls. `hooks/useTheme`: local theme persistence.
- `frontend/src/lib`: Axios transport and refresh lifecycle. `pages`: implemented screens. Existing `modules/*` scaffolds remain inactive until their module is implemented.
- `backend/app/core`: settings validation, JWT/password utilities, grants, logging, middleware and safe errors. `api/v1`: API aggregation and health layers.
- `backend/app/auth`: login/refresh/logout/current identity schemas, queries, service and routes.
- `backend/app/db`: engine, transaction dependency, declarative base, concrete model registry, role seeding. `migrations`: reviewed frozen Alembic revisions.
- `backend/app/modules/{users,roles,settings}`: implemented authorized administration. `accounting`: internal posting contract/kernel and period interface. `inventory/service.py`: interfaces only. `audit_logs/service.py`: append-only safe audit writes.
- `backend/app/shared`: business errors and atomic document numbering. Other empty shared/module files are reserved, not implemented behavior.
- `backend/app/workers`: Celery configuration, diagnostic ping, worker health. `scripts`: explicit bootstrap and isolated browser-test server.
- `backend/tests`, `frontend/tests/e2e`: repeatable verification. `scripts/test-local.sh`: disposable local PostgreSQL runner.
- `compose*.yaml`, Dockerfiles, nginx configs: runtime assembly; root `.env` for Compose, backend `.env` for native API, frontend `.env` for public build settings.
- `docs`: architecture, full domain model, implemented/planned API baseline, security, deployment, tests, traceability and stage completion evidence.
