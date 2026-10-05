"""Disponibilidad determinista + agenda (tasks 3.4, 6.1)."""
from tests.conftest import proximo_dia_habil


def _alta(ids, inicio, telefono="11-0000-0001"):
    return {
        "profesional_id": str(ids["p1"]),
        "sillon_id": str(ids["s1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": inicio.isoformat(),
        "paciente": {"nombre": "Juan Perez Demo", "telefono": telefono},
    }


async def test_disponibilidad_doble_consulta_identica(client, seed_catalog):
    fecha = proximo_dia_habil(10, 0).date().isoformat()
    params = {
        "profesional_id": str(seed_catalog["p1"]),
        "fecha": fecha,
        "prestacion_id": str(seed_catalog["c30"]),
    }
    r1 = await client.get("/disponibilidad", params=params)
    r2 = await client.get("/disponibilidad", params=params)
    assert r1.status_code == 200
    assert r1.json() == r2.json()


async def test_hueco_ocupado_ausente_y_cancelado_presente(
    client, seed_catalog, headers_recepcion
):
    base = proximo_dia_habil(10, 0)
    fecha = base.date().isoformat()
    params = {
        "profesional_id": str(seed_catalog["p1"]),
        "fecha": fecha,
        "prestacion_id": str(seed_catalog["c30"]),
    }
    r0 = await client.post("/turnos", json=_alta(seed_catalog, base), headers=headers_recepcion)
    turno_id = r0.json()["id"]
    con_turno = (await client.get("/disponibilidad", params=params)).json()["slots"]
    assert base.isoformat() not in con_turno
    await client.delete(f"/turnos/{turno_id}", headers=headers_recepcion)
    liberado = (await client.get("/disponibilidad", params=params)).json()["slots"]
    assert base.isoformat() in liberado


async def test_slots_duracion_45(client, seed_catalog):
    fecha = proximo_dia_habil(10, 0).date().isoformat()
    params = {
        "profesional_id": str(seed_catalog["p1"]),
        "fecha": fecha,
        "prestacion_id": str(seed_catalog["o45"]),
    }
    r = await client.get("/disponibilidad", params=params)
    assert r.status_code == 200
    from datetime import datetime
    slots = [datetime.fromisoformat(s) for s in r.json()["slots"]]
    assert slots
    assert all((s.hour * 60 + s.minute - 9 * 60) % 45 == 0 for s in slots)


async def test_agenda_ordenada_y_filtro_cancelados(
    client, seed_catalog, headers_recepcion, headers_odonto
):
    base = proximo_dia_habil(9, 0)
    fecha = base.date().isoformat()
    for h in (9, 11, 10):
        r = await client.post(
            "/turnos",
            json=_alta(seed_catalog, base.replace(hour=h), telefono=f"11-0000-00{h:02d}"),
            headers=headers_recepcion,
        )
        assert r.status_code == 201, r.text
    a_cancelar = await client.post(
        "/turnos",
        json=_alta(seed_catalog, base.replace(hour=12), telefono="11-0000-0099"),
        headers=headers_recepcion,
    )
    await client.delete(f"/turnos/{a_cancelar.json()['id']}", headers=headers_recepcion)
    params = {"profesional_id": str(seed_catalog["p1"]), "fecha": fecha}
    agenda = (await client.get("/agenda", params=params, headers=headers_odonto)).json()
    inicios = [t["inicio"] for t in agenda["turnos"]]
    assert inicios == sorted(inicios)
    assert len(agenda["turnos"]) == 3
    assert all("prestacion" in t and "sillon" in t and "paciente" in t for t in agenda["turnos"])
    completa = (
        await client.get(
            "/agenda", params={**params, "incluir_cancelados": "true"},
            headers=headers_odonto,
        )
    ).json()
    assert len(completa["turnos"]) == 4


async def test_catalogos_publicos(client, seed_catalog):
    for ruta in ("/profesionales", "/sillones", "/prestaciones"):
        r = await client.get(ruta)
        assert r.status_code == 200
        assert len(r.json()) >= 2
