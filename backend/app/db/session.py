from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

_database_url = make_url(get_settings().database_url.get_secret_value())
_connection_options = _database_url.query.get("options", "") + " -c statement_timeout=3000"

# Engine creation is lazy: liveness works even when PostgreSQL is unavailable.
engine = create_engine(
    _database_url, pool_pre_ping=True,
    pool_size=5, max_overflow=5, pool_timeout=3,
    connect_args={"connect_timeout": 3, "options": _connection_options},
    hide_parameters=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    with SessionLocal() as session, session.begin():
        yield session
