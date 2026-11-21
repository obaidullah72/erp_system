import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def error_response(request, status, code, message, details=None, headers=None):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(status_code=status, headers=headers, content={
        "error": {"code": code, "message": message, "details": details},
        "request_id": request_id,
    })


def register_exception_handlers(app: FastAPI):
    from app.shared.errors import BusinessError
    from sqlalchemy.exc import IntegrityError

    @app.exception_handler(BusinessError)
    async def business_error(request: Request, exc: BusinessError):
        return error_response(request, exc.status, exc.code, exc.message)

    @app.exception_handler(IntegrityError)
    async def integrity_error(request: Request, exc: IntegrityError):
        return error_response(request, 409, "constraint_conflict", "The change conflicts with an existing record or constraint")

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return error_response(request, exc.status_code, "http_error", str(exc.detail), headers=exc.headers)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        details = [{"location": list(e["loc"]), "type": e["type"]} for e in exc.errors()]
        return error_response(request, 422, "validation_error", "Request validation failed", details)

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exc: Exception):
        logger.error("Unhandled application error", extra={
            "request_id": getattr(request.state, "request_id", None), "error_type": type(exc).__name__,
        })
        return error_response(request, 500, "internal_error", "An unexpected error occurred")
