from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: str = Field(min_length=3, max_length=254)
    name: str = Field(min_length=1, max_length=160)
    password: str = Field(min_length=12, max_length=256)
    role_ids: list[UUID] = Field(max_length=30)

    @field_validator('email')
    @classmethod
    def email_valid(cls, value):
        import re
        value = value.strip().lower()
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', value):
            raise ValueError('Invalid email')
        return value


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: int = Field(ge=1)
    name: str | None = Field(default=None, min_length=1, max_length=160)
    active: bool | None = None
    role_ids: list[UUID] | None = Field(default=None, max_length=30)
    password: str | None = Field(default=None, min_length=12, max_length=256)


class UserRead(BaseModel):
    id: UUID
    email: str
    name: str
    active: bool
    version: int
    role_ids: list[UUID]


class UserPage(BaseModel):
    items: list[UserRead]
    total: int
    page: int
    page_size: int
