from fastapi import APIRouter
from app.api.v1.health import router as health_router

router = APIRouter(prefix="/api/v1")
router.include_router(health_router)

from app.auth.routes import router as auth_router
from app.modules.users.routes import router as users_router
from app.modules.roles.routes import router as roles_router
from app.modules.settings.routes import router as settings_router
for module in (auth_router, users_router, roles_router, settings_router):
    router.include_router(module)
