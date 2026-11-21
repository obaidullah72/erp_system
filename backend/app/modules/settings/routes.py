from fastapi import APIRouter, Depends, Request
from app.auth.dependencies import require
from app.db.model_registry import BusinessSettings
from app.db.session import get_db
from app.modules.settings.schemas import SettingsRead, SettingsUpdate
from app.modules.settings.service import update_settings

router = APIRouter(prefix='/business-settings', tags=['Business settings'])


@router.get('', response_model=SettingsRead)
def read(identity=Depends(require('settings:read')), db=Depends(get_db, scope='function')):
    return db.get(BusinessSettings, identity.user.business_id)


@router.patch('', response_model=SettingsRead)
def update(payload: SettingsUpdate, request: Request, identity=Depends(require('settings:update')), db=Depends(get_db, scope='function')):
    return update_settings(db, identity, payload, getattr(request.state, 'request_id', None))
