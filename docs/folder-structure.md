# Directory purposes

| Path | Purpose |
| --- | --- |
| `frontend/src/app/` | Route tree and navigation configuration |
| `frontend/src/layouts/` | Reusable responsive application shell |
| `frontend/src/components/layout/` | Sidebar and header |
| `frontend/src/components/ui/` | Shared error presentation; remaining empty files are pre-existing |
| `frontend/src/pages/` | System status, foundation, roadmap, route error and 404 pages |
| `frontend/src/hooks/` | Browser theme behavior; other empty hooks are reserved |
| `frontend/src/lib/` | Axios transport and safe frontend error messages |
| `frontend/src/config/` | Public frontend API configuration |
| `frontend/src/index.css` | Tailwind v4 import, theme variant, and global styles |
| `frontend/src/modules/` | Pre-existing empty business scaffolds; not routed or functional |
| `frontend/nginx.conf` | Container SPA fallback and same-origin API proxy |
| `backend/app/main.py` | ASGI entry point, lifespan, FastAPI factory, global middleware |
| `backend/app/api/v1/` | API composition and health route/schema/service/repository |
| `backend/app/core/` | Settings, JSON logging, middleware, exceptions, JWT utilities |
| `backend/app/auth/` | Bearer verification dependency; login/user persistence is Phase 2 |
| `backend/app/db/` | SQLAlchemy base, naming conventions, engine, session dependency |
| `backend/app/modules/` | Pre-existing empty domain scaffolds; no business implementations |
| `backend/app/shared/` | Reserved shared business primitives; currently empty |
| `backend/app/workers/` | Pre-existing inactive placeholders; Celery not configured |
| `backend/migrations/` | Alembic environment, revision template, empty foundation baseline |
| `backend/tests/` | Foundation contract tests; optional real-database connectivity test |
| `docs/` | Architecture, database proposal, roadmap, security, setup and verification |
| `infrastructure/`, `scripts/` | Existing reserved placeholders, not runnable implementation |
| `compose.yaml` | PostgreSQL, one-shot migration, API and frontend containers |
| `compose.production.yaml` | Optional production settings only; requires deployment hardening |
| `Makefile` | Install, run, build, test, migrate and health commands |
| `.env.example`, `backend/.env.example`, `frontend/.env.example` | Safe configuration examples for Compose, native API, and public frontend settings |

Empty scaffolds have intentionally not been expanded. Unused Vite assets and starter CSS remain on disk but are no longer imported. Domain files should gain content only as their approved phase is implemented.
