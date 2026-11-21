from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PostingLine(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    mapping: str = Field(min_length=1, max_length=60)
    debit: Decimal = Field(default=Decimal('0'), ge=0, lt=Decimal('100000000000000'), max_digits=20, decimal_places=2, allow_inf_nan=False)
    credit: Decimal = Field(default=Decimal('0'), ge=0, lt=Decimal('100000000000000'), max_digits=20, decimal_places=2, allow_inf_nan=False)

    @field_validator('debit', 'credit', mode='before')
    @classmethod
    def decimal_only(cls, value):
        if not isinstance(value, (str, Decimal)):
            raise ValueError('Money must be a decimal string or Decimal')
        return value

    @model_validator(mode='after')
    def one_side(self):
        if (self.debit > 0) == (self.credit > 0):
            raise ValueError('Exactly one side must be positive')
        return self


class PostingEvent(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    business_id: UUID
    actor_id: UUID
    source_type: str = Field(min_length=1, max_length=60, pattern=r'^[a-z][a-z0-9_]*$')
    source_id: str = Field(min_length=1, max_length=100)
    event: str = Field(min_length=1, max_length=60, pattern=r'^[a-z][a-z0-9_]*$')
    accounting_date: date
    currency: str = Field(pattern=r'^[A-Z]{3}$')
    lines: tuple[PostingLine, ...] = Field(min_length=2, max_length=500)
