"""Verificacion pura sin DB: docs, auth, schemas y mapper (alcance C-01)."""
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from types import SimpleNamespace

from app.core.errors import conflict_code_from_integrity_error
from app.schemas.turno import TurnoCreate


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
    assert {"/turnos"} <= rutas


async def test_post_turnos_sin_key_401(app_client):
    r = await app_client.post("/turnos", json={})
    assert r.status_code == 401
    assert r.json()["code"] == "NO_AUTORIZADO"


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
        TurnoCreate(
            profesional_id="11111111-1111-1111-1111-111111111111",
            sillon_id="22222222-2222-2222-2222-222222222222",
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
