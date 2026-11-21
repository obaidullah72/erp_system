"""Interfaces only. No stock movement, reservation, or valuation implementation in Stage 1."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol
from uuid import UUID
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class StockCommand:
    business_id: UUID
    product_id: UUID
    warehouse_id: UUID
    quantity: Decimal
    source_type: str
    source_id: UUID
    source_line_id: UUID
    accounting_date: date
    lot_id: UUID | None = None


@dataclass(frozen=True)
class StockResult:
    movement_id: UUID
    carrying_cost: Decimal


class InventoryService(Protocol):
    def receive(self, db: Session, command: StockCommand, unit_cost: Decimal) -> StockResult: ...
    def issue(self, db: Session, command: StockCommand) -> StockResult: ...
    def reserve(self, db: Session, command: StockCommand) -> UUID: ...
    def release(self, db: Session, reservation_id: UUID, business_id: UUID) -> None: ...
    # Implementations must validate positive finite quantities, tenant/FK consistency,
    # lock in stable order, and flush only. Caller owns transaction and idempotency.
