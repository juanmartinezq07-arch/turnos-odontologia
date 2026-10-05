"""E2E guest (task 5.3): reserva + token + RN05 + rechazo clinico."""
from tests.conftest import proximo_dia_habil


def _reserva(ids, inicio, telefono="11-0000-0001", **extra):
    cuerpo = {
        "profesional_id": str(ids["p1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": inicio.isoformat(),
        "paciente": {"nombre": "Juan Perez Demo", "telefono": telefono},
    }
    cuerpo.update(extra)
    return cuerpo


async def test_reserva_guest_e2e_y_cancelacion_con_token(client, seed_catalog):
    inicio = proximo_dia_habil(10, 0)
    r = await client.post("/reservas", json=_reserva(seed_catalog, inicio))
    assert r.status_code == 201, r.text
    datos = r.json()
    assert datos["token_cancelacion"]
    assert datos["fin"] > datos["inicio"]

    token = datos["token_cancelacion"]
    r2 = await client.post(f"/reservas/{token}/cancelacion")
    assert r2.status_code == 200
    assert r2.json()["estado"] == "cancelado"

    r3 = await client.post(f"/reservas/{token}/cancelacion")
    assert r3.status_code == 409  # reutilizar token no tiene doble efecto


async def test_token_inexistente_404(client, seed_catalog):
    r = await client.post("/reservas/token-que-no-existe/cancelacion")
    assert r.status_code == 404


async def test_guest_segundo_activo_mismo_dia_409(client, seed_catalog):
    base = proximo_dia_habil(10, 0)
    r1 = await client.post("/reservas", json=_reserva(seed_catalog, base))
    assert r1.status_code == 201, r1.text
    r2 = await client.post(
        "/reservas", json=_reserva(seed_catalog, base.replace(hour=11))
    )
    assert r2.status_code == 409
    assert r2.json()["code"] == "RN05"


async def test_guest_payload_clinico_422(client, seed_catalog):
    cuerpo = _reserva(
        seed_catalog, proximo_dia_habil(12, 0), diagnostico="caries distal"
    )
    r = await client.post("/reservas", json=cuerpo)
    assert r.status_code == 422
    assert r.json()["code"] == "VALIDACION"


async def test_guest_sin_sillon_autoasigna_primero_libre(client, seed_catalog):
    inicio = proximo_dia_habil(14, 0)
    r1 = await client.post("/reservas", json=_reserva(seed_catalog, inicio))
    assert r1.status_code == 201, r1.text
    sillon_ocupado = r1.json()["sillon_id"]
    r2 = await client.post(
        "/reservas",
        json=_reserva(seed_catalog, inicio, telefono="11-0000-0002"),
    )
    assert r2.status_code == 201, r2.text
    assert r2.json()["sillon_id"] != sillon_ocupado
