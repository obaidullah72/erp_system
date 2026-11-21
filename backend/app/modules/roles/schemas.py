from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1, max_length=80, pattern=r'^[A-Za-z][A-Za-z0-9 _-]*$')
    permissions: list[str] = Field(max_length=300)


class RoleUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: int = Field(ge=1)
    permissions: list[str] = Field(max_length=300)


class RoleRead(BaseModel):
    id: UUID
    name: str
    system: bool
    version: int
    permissions: list[str]


class RolePage(BaseModel):
    items: list[RoleRead]
    total: int
    page: int
    page_size: int
