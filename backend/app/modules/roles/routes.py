from uuid import UUID
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy import select, func
from app.auth.dependencies import require
from app.core.permissions import PERMISSIONS
from app.db.model_registry import Role
from app.db.session import get_db
from app.modules.roles.schemas import RoleCreate, RoleUpdate, RoleRead, RolePage
from app.modules.roles.service import view, save

router = APIRouter(prefix='/roles', tags=['Roles'])


@router.get('', response_model=RolePage)
def listing(page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
            identity=Depends(require('roles:read')), db=Depends(get_db, scope='function')):
    clause = Role.business_id == identity.user.business_id
    rows = db.scalars(select(Role).where(clause).order_by(Role.name, Role.id).offset((page-1)*page_size).limit(page_size))
    return dict(items=[view(db, r) for r in rows], total=db.scalar(select(func.count()).select_from(Role).where(clause)),
                page=page, page_size=page_size)


@router.get('/permissions', response_model=list[str])
def permissions(identity=Depends(require('roles:read'))):
    return sorted(PERMISSIONS)


@router.post('', response_model=RoleRead, status_code=201)
def create(payload: RoleCreate, request: Request, identity=Depends(require('roles:create')), db=Depends(get_db, scope='function')):
    return save(db, identity, payload, getattr(request.state, 'request_id', None))


@router.patch('/{role_id}', response_model=RoleRead)
def update(role_id: UUID, payload: RoleUpdate, request: Request, identity=Depends(require('roles:update')), db=Depends(get_db, scope='function')):
    return save(db, identity, payload, getattr(request.state, 'request_id', None), role_id)
