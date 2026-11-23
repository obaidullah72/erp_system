"""Never load developer credentials. Integration tests use unique throwaway schemas."""
import os
os.environ['ENVIRONMENT'] = 'test'
os.environ['JWT_SECRET_KEY'] = 'isolated-test-signing-key-never-use-in-deployment'
os.environ['DATABASE_URL'] = os.environ.get('ERP_TEST_DATABASE_URL', 'postgresql+psycopg://erp_test@127.0.0.1:1/erp_test')

from uuid import uuid4
from pathlib import Path
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.db.session import get_db
from app.main import create_app
from app.core.middleware import RequestLoggingMiddleware
from scripts.bootstrap_admin import bootstrap


@pytest.fixture
def database():
    url = os.environ.get('ERP_TEST_DATABASE_URL')
    if not url:
        pytest.skip('Set ERP_TEST_DATABASE_URL to run real PostgreSQL integration checks')
    if not (make_url(url).database or '').endswith('_test'):
        pytest.fail('Integration database name must end in _test')
    schema = 'test_' + uuid4().hex
    admin = create_engine(url)
    with admin.begin() as conn:
        conn.execute(text(f'CREATE SCHEMA {schema}'))
    engine = create_engine(url, connect_args={'options': f'-csearch_path={schema}'}, hide_parameters=True)
    try:
        with engine.begin() as conn:
            cfg = Config(str(Path(__file__).parents[1] / 'alembic.ini'))
            cfg.set_main_option('script_location', str(Path(__file__).parents[1] / 'migrations'))
            cfg.attributes['connection'] = conn
            command.upgrade(cfg, 'head')
        yield engine
    finally:
        engine.dispose()
        with admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA {schema} CASCADE'))
        admin.dispose()


@pytest.fixture
def seeded(database):
    sessions = sessionmaker(database, expire_on_commit=False, autoflush=False)
    with sessions.begin() as db:
        user = bootstrap(db, 'demo', 'Test business', 'admin@example.com', 'test-password-123')
        user_id, business_id = user.id, user.business_id
    return sessions, user_id, business_id


@pytest.fixture
def client(seeded):
    sessions, _, _ = seeded
    application = create_app()
    def override():
        with sessions.begin() as db:
            yield db
    application.dependency_overrides[get_db] = override
    with TestClient(RequestLoggingMiddleware(application), raise_server_exceptions=False) as client:
        client.headers['X-ERP-CSRF'] = '1'
        yield client


@pytest.fixture
def logged_in(client):
    response = client.post('/api/v1/auth/login', json={'business':'demo', 'email':'ADMIN@example.com', 'password':'test-password-123'})
    assert response.status_code == 200, response.text
    client.headers['Authorization'] = 'Bearer ' + response.json()['access_token']
    return client
