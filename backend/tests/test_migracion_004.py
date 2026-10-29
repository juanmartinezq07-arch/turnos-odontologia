"""Test de la migracion 004: cancelled_at + idx_turno_paciente_fecha (C-20)."""
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect, text

from app.core.config import get_database_url
from app.domain.models import Base

BACKEND = Path(__file__).resolve().parents[1]

# `backend/alembic/` es el directorio de migraciones y sombrea al paquete
# instalado cuando el cwd es `backend/`. Se importa el paquete real sin
# `backend` en sys.path y luego se restaura para el resto del proyecto.
_sys_path_previo = list(sys.path)
sys.path[:] = [
    p for p in sys.path if Path(p or ".").resolve() != BACKEND
]
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402

sys.path[:] = _sys_path_previo

REVISION_003 = "003_recorte_alcance_c01"
CONSTRAINTS_RN02 = {
    "rn02_profesional",
    "rn02_sillon",
    "ck_turno_fin_mayor_inicio",
}


def _alembic_config() -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "alembic"))
    return cfg


def _limpiar(engine) -> None:
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))


def _constraints(engine) -> set[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT conname FROM pg_constraint "
                "WHERE conrelid = 'turno'::regclass"
            )
        ).scalars().all()
    return set(rows)


@pytest.fixture
def engine_migrado():
    engine = create_engine(get_database_url())
    _limpiar(engine)
    command.upgrade(_alembic_config(), "head")
    yield engine
    _limpiar(engine)
    engine.dispose()


def test_004_agrega_cancelled_at_nullable(engine_migrado):
    columnas = {
        c["name"]: c for c in inspect(engine_migrado).get_columns("turno")
    }

    assert "cancelled_at" in columnas
    assert columnas["cancelled_at"]["nullable"] is True
    assert columnas["cancelled_at"]["type"].timezone is True


def test_004_crea_indice_paciente_fecha(engine_migrado):
    indices = {
        i["name"]: i for i in inspect(engine_migrado).get_indexes("turno")
    }

    assert "idx_turno_paciente_fecha" in indices
    assert indices["idx_turno_paciente_fecha"]["column_names"] == [
        "paciente_id",
        "inicio",
    ]


def test_004_preserva_invariantes_rn02(engine_migrado):
    assert CONSTRAINTS_RN02 <= _constraints(engine_migrado)


def test_004_downgrade_reversible(engine_migrado):
    command.downgrade(_alembic_config(), REVISION_003)

    columnas = {c["name"] for c in inspect(engine_migrado).get_columns("turno")}
    indices = {i["name"] for i in inspect(engine_migrado).get_indexes("turno")}

    assert "cancelled_at" not in columnas
    assert "idx_turno_paciente_fecha" not in indices
    assert CONSTRAINTS_RN02 <= _constraints(engine_migrado)


def test_turno_activo_no_tiene_cancelled_at(engine_migrado):
    inicio = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    with engine_migrado.begin() as conn:
        ids = _crear_catalogo(conn)
        turno_id = _insertar_turno(
            conn, ids, inicio, inicio + timedelta(minutes=30)
        )
        cancelled_at = conn.execute(
            text("SELECT cancelled_at FROM turno WHERE id = :id"),
            {"id": turno_id},
        ).scalar_one()

    assert cancelled_at is None


def test_mismo_paciente_en_fechas_distintas_persiste(engine_migrado):
    base = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    with engine_migrado.begin() as conn:
        ids = _crear_catalogo(conn)
        _insertar_turno(conn, ids, base, base + timedelta(minutes=30))
        _insertar_turno(
            conn,
            ids,
            base + timedelta(days=1),
            base + timedelta(days=1, minutes=30),
        )
        total = conn.execute(text("SELECT count(*) FROM turno")).scalar_one()

    assert total == 2


def _crear_catalogo(conn) -> dict[str, uuid.UUID]:
    ids = {k: uuid.uuid4() for k in ("p", "s", "pr", "pa")}
    conn.execute(
        text(
            "INSERT INTO profesional (id, nombre, apellido) "
            "VALUES (:id, 'Ana', 'Demo')"
        ),
        {"id": ids["p"]},
    )
    conn.execute(
        text("INSERT INTO sillon (id, nombre) VALUES (:id, 'Sillon Demo')"),
        {"id": ids["s"]},
    )
    conn.execute(
        text(
            "INSERT INTO prestacion (id, nombre, duracion_min) "
            "VALUES (:id, 'Consulta Demo', 30)"
        ),
        {"id": ids["pr"]},
    )
    conn.execute(
        text(
            "INSERT INTO paciente_guest (id, nombre, telefono) "
            "VALUES (:id, 'Paciente Demo', '11-0000-0000')"
        ),
        {"id": ids["pa"]},
    )
    return ids


def _insertar_turno(
    conn, ids: dict[str, uuid.UUID], inicio: datetime, fin: datetime
) -> uuid.UUID:
    turno_id = uuid.uuid4()
    conn.execute(
        text(
            "INSERT INTO turno "
            "(id, profesional_id, sillon_id, prestacion_id, paciente_id, inicio, fin) "
            "VALUES (:id, :p, :s, :pr, :pa, :inicio, :fin)"
        ),
        {
            "id": turno_id,
            "p": ids["p"],
            "s": ids["s"],
            "pr": ids["pr"],
            "pa": ids["pa"],
            "inicio": inicio,
            "fin": fin,
        },
    )
    return turno_id
