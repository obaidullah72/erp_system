from sqlalchemy import select, delete, update, func
from fastapi import HTTPException
from app.core.security import hash_password
from app.db.model_registry import Business, User, Role, UserRole, AuthSession, RolePermission, now
from app.modules.audit_logs.service import audit
from app.auth.repository import roles_for
from app.shared.errors import BusinessError


def view(db, user):
    return dict(id=user.id, email=user.email, name=user.name, active=user.active,
                version=user.version, role_ids=[r.id for r in roles_for(db, user)])


def validated_roles(db, identity, ids):
    roles = list(db.scalars(select(Role).where(Role.business_id == identity.user.business_id, Role.id.in_(ids))))
    if len(roles) != len(set(ids)):
        raise BusinessError('invalid_role', 'Role does not belong to this business', 422)
    if 'Super Admin' not in identity.roles:
        if any(r.name in {'Super Admin', 'Admin'} for r in roles):
            raise HTTPException(403, 'Only Super Admin may assign administrator roles')
        codes = set(db.scalars(select(RolePermission.permission_code).where(RolePermission.role_id.in_(ids))))
        if not codes <= identity.permissions:
            raise HTTPException(403, 'Cannot assign permissions you do not hold')
    return roles


def create_user(db, identity, payload, request_id):
    validated_roles(db, identity, payload.role_ids)
    user = User(business_id=identity.user.business_id, email=payload.email, name=payload.name,
                password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()
    db.add_all(UserRole(business_id=user.business_id, user_id=user.id, role_id=r) for r in set(payload.role_ids))
    audit(db, user.business_id, identity.user.id, 'users.create', user.id, request_id)
    db.flush()
    return view(db, user)


def update_user(db, identity, user_id, payload, request_id):
    # Serialize membership changes and last-admin checks within the tenant.
    db.scalar(select(Business).where(Business.id == identity.user.business_id).with_for_update())
    user = db.scalar(select(User).where(User.id == user_id, User.business_id == identity.user.business_id).with_for_update())
    if not user:
        raise HTTPException(404, 'User not found')
    if user.version != payload.version:
        raise BusinessError('version_conflict', 'Reload the user before updating')
    old_roles = roles_for(db, user)
    if 'Super Admin' not in identity.roles and any(r.name in {'Super Admin', 'Admin'} for r in old_roles):
        raise HTTPException(403, 'Only Super Admin may modify administrators')
    new_roles = validated_roles(db, identity, payload.role_ids) if payload.role_ids is not None else old_roles
    removing_admin = payload.active is False or not any(r.name == 'Super Admin' for r in new_roles)
    if user.active and any(r.name == 'Super Admin' for r in old_roles) and removing_admin:
        count = db.scalar(select(func.count()).select_from(User).join(UserRole, UserRole.user_id == User.id)
                          .join(Role, Role.id == UserRole.role_id).where(User.business_id == user.business_id,
                           User.active.is_(True), Role.name == 'Super Admin'))
        if count <= 1:
            raise BusinessError('last_admin', 'The last active Super Admin cannot be removed')
    for field in ('name', 'active'):
        value = getattr(payload, field)
        if value is not None:
            setattr(user, field, value)
    if payload.password:
        user.password_hash = hash_password(payload.password)
    if payload.password or payload.active is False:
        db.execute(update(AuthSession).where(AuthSession.user_id == user.id, AuthSession.revoked_at.is_(None)).values(revoked_at=now()))
    if payload.role_ids is not None:
        db.execute(delete(UserRole).where(UserRole.user_id == user.id))
        db.add_all(UserRole(business_id=user.business_id, user_id=user.id, role_id=r.id) for r in new_roles)
    user.version += 1
    audit(db, user.business_id, identity.user.id, 'users.update', user.id, request_id)
    db.flush()
    return view(db, user)
