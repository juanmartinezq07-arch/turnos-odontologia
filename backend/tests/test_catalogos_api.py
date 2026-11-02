"""Tests de catálogos públicos (C-24): GET /profesionales, /sillones, /prestaciones.

Verifica:
- 200 OK sin credenciales (rutas públicas KB-03).
- Solo se devuelven registros activos (activo=True / activa=True).
- duracion_min visible en /prestaciones (RN01).
- Presencia de las 3 rutas en /openapi.json.
- Schemas de salida rechazan campos extra (extra='forbid').
"""
import uuid
from types import SimpleNamespace

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.models import Prestacion, Profesional, Sillon
from app.main import create_app


def test_catalogos_presentes_en_openapi():
    paths = create_app().openapi()["paths"]
    for ruta in ("/profesionales", "/sillones", "/prestaciones"):
        assert ruta in paths, f"Falta {ruta} en /openapi.json"
        assert "get" in paths[ruta]


def test_schemas_catalogo_validan_orm_y_rechazan_extra():
    from app.schemas.catalogo import PrestacionOut, ProfesionalOut, SillonOut

    uid = uuid.uuid4()
    prof = ProfesionalOut.model_validate(
        SimpleNamespace(
            id=uid, nombre="Ana", apellido="Demo", matricula="MAT-1"
        )
    )
    assert prof.id == uid
    sillon = SillonOut.model_validate(SimpleNamespace(id=uid, nombre="Sillon 1"))
    assert sillon.nombre == "Sillon 1"
    prest = PrestacionOut.model_validate(
        SimpleNamespace(id=uid, nombre="Consulta Demo", duracion_min=30)
    )
    assert prest.duracion_min == 30

    with pytest.raises(ValidationError):
        ProfesionalOut(
            id=uid,
            nombre="Ana",
            apellido="Demo",
            matricula="MAT-1",
            campo_extra="prohibido",
        )


@pytest_asyncio.fixture
async def seed_catalog_con_inactivos(db_engine):
    """Puebla profesionales, sillones y prestaciones activos e inactivos."""
    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with factory() as session:
        p_activo_1 = Profesional(
            nombre="Ana", apellido="Zeta Demo", matricula="MAT-101", activo=True
        )
        p_activo_2 = Profesional(
            nombre="Bruno", apellido="Alba Demo", matricula="MAT-102", activo=True
        )
        p_inactivo = Profesional(
            nombre="Carlos", apellido="Inactivo Demo", matricula="MAT-999", activo=False
        )

        s_activo_1 = Sillon(nombre="Sillon B", activo=True)
        s_activo_2 = Sillon(nombre="Sillon A", activo=True)
        s_inactivo = Sillon(nombre="Sillon Fuera de Servicio", activo=False)

        pr_activa_1 = Prestacion(
            nombre="Obturacion Demo", duracion_min=45, activa=True
        )
        pr_activa_2 = Prestacion(
            nombre="Consulta Demo", duracion_min=30, activa=True
        )
        pr_inactiva = Prestacion(
            nombre="Cirugia Inactiva Demo", duracion_min=60, activa=False
        )

        session.add_all(
            [
                p_activo_1,
                p_activo_2,
                p_inactivo,
                s_activo_1,
                s_activo_2,
                s_inactivo,
                pr_activa_1,
                pr_activa_2,
                pr_inactiva,
            ]
        )
        await session.commit()


async def test_get_profesionales_publico_solo_activos_y_ordenado(
    client, seed_catalog_con_inactivos
):
    r = await client.get("/profesionales")
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) == 2
    assert [p["apellido"] for p in items] == ["Alba Demo", "Zeta Demo"]
    for p in items:
        assert set(p.keys()) == {"id", "nombre", "apellido", "matricula"}


async def test_get_sillones_publico_solo_activos_y_ordenado(
    client, seed_catalog_con_inactivos
):
    r = await client.get("/sillones")
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) == 2
    assert [s["nombre"] for s in items] == ["Sillon A", "Sillon B"]
    for s in items:
        assert set(s.keys()) == {"id", "nombre"}


async def test_get_prestaciones_publico_solo_activas_con_duracion_rn01(
    client, seed_catalog_con_inactivos
):
    r = await client.get("/prestaciones")
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) == 2
    assert [pr["nombre"] for pr in items] == ["Consulta Demo", "Obturacion Demo"]
    assert [pr["duracion_min"] for pr in items] == [30, 45]
    for pr in items:
        assert set(pr.keys()) == {"id", "nombre", "duracion_min"}
