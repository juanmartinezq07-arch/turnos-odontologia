"""Alembic sync (psycopg). Migraciones 001 tablas, 002 EXCLUDE, 003 recorte."""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# backend/.env (misma regla que app/core/config.py: no pisa la shell).
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.domain.models import Base

config = context.config
config.set_main_option(
    "sqlalchemy.url",
    os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://turnos:turnos@localhost:5432/turnos",
    ),
)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
