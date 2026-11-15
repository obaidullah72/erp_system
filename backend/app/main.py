from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.router import router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.db.session import engine

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine.dispose()


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan,
                          docs_url=None if settings.environment == "production" else "/docs",
                          redoc_url=None, openapi_url=None if settings.environment == "production" else "/openapi.json")
    register_exception_handlers(application)
    application.include_router(router)
    return application


# Wrap globally so even unhandled error responses receive CORS and request IDs.
app = RequestLoggingMiddleware(CORSMiddleware(
    create_app(), allow_origins=settings.cors_origins, allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"], expose_headers=["X-Request-ID"],
))
