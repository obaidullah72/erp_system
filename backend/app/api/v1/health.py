from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.api.v1.health_schemas import HealthResponse
from app.api.v1.health_service import database_is_ready
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["System health"])


@router.get("/live", response_model=HealthResponse, response_model_exclude_none=True)
def liveness(response: Response):
    response.headers["Cache-Control"] = "no-store"
    return HealthResponse(status="ok", service="erp-api")


@router.get("/ready", response_model=HealthResponse, responses={503: {"model": HealthResponse}})
def readiness(response: Response, session: Session = Depends(get_db, scope='function')):
    ready = database_is_ready(session)
    response.status_code = 200 if ready else 503
    response.headers["Cache-Control"] = "no-store"
    return HealthResponse(status="ok" if ready else "unavailable", service="erp-api",
                          database="connected" if ready else "unavailable")
