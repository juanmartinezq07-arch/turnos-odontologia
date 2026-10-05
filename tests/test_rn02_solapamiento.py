"""RN02 secuencial contra Postgres real (task 2.1 RED).

Borde [) no choca, doble eje profesional/sillon, cancelado libera.
Asserts por nombre de constraint, nunca por status solo.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.models import (
    PacienteGuest,
    Prestacion,
    Profesional,
    Sillon,
    Turno,
)

TZ = ZoneInfo("America/Argentina/Buenos_Aires")


def _dt(h, mi, dia=6, mes=5, anio=2030):
    return datetime(anio, mes, dia, h, mi, tzinfo=TZ)


@pytest.fixture
async def seed(db_session):
    p1 = Profesional(nombre="Ana", apellido="Demo", matricula="MAT-001")
    p2 = Profesional(nombre="Luis", apellido="Demo", matricula="MAT-002")
    s1 = Sillon(nombre="Sillon 1")
    s2 = Sillon(nombre="Sillon 2")
    pr = Prestacion(nombre="Consulta Demo", duracion_min=30)
    pa = PacienteGuest(nombre="Juan Perez Demo", telefono="11-0000-0001")
    db_session.add_all([p1, p2, s1, s2, pr, pa])
    await db_session.flush()
    return {"p1": p1, "p2": p2, "s1": s1, "s2": s2, "pr": pr, "pa": pa}


def _turno(seed, inicio, fin, prof=None, sillon=None, estado="activo"):
    return Turno(
        profesional_id=(prof or seed["p1"]).id,
        sillon_id=(sillon or seed["s1"]).id,
        prestacion_id=seed["pr"].id,
        paciente_id=seed["pa"].id,
        inicio=inicio,
        fin=fin,
        estado=estado,
    )


async def test_borde_que_se_toca_no_choca(db_session, seed):
    db_session.add(_turno(seed, _dt(10, 0), _dt(10, 30)))
    await db_session.flush()
    db_session.add(_turno(seed, _dt(10, 30), _dt(11, 0)))
    await db_session.flush()  # no debe violar nada


async def test_choque_mismo_profesional_distinto_sillon(db_session, seed):
    db_session.add(_turno(seed, _dt(10, 0), _dt(10, 30)))
    await db_session.flush()
    db_session.add(_turno(seed, _dt(10, 15), _dt(10, 45), sillon=seed["s2"]))
    with pytest.raises(IntegrityError) as exc:
        await db_session.flush()
    assert exc.value.orig.diag.constraint_name == "rn02_profesional"
    await db_session.rollback()


async def test_choque_mismo_sillon_distinto_profesional(db_session, seed):
    db_session.add(_turno(seed, _dt(10, 0), _dt(10, 30)))
    await db_session.flush()
    db_session.add(_turno(seed, _dt(10, 15), _dt(10, 45), prof=seed["p2"]))
    with pytest.raises(IntegrityError) as exc:
        await db_session.flush()
    assert exc.value.orig.diag.constraint_name == "rn02_sillon"
    await db_session.rollback()


async def test_cancelado_libera_el_slot(db_session, seed):
    viejo = _turno(seed, _dt(10, 0), _dt(10, 30), estado="cancelado")
    db_session.add(viejo)
    await db_session.flush()
    db_session.add(_turno(seed, _dt(10, 0), _dt(10, 30)))
    await db_session.flush()  # el parcial WHERE estado='activo' lo permite
