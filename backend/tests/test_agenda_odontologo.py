"""Tests unitarios y de integracion para C-27 (GET /agenda odontologo + RBAC)."""
from datetime import datetime, timedelta
import uuid

import pytest
from pydantic import ValidationError

from app.domain.models import PacienteGuest, Turno
from app.main import create_app
from tests.conftest import proximo_dia_habil


def test_agenda_presente_en_openapi():
    """GET /agenda debe estar documentado en /openapi.json."""
    openapi = create_app().openapi()
    assert "/agenda" in openapi["paths"]
    assert "get" in openapi["paths"]["/agenda"]


def test_schema_agenda_turno_out_rechaza_extra():
    """Regla dura: schemas de agenda con extra='forbid'."""
    from app.schemas.agenda import (
        AgendaPacienteOut,
        AgendaPrestacionOut,
        AgendaSillonOut,
        AgendaTurnoOut,
    )

    ahora = proximo_dia_habil(10, 0)
    with pytest.raises(ValidationError):
        AgendaTurnoOut(
            id=uuid.uuid4(),
            profesional_id=uuid.uuid4(),
            inicio=ahora,
            fin=ahora + timedelta(minutes=30),
            estado="activo",
            prestacion=AgendaPrestacionOut(
                id=uuid.uuid4(), nombre="Consulta Demo", duracion_min=30
            ),
            sillon=AgendaSillonOut(id=uuid.uuid4(), nombre="Sillon 1"),
            paciente=AgendaPacienteOut(
                id=uuid.uuid4(),
                nombre="Juan Perez Demo",
                telefono="11-0000-0001",
                email="juan@example.com",
            ),
            campo_extra="no-permitido",
        )


async def test_get_agenda_ordenada_por_inicio_con_prestacion_sillon_y_paciente(
    client, db_session, seed_catalog
):
    """US-006: devuelve turnos activos ordenados por inicio con prestacion (+duracion_min), sillon y paciente."""
    dia_dt = proximo_dia_habil(10, 0)
    fecha_str = dia_dt.date().isoformat()
    tz = dia_dt.tzinfo

    pac1 = PacienteGuest(
        nombre="Paciente 11h Demo",
        telefono="11-3000-0001",
        email="pac11@example.com",
    )
    pac2 = PacienteGuest(
        nombre="Paciente 09h30 Demo",
        telefono="11-3000-0002",
        email="pac0930@example.com",
    )
    db_session.add_all([pac1, pac2])
    await db_session.flush()

    # Insertamos primero el de las 11:00 (45 min) y luego el de las 09:30 (30 min)
    t_tarde = Turno(
        profesional_id=seed_catalog["p1"],
        sillon_id=seed_catalog["s2"],
        prestacion_id=seed_catalog["o45"],
        paciente_id=pac1.id,
        inicio=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 11, 0, tzinfo=tz),
        fin=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 11, 45, tzinfo=tz),
        estado="activo",
    )
    t_temprano = Turno(
        profesional_id=seed_catalog["p1"],
        sillon_id=seed_catalog["s1"],
        prestacion_id=seed_catalog["c30"],
        paciente_id=pac2.id,
        inicio=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 9, 30, tzinfo=tz),
        fin=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 10, 0, tzinfo=tz),
        estado="activo",
    )
    db_session.add_all([t_tarde, t_temprano])
    await db_session.commit()

    headers_odonto_p1 = {
        "X-API-Key": "test-odontologo-key",
        "X-Profesional-Id": str(seed_catalog["p1"]),
    }
    resp = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p1"]), "fecha": fecha_str},
        headers=headers_odonto_p1,
    )
    assert resp.status_code == 200, resp.text
    items = resp.json()
    assert len(items) == 2

    # Orden ascendente por inicio: primero 09:30, luego 11:00
    assert datetime.fromisoformat(items[0]["inicio"]) == t_temprano.inicio
    assert items[0]["prestacion"]["nombre"] == "Consulta Demo"
    assert items[0]["prestacion"]["duracion_min"] == 30
    assert items[0]["sillon"]["nombre"] == "Sillon 1"
    assert items[0]["paciente"]["nombre"] == "Paciente 09h30 Demo"

    assert datetime.fromisoformat(items[1]["inicio"]) == t_tarde.inicio
    assert items[1]["prestacion"]["nombre"] == "Obturacion Demo"
    assert items[1]["prestacion"]["duracion_min"] == 45
    assert items[1]["sillon"]["nombre"] == "Sillon 2"
    assert items[1]["paciente"]["nombre"] == "Paciente 11h Demo"


async def test_get_agenda_excluye_cancelados_por_defecto_e_incluye_con_filtro(
    client, db_session, seed_catalog
):
    """US-006 / RN04: cancelados no aparecen salvo ?incluir_cancelados=true."""
    dia_dt = proximo_dia_habil(10, 0)
    fecha_str = dia_dt.date().isoformat()
    tz = dia_dt.tzinfo

    pac_act = PacienteGuest(nombre="Activo Demo", telefono="11-3100-0001")
    pac_can = PacienteGuest(nombre="Cancelado Demo", telefono="11-3100-0002")
    db_session.add_all([pac_act, pac_can])
    await db_session.flush()

    t_activo = Turno(
        profesional_id=seed_catalog["p1"],
        sillon_id=seed_catalog["s1"],
        prestacion_id=seed_catalog["c30"],
        paciente_id=pac_act.id,
        inicio=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 10, 0, tzinfo=tz),
        fin=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 10, 30, tzinfo=tz),
        estado="activo",
    )
    t_cancelado = Turno(
        profesional_id=seed_catalog["p1"],
        sillon_id=seed_catalog["s1"],
        prestacion_id=seed_catalog["c30"],
        paciente_id=pac_can.id,
        inicio=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 11, 0, tzinfo=tz),
        fin=datetime(dia_dt.year, dia_dt.month, dia_dt.day, 11, 30, tzinfo=tz),
        estado="cancelado",
    )
    db_session.add_all([t_activo, t_cancelado])
    await db_session.commit()

    headers_odonto_p1 = {
        "X-API-Key": "test-odontologo-key",
        "X-Profesional-Id": str(seed_catalog["p1"]),
    }

    # Por defecto: solo activos
    r_default = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p1"]), "fecha": fecha_str},
        headers=headers_odonto_p1,
    )
    assert r_default.status_code == 200
    assert len(r_default.json()) == 1
    assert r_default.json()[0]["estado"] == "activo"

    # Con ?incluir_cancelados=true: ambos ordenados por inicio
    r_all = await client.get(
        "/agenda",
        params={
            "profesional_id": str(seed_catalog["p1"]),
            "fecha": fecha_str,
            "incluir_cancelados": "true",
        },
        headers=headers_odonto_p1,
    )
    assert r_all.status_code == 200
    assert [t["estado"] for t in r_all.json()] == ["activo", "cancelado"]


async def test_get_agenda_ajena_devuelve_403(client, seed_catalog):
    """KB-03 / KB-07 Flujo 4: odontologo pidiendo agenda de otro profesional recibe 403 AGENDA_AJENA."""
    fecha_str = proximo_dia_habil(10, 0).date().isoformat()
    headers_odonto_p1 = {
        "X-API-Key": "test-odontologo-key",
        "X-Profesional-Id": str(seed_catalog["p1"]),
    }
    resp = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p2"]), "fecha": fecha_str},
        headers=headers_odonto_p1,
    )
    assert resp.status_code == 403
    assert resp.json()["code"] == "AGENDA_AJENA"


async def test_get_agenda_sin_credencial_devuelve_401(client, seed_catalog):
    """Sin X-API-Key o con clave invalida responde 401."""
    fecha_str = proximo_dia_habil(10, 0).date().isoformat()
    r_sin = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p1"]), "fecha": fecha_str},
    )
    assert r_sin.status_code == 401
    assert r_sin.json()["code"] == "NO_AUTORIZADO"

    r_inv = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p1"]), "fecha": fecha_str},
        headers={"X-API-Key": "clave-inexistente"},
    )
    assert r_inv.status_code == 401


async def test_get_agenda_fecha_invalida_devuelve_422(client, seed_catalog):
    """KB-07 Flujo 4: fecha invalida -> 422."""
    headers_odonto_p1 = {
        "X-API-Key": "test-odontologo-key",
        "X-Profesional-Id": str(seed_catalog["p1"]),
    }
    resp = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p1"]), "fecha": "no-es-fecha"},
        headers=headers_odonto_p1,
    )
    assert resp.status_code == 422
    assert resp.json()["code"] == "VALIDACION"


async def test_get_agenda_recepcionista_lectura_global(
    client, seed_catalog, headers_recepcion
):
    """KB-03 RBAC: recepcionista tiene lectura global de agenda sin requerir X-Profesional-Id."""
    fecha_str = proximo_dia_habil(10, 0).date().isoformat()
    resp = await client.get(
        "/agenda",
        params={"profesional_id": str(seed_catalog["p2"]), "fecha": fecha_str},
        headers=headers_recepcion,
    )
    assert resp.status_code == 200
    assert resp.json() == []
