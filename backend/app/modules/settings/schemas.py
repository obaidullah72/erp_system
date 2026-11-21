from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from pydantic import BaseModel, ConfigDict, Field, field_validator


class SettingsUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: int = Field(ge=1)
    currency: str = Field(pattern=r'^[A-Z]{3}$')
    timezone: str = Field(max_length=64)

    @field_validator('timezone')
    @classmethod
    def timezone_exists(cls, value):
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError('Unknown timezone') from None
        return value


class SettingsRead(SettingsUpdate):
    model_config = ConfigDict(from_attributes=True)
    business_id: UUID
