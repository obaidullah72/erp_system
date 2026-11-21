from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

# Engine creation is lazy: liveness works even when PostgreSQL is unavailable.
engine = create_engine(
    get_settings().database_url.get_secret_value(), pool_pre_ping=True,
    pool_size=5, max_overflow=5, pool_timeout=3,
    connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
    hide_parameters=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    with SessionLocal() as session, session.begin():
        yield session
