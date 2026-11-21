from fastapi import HTTPException
from sqlalchemy import select, delete
from app.core.permissions import PERMISSIONS, ROLE_GRANTS
from app.db.model_registry import Role, RolePermission
from app.modules.audit_logs.service import audit
from app.shared.errors import BusinessError


def view(db, role):
    return dict(id=role.id, name=role.name, system=role.system, version=role.version,
                permissions=sorted(db.scalars(select(RolePermission.permission_code).where(RolePermission.role_id == role.id))))


def save(db, identity, payload, request_id, role_id=None):
    if 'Super Admin' not in identity.roles:
        raise HTTPException(403, 'Only Super Admin may configure roles')
    codes = set(payload.permissions)
    if not codes <= PERMISSIONS:
        raise BusinessError('invalid_permission', 'Unknown module/action permission', 422)
    if role_id:
        role = db.scalar(select(Role).where(Role.id == role_id, Role.business_id == identity.user.business_id).with_for_update())
        if not role:
            raise HTTPException(404, 'Role not found')
        if role.name in {'Super Admin', 'Admin'}:
            raise BusinessError('protected_role', 'Administrator grants are protected')
        if role.name == 'Viewer' and any(not p.endswith(':read') for p in codes):
            raise BusinessError('read_only_role', 'Viewer must remain read-only', 422)
        # Responsibility roles cannot become administrators under an innocuous name.
        if any(p.split(':')[0] in {'users', 'roles', 'settings'} and not p.endswith(':read') for p in codes):
            raise BusinessError('restricted_grant', 'Administrative writes belong to administrator roles', 422)
        if role.version != payload.version:
            raise BusinessError('version_conflict', 'Reload the role before updating')
        role.version += 1
        db.execute(delete(RolePermission).where(RolePermission.role_id == role.id))
    else:
        if payload.name in ROLE_GRANTS:
            raise BusinessError('reserved_role', 'This role name is reserved')
        if any(p.split(':')[0] in {'users', 'roles', 'settings'} and not p.endswith(':read') for p in codes):
            raise BusinessError('restricted_grant', 'Administrative writes belong to administrator roles', 422)
        role = Role(business_id=identity.user.business_id, name=payload.name)
        db.add(role)
        db.flush()
    db.add_all(RolePermission(role_id=role.id, permission_code=code) for code in codes)
    audit(db, role.business_id, identity.user.id, 'roles.update' if role_id else 'roles.create', role.id, request_id)
    db.flush()
    return view(db, role)
