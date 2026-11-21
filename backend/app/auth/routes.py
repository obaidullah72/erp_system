from fastapi import APIRouter, Depends, Request, Response, HTTPException
from app.auth.dependencies import current_identity
from app.auth.schemas import CurrentUser, LoginRequest, TokenResponse
from app.auth.service import login, refresh, user_view
from app.core.config import get_settings
from app.core.exceptions import error_response
from app.db.session import get_db
from app.db.model_registry import now
from app.modules.audit_logs.service import audit

router = APIRouter(prefix='/auth', tags=['Authentication'])
COOKIE = 'erp_refresh'
COOKIE_PATH = '/api/v1/auth'


def check_origin(request):
    # Cookie-authenticated commands require a custom header and exact allowed Origin.
    if request.headers.get('X-ERP-CSRF') != '1':
        raise HTTPException(403, 'CSRF header required')
    origin = request.headers.get('origin')
    if origin and origin not in get_settings().cors_origins:
        raise HTTPException(403, 'Origin not allowed')


def set_cookie(response, value):
    response.headers['Cache-Control'] = 'no-store'
    response.set_cookie(COOKIE, value, httponly=True, secure=get_settings().environment == 'production',
                        samesite='strict', path=COOKIE_PATH, max_age=get_settings().refresh_token_days * 86400)


@router.post('/login', response_model=TokenResponse)
def login_route(payload: LoginRequest, request: Request, response: Response, db=Depends(get_db, scope='function')):
    check_origin(request)
    body, cookie = login(db, payload, getattr(request.state, 'request_id', None))
    set_cookie(response, cookie)
    return body


@router.post('/refresh', response_model=TokenResponse)
def refresh_route(request: Request, response: Response, db=Depends(get_db, scope='function')):
    check_origin(request)
    result = refresh(db, request.cookies.get(COOKIE), getattr(request.state, 'request_id', None))
    if result is None:
        error = error_response(request, 401, 'session_expired', 'Session expired; sign in again')
        error.delete_cookie(COOKIE, path=COOKIE_PATH)
        error.headers['Cache-Control'] = 'no-store'
        return error
    body, cookie = result
    set_cookie(response, cookie)
    return body


@router.post('/logout', status_code=204)
def logout_route(request: Request, identity=Depends(current_identity), db=Depends(get_db, scope='function')):
    check_origin(request)
    identity.session.revoked_at = now()
    audit(db, identity.user.business_id, identity.user.id, 'auth.logout', identity.session.id,
          getattr(request.state, 'request_id', None))
    response = Response(status_code=204, headers={'Cache-Control': 'no-store'})
    response.delete_cookie(COOKIE, path=COOKIE_PATH)
    return response


@router.get('/me', response_model=CurrentUser)
def me(response: Response, identity=Depends(current_identity), db=Depends(get_db, scope='function')):
    response.headers['Cache-Control'] = 'no-store'
    return user_view(db, identity.user)
