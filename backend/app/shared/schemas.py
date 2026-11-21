from pydantic import BaseModel


class ErrorDetail(BaseModel):
    location: list[str | int]
    type: str


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] | None = None


class ErrorEnvelope(BaseModel):
    error: ErrorBody
    request_id: str | None = None
