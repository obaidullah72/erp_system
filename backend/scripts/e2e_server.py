"""Isolated browser-test API; creates/drops only a random test schema."""
import os
import sys
from pathlib import Path
from uuid import uuid4
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

url = os.environ.get('ERP_TEST_DATABASE_URL')
if not url or not (make_url(url).database or '').endswith('_test'):
    raise SystemExit('ERP_TEST_DATABASE_URL must name a dedicated *_test database')
schema = 'e2e_' + uuid4().hex
admin = create_engine(url)
with admin.begin() as conn:
    conn.execute(text(f'CREATE SCHEMA {schema}'))
os.environ['DATABASE_URL'] = make_url(url).update_query_dict({'options':f'-csearch_path={schema}'}).render_as_string(hide_password=False)
os.environ['JWT_SECRET_KEY'] = 'browser-test-only-signing-key-not-for-real-use'
os.environ['ENVIRONMENT'] = 'test'
os.environ['CORS_ORIGINS'] = '["http://127.0.0.1:5174","http://localhost:5174"]'
try:
    from alembic import command
    from alembic.config import Config
    from app.db.session import engine, SessionLocal
    from scripts.bootstrap_admin import bootstrap
    cfg = Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini'))
    cfg.set_main_option('script_location', str(Path(__file__).resolve().parents[1] / 'migrations'))
    with engine.begin() as connection:
        cfg.attributes['connection'] = connection
        command.upgrade(cfg, 'head')
    with SessionLocal.begin() as db:
        bootstrap(db, 'demo', 'Browser test', 'admin@example.com', 'browser-test-password')
    import uvicorn
    uvicorn.run('app.main:app', host='127.0.0.1', port=8001, access_log=False)
finally:
    with admin.begin() as conn:
        conn.execute(text(f'DROP SCHEMA {schema} CASCADE'))
    admin.dispose()
