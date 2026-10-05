"""RN02 bajo concurrencia real (task 5.1): 2 POST al mismo slot -> 201 + 409."""
import asyncio

from tests.conftest import proximo_dia_habil


def _payload(ids, inicio):
    return {
        "profesional_id": str(ids["p1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": inicio.isoformat(),
        "paciente": {"nombre": "Juan Perez Demo", "telefono": "11-0000-0001"},
    }


async def test_doble_post_concurrente_un_ganador(client, seed_catalog):
    inicio = proximo_dia_habil(10, 0)
    cuerpo = _payload(seed_catalog, inicio)

    async def post():
        return await client.post("/reservas", json=cuerpo)

    r1, r2 = await asyncio.gather(post(), post())
    assert sorted([r1.status_code, r2.status_code]) == [201, 409]
    perdedor = r1 if r1.status_code == 409 else r2
    assert perdedor.json()["code"] in ("RN02_PROFESIONAL", "RN02_SILLON")
