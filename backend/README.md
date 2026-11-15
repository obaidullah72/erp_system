# Backend foundation

From the repository root, run `make install`, configure `backend/.env`, then `make migrate` and `make backend`. Settings load `backend/.env` regardless of working directory. Shell environment variables take precedence.

`app.main:app` is an ASGI app wrapped globally for CORS and request logging. The FastAPI factory is `create_app()`. Routes live under `/api/v1`. Database sessions close automatically; repositories must not commit. Business services will own explicit transaction scopes in future phases.

`requirements.txt` contains direct runtime constraints, including SQLAlchemy 2.0.x and Pydantic v2; `requirements-dev.txt` adds verification tools. These are bounded dependency manifests, not a fully resolved Python lockfile. Resolve and audit a lockfile before a production release.
