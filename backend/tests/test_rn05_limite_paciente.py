"""RN05 límite por paciente: máximo 1 turno activo por día, código RN05.

Tests de punta a punta contra POST /turnos con Postgres real.
Esperan fallar en RED porque la aplicación aún no mapea rn05_un_activo_por_dia
a RN05 ni hace precheck de aplicación.
"""
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


async def test_rn05_mismo_paciente_mismo_dia_409(
    client, seed_catalog, headers_recepcion
):
    """Mismo paciente, mismo día, dos turnos activos → 409 con code RN05."""
    inicio = proximo_dia_habil(10, 0)
    r1 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, inicio, telefono="11-0000-0001"),
        headers=headers_recepcion,
    )
    assert r1.status_code == 201, r1.text
    r2 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, inicio.replace(minute=45), telefono="11-0000-0001"),
        headers=headers_recepcion,
    )
    assert r2.status_code == 409, r2.text
    assert r2.json()["code"] == "RN05"


async def test_rn05_distinto_paciente_mismo_dia_201(
    client, seed_catalog, headers_recepcion
    ):
    """Distinto paciente, mismo día → ambos 201."""
    inicio = proximo_dia_habil(10, 0)
    r1 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, inicio, telefono="11-0000-0001"),
        headers=headers_recepcion,
    )
    assert r1.status_code == 201, r1.text
    r2 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, inicio.replace(minute=45), telefono="11-0000-0002"),
        headers=headers_recepcion,
    )
    assert r2.status_code == 201, r2.text


async def test_rn05_mismo_paciente_dia_distinto_201(
    client, seed_catalog, headers_recepcion
):
    """Mismo paciente, día distinto → ambos 201."""
    inicio = proximo_dia_habil(10, 0)
    r1 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, inicio, telefono="11-0000-0001"),
        headers=headers_recepcion,
    )
    assert r1.status_code == 201, r1.text
    otro_dia = proximo_dia_habil(10, 0)
    # Asegurar que es un día diferente al primero
    if otro_dia.date() == inicio.date():
        otro_dia = otro_dia.replace(day=inicio.day + 2)
    r2 = await client.post(
        "/turnos",
        json=_alta(seed_catalog, otro_dia, telefono="11-0000-0001"),
        headers=headers_recepcion,
    )
    assert r2.status_code == 201, r2.text
