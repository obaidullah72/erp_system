from dataclasses import dataclass
from uuid import UUID
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from app.core.security import decode_access_token
from app.db.session import get_db
from app.db.model_registry import AuthSession, Business, User, now
from app.auth.repository import permissions_for, roles_for

bearer = HTTPBearer(auto_error=False)


@dataclass
class Identity:
    user: User
    session: AuthSession
    permissions: set[str]
    roles: list[str]


def current_identity(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db=Depends(get_db, scope='function')):
    try:
        if not credentials:
            raise ValueError()
        payload = decode_access_token(credentials.credentials)
        session = db.get(AuthSession, UUID(payload['sid']))
        user = db.get(User, UUID(payload['sub']))
        if (not session or not user or session.user_id != user.id or session.revoked_at
                or session.expires_at <= now() or not user.active):
            raise ValueError()
        business = db.get(Business, user.business_id)
        if not business or not business.active:
            raise ValueError()
        return Identity(user, session, permissions_for(db, user), [r.name for r in roles_for(db, user)])
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise HTTPException(401, 'Authentication required', headers={'WWW-Authenticate': 'Bearer'}) from None


def require(permission):
    def dependency(identity: Identity = Depends(current_identity)):
        if permission not in identity.permissions:
            raise HTTPException(403, 'Permission denied')
        return identity
    return dependency
