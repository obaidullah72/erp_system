from alembic import context
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

import app.db.model_registry  # noqa: F401 — register only concrete foundation models
target_metadata = Base.metadata

if context.is_offline_mode():
    context.configure(url=get_settings().database_url.get_secret_value(), target_metadata=target_metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"}, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    def migrate(connection):
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
    supplied = context.config.attributes.get('connection')
    if supplied is not None:
        migrate(supplied)
    else:
        with engine.connect() as connection:
            migrate(connection)
        engine.dispose()
