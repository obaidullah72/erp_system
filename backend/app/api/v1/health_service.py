import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.api.v1.health_repository import ping_database

logger = logging.getLogger(__name__)


def database_is_ready(session: Session) -> bool:
    try:
        return ping_database(session)
    except SQLAlchemyError as exc:
        session.rollback()
        logger.warning("Database readiness failed", extra={"error_type": type(exc).__name__})
        return False
