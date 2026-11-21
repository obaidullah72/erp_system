import hashlib
import secrets
from datetime import timedelta
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from app.auth.repository import permissions_for, roles_for
from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.db.model_registry import AuthSession, Business, User, now
from app.modules.audit_logs.service import audit


def user_view(db, user):
    return dict(id=user.id, business_id=user.business_id, email=user.email, name=user.name,
                roles=sorted(r.name for r in roles_for(db, user)), permissions=sorted(permissions_for(db, user)))


def refresh_digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def tokens(db, user, session):
    secret = secrets.token_urlsafe(48)
    session.refresh_hash = refresh_digest(secret)
    db.flush()
    return dict(access_token=create_access_token(str(user.id), str(session.id)), token_type='bearer',
                expires_in=get_settings().access_token_minutes * 60, user=user_view(db, user)), f'{session.id}.{secret}'


def login(db, payload, request_id):
    user = db.scalar(select(User).join(Business).where(Business.slug == payload.business,
                     Business.active.is_(True), User.email == payload.email))
    if not verify_password(payload.password, user.password_hash if user else None) or not user.active:
        raise HTTPException(401, 'Invalid credentials')
    session = AuthSession(business_id=user.business_id, user_id=user.id,
                          refresh_hash=secrets.token_hex(32),
                          expires_at=now() + timedelta(days=get_settings().refresh_token_days))
    db.add(session)
    db.flush()
    audit(db, user.business_id, user.id, 'auth.login', session.id, request_id)
    return tokens(db, user, session)


def refresh(db, value, request_id):
    try:
        session_id, secret = value.split('.', 1)
        session = db.scalar(select(AuthSession).where(AuthSession.id == UUID(session_id)).with_for_update())
    except (ValueError, AttributeError):
        session = None
    if not session or session.revoked_at or session.expires_at <= now():
        return None
    if not secrets.compare_digest(session.refresh_hash, refresh_digest(secret)):
        # Return a normal error response from the route so revocation commits.
        session.revoked_at = now()
        audit(db, session.business_id, session.user_id, 'auth.refresh_reuse', session.id, request_id)
        return None
    user = db.get(User, session.user_id)
    business = db.get(Business, session.business_id)
    if not user.active or not business.active:
        session.revoked_at = now()
        return None
    return tokens(db, user, session)
