import asyncio
import logging
import os
import sys

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from alembic import context
from alembic.environment import MigrationContext
from alembic.operations import MigrationScript
from dotenv import load_dotenv
from sqlalchemy import URL, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.sql.schema import MetaData


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path = [str(BASE_DIR), str(BASE_DIR / "app"), *sys.path[1:]]

from common.models import Base  # noqa: E402


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5.5s [%(name)s] %(message)s",
)
logger = logging.getLogger("alembic.runtime.migration")

config = context.config

target_metadata: MetaData = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def process_revision_directives(
    _context: MigrationContext,
    _revision: str | Iterable[str | None] | Iterable[str],
    directives: list[MigrationScript],
) -> None:
    if config.cmd_opts is None or not getattr(config.cmd_opts, "autogenerate", False):
        return

    if getattr(config.cmd_opts, "autogenerate", False):
        script = directives[0]
        if script.upgrade_ops is None:
            return
        if script.upgrade_ops.is_empty():
            directives[:] = []
            logger.info("No changes detected, skip create migration")


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configuration: dict[str, Any] = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = build_async_url()

    connectable = async_engine_from_config(
        configuration,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


def build_async_url() -> URL:
    username = os.environ["DATABASE_USERNAME"]
    password = os.environ["DATABASE_PASSWORD"]
    host = os.environ["DATABASE_HOST"]
    port = os.environ["DATABASE_PORT"]
    name = os.environ["DATABASE_NAME"]
    return URL.create(
        "postgresql+asyncpg", username=username, password=password, host=host, port=int(port), database=name
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
