"""Comportamiento del indice parcial unico rn05_un_activo_por_dia (C-21).

- Dos turnos activos mismo paciente mismo dia -> viola indice.
- Dos turnos activos mismo paciente dias distintos -> persisten.
- Turno cancelado + turno activo mismo dia -> se permite (WHERE estado='activo').
- Token repetido -> viola unicidad.
"""
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

from app.core.config import get_database_url
from app.domain.models import Base

BACKEND = Path(__file__).resolve().parents[1]

# Importar alembic sin que backend/alembic sombre al paquete instalado.
_sys_path_previo = list(sys.path)
sys.path[:] = [
    p for p in sys.path if Path(p or ".").resolve() != BACKEND
]
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
sys.path[:] = _sys_path_previo


def _alembic_config() -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "alembic"))
    return cfg


def _limpiar(engine) -> None:
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))


@pytest.fixture
def conn():
    engine = create_engine(get_database_url())
    _limpiar(engine)
    command.upgrade(_alembic_config(), "head")
    with engine.connect() as connection:
        yield connection
    _limpiar(engine)
    engine.dispose()


def _crear_catalogo(conn) -> dict[str, uuid.UUID]:
    ids = {k: uuid.uuid4() for k in ("p", "s", "pr", "pa")}
    conn.execute(
        text("INSERT INTO profesional (id, nombre, apellido) VALUES (:id, 'Ana', 'Demo')"),
        {"id": ids["p"]},
    )
    conn.execute(
        text("INSERT INTO sillon (id, nombre) VALUES (:id, 'Sillon Demo')"),
        {"id": ids["s"]},
    )
    conn.execute(
        text("INSERT INTO prestacion (id, nombre, duracion_min) VALUES (:id, 'Consulta Demo', 30)"),
        {"id": ids["pr"]},
    )
    conn.execute(
        text("INSERT INTO paciente_guest (id, nombre, telefono) VALUES (:id, 'Paciente Demo', '11-0000-0000')"),
        {"id": ids["pa"]},
    )
    return ids


def _insertar_turno(conn, ids, inicio, fin, estado="activo", token=None):
    turno_id = uuid.uuid4()
    conn.execute(
        text(
            "INSERT INTO turno "
            "(id, profesional_id, sillon_id, prestacion_id, paciente_id, inicio, fin, estado, token_cancelacion) "
            "VALUES (:id, :p, :s, :pr, :pa, :inicio, :fin, :estado, :token)"
        ),
        {
            "id": turno_id,
            "p": ids["p"],
            "s": ids["s"],
            "pr": ids["pr"],
            "pa": ids["pa"],
            "inicio": inicio,
            "fin": fin,
            "estado": estado,
            "token": token,
        },
    )
    return turno_id


def test_dos_turnos_activos_mismo_paciente_mismo_dia_violan_rn05(conn):
    ids = _crear_catalogo(conn)
    base = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    _insertar_turno(conn, ids, base, base + timedelta(minutes=30))

    with pytest.raises(IntegrityError):
        _insertar_turno(
            conn, ids,
            base + timedelta(minutes=45),
            base + timedelta(minutes=75),
        )
    conn.rollback()


def test_dos_turnos_activos_mismo_paciente_dias_distintos_persisten(conn):
    ids = _crear_catalogo(conn)
    base = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    _insertar_turno(conn, ids, base, base + timedelta(minutes=30))
    _insertar_turno(
        conn, ids,
        base + timedelta(days=1),
        base + timedelta(days=1, minutes=30),
    )
    total = conn.execute(text("SELECT count(*) FROM turno")).scalar_one()
    assert total == 2


def test_turno_cancelado_no_bloquea_turno_activo_mismo_dia(conn):
    ids = _crear_catalogo(conn)
    base = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    _insertar_turno(conn, ids, base, base + timedelta(minutes=30), estado="cancelado")
    _insertar_turno(conn, ids, base + timedelta(minutes=45), base + timedelta(minutes=75))
    total = conn.execute(text("SELECT count(*) FROM turno")).scalar_one()
    assert total == 2


def test_token_repetido_viola_unicidad(conn):
    ids = _crear_catalogo(conn)
    base = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    _insertar_turno(conn, ids, base, base + timedelta(minutes=30), token="TOK-001")

    with pytest.raises(IntegrityError):
        _insertar_turno(
            conn, ids,
            base + timedelta(hours=1),
            base + timedelta(hours=1, minutes=30),
            token="TOK-001",
        )
    conn.rollback()
