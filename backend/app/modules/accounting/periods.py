from datetime import date
from typing import Protocol
from uuid import UUID
from sqlalchemy.orm import Session


class PeriodPolicy(Protocol):
    def assert_open(self, db: Session, business_id: UUID, accounting_date: date) -> None:
        """Raise BusinessError for a closed period; caller transaction owns any locks."""
        ...


class OpenPeriodPolicy:
    """Stage 1 only: fiscal-period records and closing workflows are not implemented."""
    def assert_open(self, db, business_id, accounting_date):
        return None
