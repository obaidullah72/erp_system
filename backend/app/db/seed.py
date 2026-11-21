from sqlalchemy import select
from app.core.permissions import PERMISSIONS, ROLE_GRANTS
from app.db.model_registry import Permission, Role, RolePermission


def seed_roles(db, business_id):
    """Caller owns transaction; repeatable on a business without resetting custom grants."""
    existing = set(db.scalars(select(Permission.code)))
    db.add_all(Permission(code=code) for code in sorted(PERMISSIONS - existing))
    db.flush()
    roles = {r.name: r for r in db.scalars(select(Role).where(Role.business_id == business_id))}
    for name, codes in ROLE_GRANTS.items():
        if name in roles:
            continue
        role = Role(business_id=business_id, name=name, system=True)
        db.add(role)
        db.flush()
        db.add_all(RolePermission(role_id=role.id, permission_code=code) for code in sorted(codes))
        roles[name] = role
    db.flush()
    return roles
