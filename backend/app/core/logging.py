import json
import logging
import re
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": re.sub(r"(redis[s]?|postgresql(?:\+psycopg)?|https?)://[^\s]+", "[redacted-url]", record.getMessage()),
        }
        for key in ("request_id", "method", "path", "status", "duration_ms", "error_type"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload)


def configure_logging(level: str):
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
    # Uvicorn's access log includes query strings; use our sanitized request log.
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.error").propagate = True
