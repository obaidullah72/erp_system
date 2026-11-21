from uuid import UUID
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select, func
from app.auth.dependencies import require
from app.db.session import get_db
from app.db.model_registry import User
from app.modules.users.schemas import UserCreate, UserUpdate, UserRead, UserPage
from app.modules.users.service import create_user, update_user, view

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('', response_model=UserPage)
def list_users(page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100),
               q: str = Query('', max_length=100), active: bool | None = None,
               identity=Depends(require('users:read')), db=Depends(get_db, scope='function')):
    filters = [User.business_id == identity.user.business_id]
    if q:
        filters.append(User.email.contains(q.lower(), autoescape=True))
    if active is not None:
        filters.append(User.active == active)
    users = db.scalars(select(User).where(*filters).order_by(User.email, User.id).offset((page-1)*page_size).limit(page_size))
    return dict(items=[view(db, u) for u in users], total=db.scalar(select(func.count()).select_from(User).where(*filters)),
                page=page, page_size=page_size)


@router.post('', response_model=UserRead, status_code=201)
def create(payload: UserCreate, request: Request, identity=Depends(require('users:create')), db=Depends(get_db, scope='function')):
    return create_user(db, identity, payload, getattr(request.state, 'request_id', None))


@router.patch('/{user_id}', response_model=UserRead)
def update(user_id: UUID, payload: UserUpdate, request: Request, identity=Depends(require('users:update')), db=Depends(get_db, scope='function')):
    return update_user(db, identity, user_id, payload, getattr(request.state, 'request_id', None))
