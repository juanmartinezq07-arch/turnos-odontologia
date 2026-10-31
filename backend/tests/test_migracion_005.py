"""Test de la migracion 005: token_cancelacion UNIQUE + indice parcial rn05_un_activo_por_dia (C-21)."""
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

REVISION_004 = "004_cancelled_at_paciente_fecha"
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


def _indices(engine) -> set[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT indexname FROM pg_indexes "
                "WHERE tablename = 'turno'"
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


def test_005_agrega_token_cancelacion_nullable_unique(engine_migrado):
    columnas = {
        c["name"]: c for c in inspect(engine_migrado).get_columns("turno")
    }

    assert "token_cancelacion" in columnas
    assert columnas["token_cancelacion"]["nullable"] is True
    assert columnas["token_cancelacion"]["type"].python_type is str or \
        str(columnas["token_cancelacion"]["type"]).startswith("VARCHAR") or \
        str(columnas["token_cancelacion"]["type"]).startswith("TEXT")


def test_005_crea_indice_unico_parcial_rn05(engine_migrado):
    indices = _indices(engine_migrado)
    assert "rn05_un_activo_por_dia" in indices


def test_005_preserva_invariantes_rn02(engine_migrado):
    assert CONSTRAINTS_RN02 <= _constraints(engine_migrado)


def test_005_downgrade_reversible(engine_migrado):
    command.downgrade(_alembic_config(), REVISION_004)

    columnas = {c["name"] for c in inspect(engine_migrado).get_columns("turno")}
    indices = _indices(engine_migrado)

    assert "token_cancelacion" not in columnas
    assert "rn05_un_activo_por_dia" not in indices
    assert CONSTRAINTS_RN02 <= _constraints(engine_migrado)


def test_turno_sin_token_puede_persistir(engine_migrado):
    inicio = datetime(2030, 1, 7, 13, 0, tzinfo=timezone.utc)
    with engine_migrado.begin() as conn:
        ids = _crear_catalogo(conn)
        _insertar_turno(
            conn, ids, inicio, inicio + timedelta(minutes=30), token=None
        )
        total = conn.execute(text("SELECT count(*) FROM turno")).scalar_one()

    assert total == 1


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
    conn, ids: dict[str, uuid.UUID], inicio: datetime, fin: datetime,
    token: str | None = None
) -> uuid.UUID:
    turno_id = uuid.uuid4()
    conn.execute(
        text(
            "INSERT INTO turno "
            "(id, profesional_id, sillon_id, prestacion_id, paciente_id, inicio, fin, token_cancelacion) "
            "VALUES (:id, :p, :s, :pr, :pa, :inicio, :fin, :token)"
        ),
        {
            "id": turno_id,
            "p": ids["p"],
            "s": ids["s"],
            "pr": ids["pr"],
            "pa": ids["pa"],
            "inicio": inicio,
            "fin": fin,
            "token": token,
        },
    )
    return turno_id
