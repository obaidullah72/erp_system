from sqlalchemy import select
from app.db.model_registry import Role, RolePermission, UserRole


def roles_for(db, user):
    return list(db.scalars(select(Role).join(UserRole, UserRole.role_id == Role.id).where(
        UserRole.user_id == user.id, UserRole.business_id == user.business_id)))


def permissions_for(db, user):
    return set(db.scalars(select(RolePermission.permission_code).join(
        UserRole, UserRole.role_id == RolePermission.role_id).where(
        UserRole.user_id == user.id, UserRole.business_id == user.business_id)))
