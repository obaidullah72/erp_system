# Phase 1 API

Base path: `/api/v1`. Development OpenAPI: `/openapi.json`; Swagger UI: `/docs`. Both are disabled in production settings.

| Method/path | Result |
| --- | --- |
| GET `/health/live` | 200 `{"status":"ok","service":"erp-api"}`; no database connection |
| GET `/health/ready` | 200 with `database: "connected"` after SELECT 1; 503 with `status: "unavailable"`, `database: "unavailable"` on failure |

Readiness is connectivity only, not schema or business-module readiness. Both responses have `Cache-Control: no-store`. The service name is `erp-api`. Every HTTP response includes generated `X-Request-ID`; CORS exposes it to permitted origins. No authentication is required for health.

Errors use `{"error":{"code":"...","message":"...","details":null},"request_id":"..."}`. Validation returns sanitized location/type details without user input. Readiness 503 is a typed health response, not the generic error envelope. No business or login endpoints exist in this phase.
