"""Tests de disponibilidad real (C-25): función pura + GET /disponibilidad.

Verifica:
- Función pura rules.calcular_slots_disponibles (huecos, bloque que no entra completo,
  borde [) no pisa activos, descarte de pasado con now inyectado, determinismo).
- Endpoint público GET /disponibilidad?profesional_id=&fecha=&prestacion_id= (200 sin credencial,
  turno activo resta hueco, turno cancelado no resta hueco, determinismo en dos llamadas
  seguidas, presencia en /openapi.json).
"""
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from app.domain import rules
from app.domain.models import PacienteGuest, Turno
from app.main import create_app
from tests.conftest import proximo_dia_habil

TZ = ZoneInfo("America/Argentina/Buenos_Aires")


# --- 1. Tests unitarios puros sobre rules.calcular_slots_disponibles ---


def test_puro_huecos_y_borde_semiabierto():
    """Horario 09:00 a 11:00, prestación 30 min, turno activo 09:30 a 10:00."""
    fecha = date(2030, 5, 6)
    ahora = datetime(2030, 5, 6, 8, 0, tzinfo=TZ)
    bloques = [(time(9, 0), time(11, 0))]
    ocupados = [
        (
            datetime(2030, 5, 6, 9, 30, tzinfo=TZ),
            datetime(2030, 5, 6, 10, 0, tzinfo=TZ),
        )
    ]

    slots = rules.calcular_slots_disponibles(
        fecha=fecha,
        bloques=bloques,
        ocupados=ocupados,
        duracion_min=30,
        ahora=ahora,
        tz=TZ,
    )

    esperados = [
        (
            datetime(2030, 5, 6, 9, 0, tzinfo=TZ),
            datetime(2030, 5, 6, 9, 30, tzinfo=TZ),
        ),
        (
            datetime(2030, 5, 6, 10, 0, tzinfo=TZ),
            datetime(2030, 5, 6, 10, 30, tzinfo=TZ),
        ),
        (
            datetime(2030, 5, 6, 10, 30, tzinfo=TZ),
            datetime(2030, 5, 6, 11, 0, tzinfo=TZ),
        ),
    ]
    assert slots == esperados


def test_puro_bloque_que_no_entra_completo_al_final_se_descarta():
    """Horario 09:00 a 12:00 (180 min) con prestación de 45 min -> 4 slots; si cierra 11:50 -> 3 slots."""
    fecha = date(2030, 5, 6)
    ahora = datetime(2030, 5, 6, 8, 0, tzinfo=TZ)
    bloques = [(time(9, 0), time(11, 50))]

    slots = rules.calcular_slots_disponibles(
        fecha=fecha,
        bloques=bloques,
        ocupados=[],
        duracion_min=45,
        ahora=ahora,
        tz=TZ,
    )

    # 09:00-09:45, 09:45-10:30, 10:30-11:15 (el de 11:15-12:00 excede 11:50)
    assert len(slots) == 3
    assert slots[-1][1] == datetime(2030, 5, 6, 11, 15, tzinfo=TZ)


def test_puro_descarta_pasado_segun_ahora_inyectado():
    """Si ahora es 10:15, ningún slot tiene inicio < 10:15."""
    fecha = date(2030, 5, 6)
    ahora = datetime(2030, 5, 6, 10, 15, tzinfo=TZ)
    bloques = [(time(9, 0), time(11, 30))]

    slots = rules.calcular_slots_disponibles(
        fecha=fecha,
        bloques=bloques,
        ocupados=[],
        duracion_min=30,
        ahora=ahora,
        tz=TZ,
    )

    assert all(ini >= ahora for ini, _ in slots)
    assert [ini.time() for ini, _ in slots] == [time(10, 30), time(11, 0)]


def test_puro_determinismo_dos_llamadas_identicas():
    """Dos ejecuciones con los mismos argumentos devuelven exactamente lo mismo."""
    fecha = date(2030, 5, 6)
    ahora = datetime(2030, 5, 6, 8, 0, tzinfo=TZ)
    bloques = [(time(9, 0), time(12, 0))]
    ocupados = [
        (
            datetime(2030, 5, 6, 10, 0, tzinfo=TZ),
            datetime(2030, 5, 6, 10, 45, tzinfo=TZ),
        )
    ]

    s1 = rules.calcular_slots_disponibles(
        fecha=fecha,
        bloques=bloques,
        ocupados=ocupados,
        duracion_min=30,
        ahora=ahora,
        tz=TZ,
    )
    s2 = rules.calcular_slots_disponibles(
        fecha=fecha,
        bloques=bloques,
        ocupados=ocupados,
        duracion_min=30,
        ahora=ahora,
        tz=TZ,
    )
    assert s1 == s2
    # Tras el turno 10:00-10:45, el siguiente slot aprovecha el borde 10:45-11:15
    assert (
        datetime(2030, 5, 6, 10, 45, tzinfo=TZ),
        datetime(2030, 5, 6, 11, 15, tzinfo=TZ),
    ) in s1


def test_disponibilidad_presente_en_openapi():
    paths = create_app().openapi()["paths"]
    assert "/disponibilidad" in paths
    assert "get" in paths["/disponibilidad"]


def test_schema_slot_disponibilidad_rechaza_extra():
    from app.schemas.disponibilidad import SlotDisponibilidadOut

    with pytest.raises(ValidationError):
        SlotDisponibilidadOut(
            inicio=datetime(2030, 5, 6, 9, 0, tzinfo=TZ),
            fin=datetime(2030, 5, 6, 9, 30, tzinfo=TZ),
            extra_field="no",
        )


# --- 2. Tests de integración HTTP contra PostgreSQL 16 ---


async def test_get_disponibilidad_publico_determinista_y_respeta_activos_y_cancelados(
    client, seed_catalog, db_session
):
    dia = proximo_dia_habil(9, 0)
    fecha_str = dia.date().isoformat()
    p1 = seed_catalog["p1"]
    s1 = seed_catalog["s1"]
    c30 = seed_catalog["c30"]

    # Insertar un turno activo 09:30-10:00 y uno cancelado 10:00-10:30
    pa1 = PacienteGuest(nombre="Ana Demo", telefono="11-2222-0001")
    pa2 = PacienteGuest(nombre="Luis Demo", telefono="11-2222-0002")
    db_session.add_all([pa1, pa2])
    await db_session.flush()

    t_activo = Turno(
        profesional_id=p1,
        sillon_id=s1,
        prestacion_id=c30,
        paciente_id=pa1.id,
        inicio=dia.replace(hour=9, minute=30),
        fin=dia.replace(hour=10, minute=0),
        estado="activo",
    )
    t_cancelado = Turno(
        profesional_id=p1,
        sillon_id=s1,
        prestacion_id=c30,
        paciente_id=pa2.id,
        inicio=dia.replace(hour=10, minute=0),
        fin=dia.replace(hour=10, minute=30),
        estado="cancelado",
    )
    db_session.add_all([t_activo, t_cancelado])
    await db_session.commit()

    params = {
        "profesional_id": str(p1),
        "fecha": fecha_str,
        "prestacion_id": str(c30),
    }

    # Sin header X-API-Key (público) y determinista en dos llamadas seguidas
    r1 = await client.get("/disponibilidad", params=params)
    r2 = await client.get("/disponibilidad", params=params)

    assert r1.status_code == 200, r1.text
    assert r2.status_code == 200, r2.text
    slots = r1.json()
    assert slots == r2.json()

    inicios = [s["inicio"] for s in slots]
    # 09:00 está libre, 09:30 está ocupado (activo), 10:00 está libre (cancelado no bloquea)
    assert dia.replace(hour=9, minute=0).isoformat() in inicios
    assert dia.replace(hour=9, minute=30).isoformat() not in inicios
    assert dia.replace(hour=10, minute=0).isoformat() in inicios
    for s in slots:
        assert set(s.keys()) == {"inicio", "fin"}


async def test_get_disponibilidad_domingo_sin_horario_devuelve_vacio(
    client, seed_catalog
):
    from datetime import timedelta

    base = proximo_dia_habil(10, 0)
    domingo = (base + timedelta(days=(6 - base.weekday()) % 7 or 7)).date()
    r = await client.get(
        "/disponibilidad",
        params={
            "profesional_id": str(seed_catalog["p1"]),
            "fecha": domingo.isoformat(),
            "prestacion_id": str(seed_catalog["c30"]),
        },
    )
    assert r.status_code == 200, r.text
    assert r.json() == []
