"""Fixtures contra Postgres 16 real. NUNCA SQLite (hard rule)."""
import os

os.environ.setdefault("API_KEY_RECEPCION", "test-recepcion-key")
os.environ.setdefault("API_KEY_ODONTOLOGO", "test-odonto-key")
os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://turnos:turnos@localhost:5432/turnos"
)
os.environ.setdefault("TZ_CONSULTORIO", "America/Argentina/Buenos_Aires")
os.environ.setdefault("NOTIF_BACKEND", "mock")
os.environ.setdefault("RESERVA_RATE_LIMIT", "1000/minute")

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_database_url, get_tz_consultorio
from app.db import get_session
from app.domain.models import (
    Base,
    HorarioAtencion,
    Prestacion,
    Profesional,
    Sillon,
)


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(get_database_url(), pool_pre_ping=True)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_engine):
    from app.main import create_app

    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_session():
        async with factory() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def _reset_rate_limit():
    from app.api.v1 import reservas as reservas_router

    reservas_router.reset_rate_limit()
    yield
    reservas_router.reset_rate_limit()


@pytest_asyncio.fixture
async def seed_catalog(db_engine):
    """2 profesionales, 2 sillones, 3 prestaciones 30/45/90, horario Lun-Vie 9-18 + Sab 9-12."""
    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with factory() as session:
        p1 = Profesional(nombre="Ana", apellido="Demo", matricula="MAT-001")
        p2 = Profesional(nombre="Bruno", apellido="Demo", matricula="MAT-002")
        s1 = Sillon(nombre="Sillon 1")
        s2 = Sillon(nombre="Sillon 2")
        c30 = Prestacion(nombre="Consulta Demo", duracion_min=30)
        o45 = Prestacion(nombre="Obturacion Demo", duracion_min=45)
        e90 = Prestacion(nombre="Endodoncia Demo", duracion_min=90)
        session.add_all([p1, p2, s1, s2, c30, o45, e90])
        await session.flush()
        session.add_all(
            [
                HorarioAtencion(
                    profesional_id=None, dia_semana=d,
                    hora_desde=time(9, 0), hora_hasta=time(18, 0),
                )
                for d in range(0, 5)
            ]
            + [
                HorarioAtencion(
                    profesional_id=None, dia_semana=5,
                    hora_desde=time(9, 0), hora_hasta=time(12, 0),
                )
            ]
        )
        await session.commit()
        ids = {
            "p1": p1.id, "p2": p2.id, "s1": s1.id, "s2": s2.id,
            "c30": c30.id, "o45": o45.id, "e90": e90.id,
        }
    return ids


def proximo_dia_habil(hora: int = 10, minuto: int = 0) -> datetime:
    """Proximo Lun-Vie futuro a la hora dada, aware en TZ consultorio."""
    tz = ZoneInfo(get_tz_consultorio())
    base = datetime.now(tz).replace(microsecond=0) + timedelta(days=1)
    while base.weekday() > 4:
        base += timedelta(days=1)
    return base.replace(hour=hora, minute=minuto, second=0)


@pytest.fixture
def headers_recepcion():
    return {"X-API-Key": "test-recepcion-key"}


@pytest.fixture
def headers_odonto():
    return {"X-API-Key": "test-odonto-key"}
