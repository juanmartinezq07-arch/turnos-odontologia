"""Verificacion pura sin DB: docs, auth, schemas, mapper, slots, rate-limit."""
from datetime import date, datetime, time
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.application.availability import generar_slots
from app.core.errors import conflict_code_from_integrity_error
from app.schemas.turno import ReservaCreate, TurnoCreate

TZ = ZoneInfo("America/Argentina/Buenos_Aires")


import pytest_asyncio


@pytest_asyncio.fixture
async def app_client():
    from app.main import create_app

    transport = ASGITransport(app=create_app())
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


async def test_docs_y_openapi_accesibles(app_client):
    assert (await app_client.get("/docs")).status_code == 200
    r = await app_client.get("/openapi.json")
    assert r.status_code == 200
    rutas = set(r.json()["paths"].keys())
    assert {
        "/turnos", "/disponibilidad", "/reservas",
        "/agenda", "/profesionales", "/sillones", "/prestaciones",
    } <= rutas


async def test_post_turnos_sin_key_401(app_client):
    r = await app_client.post("/turnos", json={})
    assert r.status_code == 401
    assert r.json()["code"] == "NO_AUTORIZADO"


async def test_agenda_sin_key_401(app_client):
    r = await app_client.get("/agenda", params={"profesional_id": str(__import__("uuid").uuid4()), "fecha": "2030-05-06"})
    assert r.status_code == 401


async def test_agenda_ajena_403_sin_tocar_db():
    import uuid

    from app.core.security import get_current_odontologo
    from app.main import create_app

    prof_a, prof_b = str(uuid.uuid4()), str(uuid.uuid4())
    app = create_app()
    app.dependency_overrides[get_current_odontologo] = lambda: prof_a
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://t") as client:
        r = await client.get(
            "/agenda",
            params={"profesional_id": prof_b, "fecha": "2030-05-06"},
            headers={"X-API-Key": "cualquiera"},
        )
    assert r.status_code == 403
    assert r.json()["code"] == "PROHIBIDO"
    app.dependency_overrides.clear()


def test_schema_rechaza_campo_fin():
    with pytest.raises(ValidationError):
        TurnoCreate(
            profesional_id="11111111-1111-1111-1111-111111111111",
            sillon_id="22222222-2222-2222-2222-222222222222",
            prestacion_id="33333333-3333-3333-3333-333333333333",
            inicio="2030-05-06T10:00:00-03:00",
            fin="2030-05-06T10:30:00-03:00",
            paciente={"nombre": "Juan Perez Demo", "telefono": "11-0000-0001"},
        )


def test_schema_rechaza_campo_clinico():
    with pytest.raises(ValidationError):
        ReservaCreate(
            profesional_id="11111111-1111-1111-1111-111111111111",
            prestacion_id="33333333-3333-3333-3333-333333333333",
            inicio="2030-05-06T10:00:00-03:00",
            paciente={"nombre": "Juan Perez Demo", "telefono": "11-0000-0001"},
            diagnostico="caries distal",
        )


def _integrity(constraint: str) -> IntegrityError:
    orig = SimpleNamespace(diag=SimpleNamespace(constraint_name=constraint))
    return IntegrityError("INSERT", {}, orig)


def test_mapper_rn02_profesional():
    assert conflict_code_from_integrity_error(_integrity("rn02_profesional")) == "RN02_PROFESIONAL"


def test_mapper_rn02_sillon():
    assert conflict_code_from_integrity_error(_integrity("rn02_sillon")) == "RN02_SILLON"


def test_mapper_rn05():
    assert conflict_code_from_integrity_error(_integrity("rn05_un_activo_por_dia")) == "RN05"


def test_slots_deterministas_y_ordenados():
    bloques = [(time(9, 0), time(18, 0))]
    dia = date(2030, 5, 6)
    a = generar_slots(bloques, [], 30, dia, TZ)
    b = generar_slots(bloques, [], 30, dia, TZ)
    assert a == b
    assert a == sorted(a)
    assert len(a) == 18  # 9 horas en bloques de 30


def test_slots_excluyen_ocupado_y_respetan_duracion():
    bloques = [(time(9, 0), time(12, 0))]
    dia = date(2030, 5, 6)
    ocupados = [
        (datetime(2030, 5, 6, 10, 0, tzinfo=TZ), datetime(2030, 5, 6, 10, 45, tzinfo=TZ))
    ]
    slots = generar_slots(bloques, ocupados, 45, dia, TZ)
    assert all(
        not (s < datetime(2030, 5, 6, 10, 45, tzinfo=TZ) and s + __import__("datetime").timedelta(minutes=45) > datetime(2030, 5, 6, 10, 0, tzinfo=TZ))
        for s in slots
    )
    assert slots, "debe haber huecos fuera del ocupado"


def test_slots_nunca_en_pasado():
    bloques = [(time(9, 0), time(18, 0))]
    dia = date(2030, 5, 6)
    desde = datetime(2030, 5, 6, 15, 0, tzinfo=TZ)
    slots = generar_slots(bloques, [], 30, dia, TZ, desde=desde)
    assert all(s >= desde for s in slots)


def test_rate_limit_bloquea_al_exceder(monkeypatch):
    from app.api.v1 import reservas as reservas_router

    monkeypatch.setenv("RESERVA_RATE_LIMIT", "2/minute")
    reservas_router.reset_rate_limit()
    req = SimpleNamespace(headers={}, client=SimpleNamespace(host="9.9.9.9"))
    reservas_router._chequear_rate_limit(req)
    reservas_router._chequear_rate_limit(req)
    with pytest.raises(reservas_router.RateLimited):
        reservas_router._chequear_rate_limit(req)
    reservas_router.reset_rate_limit()
