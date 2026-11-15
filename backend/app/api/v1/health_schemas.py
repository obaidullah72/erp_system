from typing import Literal
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    service: str
    database: Literal["connected", "unavailable"] | None = None
