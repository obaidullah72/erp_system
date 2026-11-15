import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.security import decode_access_token

bearer = HTTPBearer(auto_error=False)


def token_subject(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
    """JWT verification foundation only. User activation and permissions arrive in Phase 2."""
    if credentials is None:
        raise HTTPException(401, "Authentication required", headers={"WWW-Authenticate": "Bearer"})
    try:
        return decode_access_token(credentials.credentials)["sub"]
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid or expired access token", headers={"WWW-Authenticate": "Bearer"}) from None
