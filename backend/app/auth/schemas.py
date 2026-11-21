from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    business: str = Field(min_length=1, max_length=80, pattern=r'^[a-z0-9-]+$')
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)

    @field_validator('email')
    @classmethod
    def normalize(cls, value):
        return value.strip().lower()


class CurrentUser(BaseModel):
    id: UUID
    business_id: UUID
    name: str
    email: str
    roles: list[str]
    permissions: list[str]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expires_in: int
    user: CurrentUser
