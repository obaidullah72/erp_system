from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4
import pytest
from pydantic import ValidationError
from sqlalchemy import select, func, text
from sqlalchemy.exc import IntegrityError
from app.core.permissions import ROLE_GRANTS
from app.core.security import hash_password
from app.db.model_registry import (Account, AuthSession, AuditLog, Business, BusinessSettings,
    IdempotencyRecord, JournalEntry, JournalEntryLine, Role, User, UserRole, now)
from app.modules.accounting.posting import post_event
from app.modules.accounting.schemas import PostingEvent, PostingLine
from app.shared.errors import BusinessError
from scripts.bootstrap_admin import bootstrap


def roles(client):
    response = client.get('/api/v1/roles')
    assert response.status_code == 200
    return {r['name']:r for r in response.json()['items']}


def create_viewer(client):
    response = client.post('/api/v1/users', json={'email':'viewer@example.com','name':'Viewer',
        'password':'viewer-password-123','role_ids':[roles(client)['Viewer']['id']]})
    assert response.status_code == 201, response.text
    return response.json()


def test_migrations_bootstrap_roles_and_refusal(seeded):
    sessions, uid, bid = seeded
    with sessions.begin() as db:
        assert set(db.scalars(select(Role.name))) == set(ROLE_GRANTS)
        assert db.scalar(select(func.count()).select_from(User)) == 1
        assert db.scalar(text('SELECT version_num FROM alembic_version')) == '0002_foundation_tables'
        assert db.get(User, uid).password_hash.startswith('$argon2id$')
        with pytest.raises(ValueError, match='already initialized'):
            bootstrap(db, 'another', 'Another', 'another@example.com', 'another-password')


def test_login_permission_denial_and_tenant_boundary(logged_in, seeded):
    client = logged_in
    assert client.get('/api/v1/auth/me').json()['roles'] == ['Super Admin']
    viewer = create_viewer(client)
    response = client.post('/api/v1/auth/login', json={'business':'demo','email':'viewer@example.com','password':'viewer-password-123'})
    client.headers['Authorization'] = 'Bearer ' + response.json()['access_token']
    assert client.get('/api/v1/users').status_code == 403
    assert client.patch('/api/v1/users/'+viewer['id'], json={'version':1,'active':False}).status_code == 403
    assert client.get('/api/v1/business-settings').status_code == 403
    assert client.get('/api/v1/auth/me').status_code == 200
    assert 'password' not in client.get('/api/v1/auth/me').text


def test_refresh_rotation_reuse_and_logout(logged_in):
    client = logged_in
    old_cookie = client.cookies.get('erp_refresh')
    response = client.post('/api/v1/auth/refresh')
    assert response.status_code == 200
    assert client.cookies.get('erp_refresh') != old_cookie
    assert 'httponly' in response.headers['set-cookie'].lower()
    assert 'samesite=strict' in response.headers['set-cookie'].lower()
    client.cookies.clear()
    response = client.post('/api/v1/auth/refresh', headers={'Cookie':f'erp_refresh={old_cookie}'})
    assert response.status_code == 401
    assert client.get('/api/v1/auth/me').status_code == 401
    response = client.post('/api/v1/auth/login', json={'business':'demo','email':'admin@example.com','password':'test-password-123'})
    client.headers['Authorization'] = 'Bearer ' + response.json()['access_token']
    assert client.post('/api/v1/auth/logout').status_code == 204
    assert client.get('/api/v1/auth/me').status_code == 401
    assert client.post('/api/v1/auth/refresh').status_code == 401


def test_expired_session_and_invalid_password(logged_in, seeded):
    sessions, _, _ = seeded
    with sessions.begin() as db:
        for session in db.scalars(select(AuthSession)):
            session.expires_at = now() - timedelta(seconds=1)
    assert logged_in.get('/api/v1/auth/me').status_code == 401
    response = logged_in.post('/api/v1/auth/login', json={'business':'demo','email':'admin@example.com','password':'bad'})
    assert response.status_code == 401
    assert response.json()['error']['message'] == 'Invalid credentials'


def test_settings_versions_csrf_and_last_admin(logged_in, seeded):
    client = logged_in
    response = client.patch('/api/v1/business-settings', json={'version':1,'currency':'USD','timezone':'UTC'})
    assert response.status_code == 200 and response.json()['version'] == 2
    assert client.patch('/api/v1/business-settings', json={'version':1,'currency':'PKR','timezone':'UTC'}).status_code == 409
    assert client.patch('/api/v1/users/'+str(seeded[1]), json={'version':1,'active':False}).json()['error']['code'] == 'last_admin'
    client.headers.pop('X-ERP-CSRF')
    assert client.post('/api/v1/auth/refresh').status_code == 403
    assert client.post('/api/v1/auth/refresh', headers={'X-ERP-CSRF':'1','Origin':'https://evil.example'}).status_code == 403


def test_role_configuration_and_admin_restrictions(logged_in):
    client = logged_in
    catalogue = roles(client)
    assert client.patch('/api/v1/roles/'+catalogue['Super Admin']['id'],json={'version':1,'permissions':[]}).status_code == 409
    assert client.patch('/api/v1/roles/'+catalogue['Viewer']['id'],json={'version':1,'permissions':['sales:post']}).status_code == 422
    response = client.patch('/api/v1/roles/'+catalogue['Accountant']['id'],json={'version':1,'permissions':['accounting:read']})
    assert response.status_code == 200 and response.json()['permissions'] == ['accounting:read']
    created = client.post('/api/v1/users',json={'email':'admin2@example.com','name':'Admin', 'password':'admin-password-123','role_ids':[catalogue['Admin']['id']]})
    assert created.status_code == 201
    token = client.post('/api/v1/auth/login',json={'business':'demo','email':'admin2@example.com','password':'admin-password-123'}).json()['access_token']
    client.headers['Authorization'] = 'Bearer '+token
    assert client.patch('/api/v1/roles/'+catalogue['Accountant']['id'],json={'version':2,'permissions':[]}).status_code == 403
    assert client.post('/api/v1/users',json={'email':'escalated@example.com','name':'Escalation', 'password':'admin-password-123','role_ids':[catalogue['Super Admin']['id']]}).status_code == 403


@pytest.fixture
def posting(seeded):
    sessions, user_id, business_id = seeded
    with sessions.begin() as db:
        cash = Account(business_id=business_id, code='1000', name='Cash', kind='asset')
        equity = Account(business_id=business_id, code='3000', name='Equity', kind='equity')
        db.add_all([cash, equity]); db.flush()
        mappings = {'cash':cash.id,'equity':equity.id}
    event = PostingEvent(business_id=business_id, actor_id=user_id, source_type='opening', source_id='opening-1',
        event='posted', accounting_date=date(2026,1,1), currency='PKR',
        lines=(PostingLine(mapping='cash',debit='100.00'), PostingLine(mapping='equity',credit='100.00')))
    return sessions, event, mappings


def counts(sessions):
    with sessions() as db:
        return tuple(db.scalar(select(func.count()).select_from(t)) for t in (JournalEntry,JournalEntryLine,IdempotencyRecord))


def test_balanced_post_idempotency_duplicate_and_currency_lock(posting, logged_in):
    sessions, event, mappings = posting
    with sessions.begin() as db:
        entry_id = post_event(db,event,mappings,'first')
    with sessions.begin() as db:
        assert post_event(db,event,mappings,'first') == entry_id
        with pytest.raises(BusinessError,match='Source'):
            post_event(db,event,mappings,'second')
        with pytest.raises(BusinessError,match='different request'):
            post_event(db,event.model_copy(update={'source_id':'other'}),mappings,'first')
    assert counts(sessions) == (1,2,1)
    assert logged_in.patch('/api/v1/business-settings',json={'version':1,'currency':'USD','timezone':'UTC'}).status_code == 409


def test_unbalanced_mapping_period_and_rollback(posting):
    sessions, event, mappings = posting
    bad = event.model_copy(update={'lines':(PostingLine(mapping='cash',debit='100'),PostingLine(mapping='equity',credit='99'))})
    class Closed:
        def assert_open(self, *args):
            raise BusinessError('period_closed','Period is closed')
    with sessions.begin() as db:
        for ev, mp, kwargs in ((bad,mappings,{}),(event,{'cash':uuid4(),'equity':mappings['equity']},{}),(event,mappings,{'period_policy':Closed()})):
            with pytest.raises(BusinessError): post_event(db,ev,mp,'invalid',**kwargs)
    assert counts(sessions) == (0,0,0)
    with pytest.raises(RuntimeError,match='later command failed'):
        with sessions.begin() as db:
            post_event(db,event,mappings,'rollback')
            raise RuntimeError('later command failed')
    assert counts(sessions) == (0,0,0)
    with sessions.begin() as db: post_event(db,event,mappings,'rollback')
    assert counts(sessions) == (1,2,1)


def test_database_rejects_unbalanced_and_mutation(posting):
    sessions,event,mappings = posting
    with pytest.raises(IntegrityError):
        with sessions.begin() as db:
            row = JournalEntry(business_id=event.business_id,actor_id=event.actor_id,source_type='direct',source_id='bad',
                               event='posted',accounting_date=event.accounting_date,currency='PKR')
            db.add(row); db.flush()
            db.add(JournalEntryLine(business_id=event.business_id,entry_id=row.id,account_id=mappings['cash'],debit=Decimal('5'),credit=Decimal('0')))
    assert counts(sessions) == (0,0,0)
    with sessions.begin() as db: entry_id=post_event(db,event,mappings,'valid')
    for sql in ('UPDATE journal_entries SET currency=\'USD\'', 'DELETE FROM journal_entry_lines','DELETE FROM audit_logs'):
        with pytest.raises(IntegrityError):
            with sessions.begin() as db: db.execute(text(sql))
    with pytest.raises(IntegrityError):
        with sessions.begin() as db:
            db.add(JournalEntryLine(business_id=event.business_id,entry_id=entry_id,account_id=mappings['cash'],debit=Decimal('1'),credit=Decimal('0')))
    assert counts(sessions) == (1,2,1)


def test_concurrent_duplicate_posting(posting):
    from concurrent.futures import ThreadPoolExecutor
    sessions,event,mappings=posting
    def submit(key):
        try:
            with sessions.begin() as db: return str(post_event(db,event,mappings,key))
        except BusinessError as error: return error.code
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(submit,['a','b']))
    assert results.count('posting_conflict') == 1
    assert counts(sessions) == (1,2,1)


def test_cross_tenant_fk_and_api_isolation(logged_in, seeded):
    sessions,uid,bid=seeded
    with sessions.begin() as db:
        other=Business(slug='other',name='Other');db.add(other);db.flush()
        user=User(business_id=other.id,email='other@example.com',name='Other',password_hash=hash_password('other-password-123'))
        db.add(user);db.flush(); other_uid=user.id
        role_id=db.scalar(select(Role.id).where(Role.business_id==bid).limit(1))
    assert logged_in.patch('/api/v1/users/'+str(other_uid),json={'version':1,'active':False}).status_code == 404
    assert all(u['email']!='other@example.com' for u in logged_in.get('/api/v1/users').json()['items'])
    with pytest.raises(IntegrityError):
        with sessions.begin() as db:
            db.add(UserRole(business_id=bid,user_id=other_uid,role_id=role_id))


def test_decimal_validation():
    for value in (1.1,'NaN','Infinity','-1','0.001'):
        with pytest.raises(ValidationError): PostingLine(mapping='cash',debit=value)
    with pytest.raises(ValidationError): PostingLine(mapping='cash',debit='1',credit='1')


def test_duplicate_user_rolls_back_and_returns_conflict(logged_in):
    viewer = create_viewer(logged_in)
    response = logged_in.post('/api/v1/users',json={'email':viewer['email'],'name':'Duplicate',
                            'password':'duplicate-password','role_ids':[]})
    assert response.status_code == 409
    assert response.json()['error']['code'] == 'constraint_conflict'
    assert logged_in.get('/api/v1/users').json()['total'] == 2


def test_disable_user_revokes_existing_session(logged_in, seeded):
    viewer=create_viewer(logged_in)
    response=logged_in.post('/api/v1/auth/login',json={'business':'demo','email':viewer['email'],'password':'viewer-password-123'})
    viewer_token=response.json()['access_token']
    # The header still holds the administrator access token, irrespective of refresh cookie changes.
    assert logged_in.patch('/api/v1/users/'+viewer['id'],json={'version':1,'active':False}).status_code == 200
    assert logged_in.get('/api/v1/auth/me',headers={'Authorization':'Bearer '+viewer_token}).status_code == 401


def test_same_key_concurrent_replay(posting):
    from concurrent.futures import ThreadPoolExecutor
    sessions,event,mappings=posting
    def submit(_):
        with sessions.begin() as db: return post_event(db,event,mappings,'same-key')
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(submit,range(2)))
    assert results[0] == results[1]
    assert counts(sessions) == (1,2,1)


def test_schema_matches_orm_and_downgrade(database):
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext
    from alembic import command
    from alembic.config import Config
    from app.db.base import Base
    with database.begin() as conn:
        assert compare_metadata(MigrationContext.configure(conn),Base.metadata) == []
        cfg=Config('alembic.ini');cfg.attributes['connection']=conn
        command.downgrade(cfg,'base')
        assert conn.scalar(text("SELECT count(*) FROM information_schema.tables WHERE table_schema=current_schema() AND table_name != 'alembic_version'")) == 0
        command.upgrade(cfg,'head')
