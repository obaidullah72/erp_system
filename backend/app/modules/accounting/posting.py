"""Internal kernel. Callers authorize a source command and own the outer transaction."""
import hashlib
import json
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.model_registry import (Account, BusinessSettings, IdempotencyRecord, JournalEntry,
                                   JournalEntryLine, User)
from app.modules.accounting.schemas import PostingEvent
from app.modules.accounting.periods import OpenPeriodPolicy
from app.modules.audit_logs.service import audit
from app.shared.errors import BusinessError


def post_event(db, event: PostingEvent, mappings: dict[str, UUID], idempotency_key: str,
               *, period_policy=None, request_id=None) -> UUID:
    if not db.in_transaction():
        raise RuntimeError('Posting requires a caller-owned transaction')
    if not isinstance(event, PostingEvent):
        raise TypeError('Use the validated PostingEvent contract')
    if not isinstance(idempotency_key, str) or not 1 <= len(idempotency_key) <= 128:
        raise BusinessError('invalid_idempotency_key', 'An idempotency key of 1–128 characters is required', 422)
    if sum(line.debit for line in event.lines) != sum(line.credit for line in event.lines):
        raise BusinessError('unbalanced_journal', 'Journal debits and credits must balance', 422)
    if set(mappings) != {line.mapping for line in event.lines}:
        raise BusinessError('invalid_mapping', 'Mappings must exactly cover the event lines', 422)
    canonical = event.model_dump(mode='json')
    # Canonical Decimal formatting makes 10.0 and 10.00 the same request.
    for row in canonical['lines']:
        row['debit'] = format(Decimal(row['debit']), '.2f')
        row['credit'] = format(Decimal(row['credit']), '.2f')
    digest = hashlib.sha256(json.dumps({'event': canonical, 'mappings': {k: str(v) for k,v in mappings.items()}},
                                      sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    try:
        with db.begin_nested():
            settings = db.scalar(select(BusinessSettings).where(BusinessSettings.business_id == event.business_id).with_for_update())
            if not settings:
                raise BusinessError('invalid_business', 'Business settings are required', 422)
            existing = db.scalar(select(IdempotencyRecord).where(IdempotencyRecord.business_id == event.business_id,
                                 IdempotencyRecord.operation == 'journal.post', IdempotencyRecord.key == idempotency_key))
            if existing:
                if existing.request_hash != digest:
                    raise BusinessError('idempotency_conflict', 'Key was already used for a different request')
                return existing.result_id
            if settings.currency != event.currency:
                raise BusinessError('currency_mismatch', 'Posting currency must match business base currency', 422)
            if not db.scalar(select(User.id).where(User.id == event.actor_id, User.business_id == event.business_id, User.active.is_(True))):
                raise BusinessError('invalid_actor', 'Active same-business actor required', 422)
            accounts = list(db.scalars(select(Account).where(Account.id.in_(set(mappings.values())),
                            Account.business_id == event.business_id, Account.active.is_(True)).with_for_update()))
            if len(accounts) != len(set(mappings.values())):
                raise BusinessError('invalid_mapping', 'Mappings require active same-business accounts', 422)
            (period_policy or OpenPeriodPolicy()).assert_open(db, event.business_id, event.accounting_date)
            entry = JournalEntry(business_id=event.business_id, actor_id=event.actor_id, source_type=event.source_type,
                                 source_id=event.source_id, event=event.event, accounting_date=event.accounting_date, currency=event.currency)
            db.add(entry)
            db.flush()
            db.add_all(JournalEntryLine(business_id=event.business_id, entry_id=entry.id, account_id=mappings[line.mapping],
                                       debit=line.debit, credit=line.credit) for line in event.lines)
            db.add(IdempotencyRecord(business_id=event.business_id, operation='journal.post', key=idempotency_key,
                                     request_hash=digest, result_id=entry.id))
            audit(db, event.business_id, event.actor_id, 'journal.post', entry.id, request_id)
            db.flush()
            return entry.id
    except IntegrityError:
        raise BusinessError('posting_conflict', 'Source has already been posted or violates a posting constraint') from None
