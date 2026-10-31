"""POST /turnos recepcionista: RN01 + RN02 + RN03 (alcance C-01)."""
from tests.conftest import proximo_dia_habil


def _alta(ids, inicio, telefono="11-0000-0001", email=None, **extra):
    iso = inicio.isoformat() if hasattr(inicio, "isoformat") else inicio
    paciente = {"nombre": "Juan Perez Demo", "telefono": telefono}
    if email:
        paciente["email"] = email
    cuerpo = {
        "profesional_id": str(ids["p1"]),
        "sillon_id": str(ids["s1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": iso,
        "paciente": paciente,
    }
    cuerpo.update(extra)
    return cuerpo


async def test_alta_calcula_fin_rn01(client, seed_catalog, headers_recepcion):
    inicio = proximo_dia_habil(10, 0)
    r = await client.post(
        "/turnos", json=_alta(seed_catalog, inicio),
        headers=headers_recepcion,
    )
    assert r.status_code == 201, r.text
    datos = r.json()
    assert datos["inicio"] == inicio.isoformat()
    assert datos["fin"] == inicio.replace(minute=30).isoformat()


async def test_choque_profesional_409(client, seed_catalog, headers_recepcion):
    base = proximo_dia_habil(10, 0)
    r1 = await client.post("/turnos", json=_alta(seed_catalog, base), headers=headers_recepcion)
    assert r1.status_code == 201, r1.text
    otro_sillon = dict(_alta(seed_catalog, base.replace(minute=15)))
    otro_sillon["sillon_id"] = str(seed_catalog["s2"])
    r2 = await client.post("/turnos", json=otro_sillon, headers=headers_recepcion)
    assert r2.status_code == 409
    assert r2.json()["code"] == "RN02_PROFESIONAL"


async def test_choque_sillon_409(client, seed_catalog, headers_recepcion):
    base = proximo_dia_habil(11, 0)
    r1 = await client.post("/turnos", json=_alta(seed_catalog, base), headers=headers_recepcion)
    assert r1.status_code == 201, r1.text
    otro_prof = dict(_alta(seed_catalog, base.replace(minute=15)))
    otro_prof["profesional_id"] = str(seed_catalog["p2"])
    r2 = await client.post("/turnos", json=otro_prof, headers=headers_recepcion)
    assert r2.status_code == 409
    assert r2.json()["code"] == "RN02_SILLON"


async def test_borde_201(client, seed_catalog, headers_recepcion):
    base = proximo_dia_habil(10, 0)
    r1 = await client.post("/turnos", json=_alta(seed_catalog, base, telefono="11-0000-0001"), headers=headers_recepcion)
    assert r1.status_code == 201, r1.text
    r2 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, base.replace(minute=30), telefono="11-0000-0002"),
        headers=headers_recepcion,
    )
    assert r2.status_code == 201, r2.text


async def test_pasado_422(client, seed_catalog, headers_recepcion):
    r = await client.post(
        "/turnos", json=_alta(seed_catalog, "2020-01-06T10:00:00-03:00"),
        headers=headers_recepcion,
    )
    assert r.status_code == 422


async def test_fuera_de_horario_422(client, seed_catalog, headers_recepcion):
    # domingo sin atencion
    from datetime import timedelta
    base = proximo_dia_habil(10, 0)
    domingo = base + timedelta(days=(6 - base.weekday()) % 7 or 7)
    domingo = domingo.replace(hour=10, minute=0)
    r = await client.post(
        "/turnos", json=_alta(seed_catalog, domingo.isoformat()),
        headers=headers_recepcion,
    )
    assert r.status_code == 422


async def test_con_fin_explicito_422(client, seed_catalog, headers_recepcion):
    cuerpo = _alta(seed_catalog, proximo_dia_habil(10, 0).isoformat())
    cuerpo["fin"] = proximo_dia_habil(10, 30).isoformat()
    r = await client.post("/turnos", json=cuerpo, headers=headers_recepcion)
    assert r.status_code == 422
