import os
import pytest
from sqlalchemy import create_engine, text


def test_real_postgres_connectivity():
    url = os.environ.get("ERP_TEST_DATABASE_URL")
    if not url:
        pytest.skip("ERP_TEST_DATABASE_URL not set; no real PostgreSQL integration configured")
    engine = create_engine(url, connect_args={"connect_timeout": 3})
    try:
        with engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        engine.dispose()
