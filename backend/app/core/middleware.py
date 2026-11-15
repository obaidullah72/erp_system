import logging
import time
from uuid import uuid4
from starlette.datastructures import MutableHeaders

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        request_id = str(uuid4())
        scope.setdefault("state", {})["request_id"] = request_id
        started = time.perf_counter()
        status = 500

        async def send_with_request_id(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                MutableHeaders(scope=message)["X-Request-ID"] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            logger.info("HTTP request", extra={
                "request_id": request_id, "method": scope["method"],
                "path": scope["path"], "status": status,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            })
