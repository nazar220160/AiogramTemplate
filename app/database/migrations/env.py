import asyncio
from logging.config import fileConfig
from typing import no_type_check

import nest_asyncio
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from app.database import models
from app.core import load_settings

target_metadata = models.Base.metadata

config = context.config  # type: ignore
config.set_main_option('sqlalchemy.url', load_settings().db_url)

fileConfig(config.config_file_name)


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_server_default=True,
        render_as_batch=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


@no_type_check
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_server_default=True,
        compare_type=True,
        render_as_batch=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",  # noqa
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(run_migrations_online())
