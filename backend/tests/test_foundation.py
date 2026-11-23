from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware

from app.core.config import Settings
from app.core.middleware import RequestLoggingMiddleware
from app.db.session import get_db
from app.main import app, create_app


@pytest.fixture
def api_client():
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


def test_liveness_is_independent_of_database(api_client):
    response = api_client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "erp-api"}
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-request-id"]


def test_readiness_success_runs_database_query():
    application = create_app()
    session = Mock()
    session.execute.return_value.scalar_one.return_value = 1
    application.dependency_overrides[get_db] = lambda: session
    with TestClient(application) as client:
        response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"
    assert str(session.execute.call_args.args[0]) == "SELECT 1"


def test_readiness_failure_is_503_and_redacted():
    application = create_app()
    session = Mock()
    session.execute.side_effect = OperationalError("secret database host", {}, Exception("secret password"))
    application.dependency_overrides[get_db] = lambda: session
    with TestClient(application) as client:
        response = client.get("/api/v1/health/ready")
    assert response.status_code == 503
    assert response.json()["database"] == "unavailable"
    assert "secret" not in response.text
    session.rollback.assert_called_once()


def test_unknown_api_path_is_json_404(api_client):
    response = api_client.get("/api/v1/missing")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "http_error"
    assert response.json()["request_id"] == response.headers["x-request-id"]


def test_cors_is_explicit(api_client):
    allowed = api_client.get("/api/v1/health/live", headers={"Origin": "http://localhost:5173"})
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "X-Request-ID" in allowed.headers["access-control-expose-headers"]
    denied = api_client.get("/api/v1/health/live", headers={"Origin": "https://untrusted.example"})
    assert "access-control-allow-origin" not in denied.headers


def test_errors_are_redacted_and_keep_cors_and_request_id():
    application = create_app()

    @application.get("/explode")
    def explode():
        raise RuntimeError("do not expose this credential")

    wrapped = RequestLoggingMiddleware(CORSMiddleware(application, allow_origins=["http://localhost:5173"]))
    with TestClient(wrapped, raise_server_exceptions=False) as client:
        response = client.get("/explode", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 500
    assert "credential" not in response.text
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert response.json()["request_id"] == response.headers["x-request-id"]


def test_validation_never_echoes_input():
    application = create_app()

    class Payload(BaseModel):
        count: int

    @application.post("/validate")
    def validate(payload: Payload):
        return payload

    with TestClient(application) as client:
        response = client.post("/validate", json={"count": "secret-value"})
    assert response.status_code == 422
    assert "secret-value" not in response.text
    assert response.json()["error"]["details"][0]["location"] == ["body", "count"]


def test_settings_reject_unsafe_production_and_wildcard_cors():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, environment="production", jwt_secret_key=None)
    with pytest.raises(ValidationError):
        Settings(_env_file=None, cors_origins=["*"])
    with pytest.raises(ValidationError):
        Settings(_env_file=None, database_url="sqlite:///erp.db")
    with pytest.raises(ValidationError):
        Settings(_env_file=None, jwt_secret_key="too-short")


def test_settings_validation_does_not_print_secret_inputs():
    with pytest.raises(ValidationError) as captured:
        Settings(_env_file=None, jwt_secret_key='secret-too-short',
                 database_url='postgresql+psycopg://erp:database-secret@localhost/erp')
    assert 'secret-too-short' not in str(captured.value)
    assert 'database-secret' not in str(captured.value)
