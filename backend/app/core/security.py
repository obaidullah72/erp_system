from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import get_settings


def signing_key() -> str:
    secret = get_settings().jwt_secret_key
    if secret is None:
        raise RuntimeError("JWT_SECRET_KEY must be configured before using authentication")
    return secret.get_secret_value()


def create_access_token(subject: str) -> str:
    if not subject:
        raise ValueError("Token subject must not be empty")
    settings = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": subject, "iat": now, "exp": now + timedelta(minutes=settings.access_token_minutes),
                       "iss": settings.jwt_issuer, "aud": settings.jwt_audience}, signing_key(), algorithm="HS256")


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, signing_key(), algorithms=["HS256"], issuer=settings.jwt_issuer,
                      audience=settings.jwt_audience, options={"require": ["exp", "iat", "sub", "iss", "aud"]})
