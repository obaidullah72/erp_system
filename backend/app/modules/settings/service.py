from sqlalchemy import select
from app.db.model_registry import BusinessSettings, JournalEntry
from app.modules.audit_logs.service import audit
from app.shared.errors import BusinessError


def update_settings(db, identity, payload, request_id):
    settings = db.scalar(select(BusinessSettings).where(BusinessSettings.business_id == identity.user.business_id).with_for_update())
    if settings.version != payload.version:
        raise BusinessError('version_conflict', 'Reload settings before updating')
    if settings.currency != payload.currency and db.scalar(select(JournalEntry.id).where(JournalEntry.business_id == settings.business_id).limit(1)):
        raise BusinessError('currency_locked', 'Base currency cannot change after posting')
    settings.currency, settings.timezone = payload.currency, payload.timezone
    settings.version += 1
    audit(db, settings.business_id, identity.user.id, 'settings.update', settings.business_id, request_id)
    db.flush()
    return settings
