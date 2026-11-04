"""Tests para C-22: POST /turnos/{id}/cancelacion (RN04 + idempotencia + errores)."""
import uuid

from app.notifications.mock import MockNotificationService
from tests.conftest import proximo_dia_habil


def _alta_payload(ids, inicio, telefono="11-0000-0022", email="paciente.c22@example.com"):
    iso = inicio.isoformat() if hasattr(inicio, "isoformat") else inicio
    return {
        "profesional_id": str(ids["p1"]),
        "sillon_id": str(ids["s1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": iso,
        "paciente": {
            "nombre": "Lucia Cancelacion Demo",
            "telefono": telefono,
            "email": email,
        },
    }


async def test_turno_out_incluye_cancelled_at_nulo_en_alta(
    client, seed_catalog, headers_recepcion
):
    inicio = proximo_dia_habil(10, 0)
    r = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio),
        headers=headers_recepcion,
    )
    assert r.status_code == 201, r.text
    datos = r.json()
    assert "cancelled_at" in datos
    assert datos["cancelled_at"] is None


async def test_cancelar_turno_libera_slot_y_notifica(
    client, seed_catalog, headers_recepcion, monkeypatch
):
    mock_notif = MockNotificationService()
    monkeypatch.setattr(
        "app.application.bookings.get_notification_service", lambda: mock_notif
    )

    inicio = proximo_dia_habil(10, 0)
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201, r_alta.text
    turno_id = r_alta.json()["id"]

    # Cancelar el turno activo
    r_canc = await client.post(
        f"/turnos/{turno_id}/cancelacion",
        headers=headers_recepcion,
    )
    assert r_canc.status_code == 200, r_canc.text
    datos_canc = r_canc.json()
    assert datos_canc["id"] == turno_id
    assert datos_canc["estado"] == "cancelado"
    assert datos_canc["cancelled_at"] is not None

    # Debe haberse registrado evento "updated" en el servicio de notificaciones mock
    assert any(
        str(ev["turn_id"]) == turno_id and ev["action"] == "updated"
        for ev in mock_notif.events
    )

    # El slot queda liberado en RN02 (profesional + sillon) y RN05 (mismo paciente mismo dia)
    r_nuevo = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio),
        headers=headers_recepcion,
    )
    assert r_nuevo.status_code == 201, r_nuevo.text
    assert r_nuevo.json()["estado"] == "activo"


async def test_cancelar_turno_inexistente_404_y_sin_auth_401(
    client, seed_catalog, headers_recepcion
):
    id_inexistente = uuid.uuid4()

    # Sin credencial -> 401
    r_401 = await client.post(f"/turnos/{id_inexistente}/cancelacion")
    assert r_401.status_code == 401

    # Con credencial pero UUID inexistente -> 404 NO_ENCONTRADO
    r_404 = await client.post(
        f"/turnos/{id_inexistente}/cancelacion",
        headers=headers_recepcion,
    )
    assert r_404.status_code == 404, r_404.text
    err = r_404.json()
    assert err["code"] == "NO_ENCONTRADO"
    assert isinstance(err["message"], str) and len(err["message"]) > 0


async def test_cancelar_turno_idempotente_conserva_cancelled_at(
    client, seed_catalog, headers_recepcion, monkeypatch
):
    mock_notif = MockNotificationService()
    monkeypatch.setattr(
        "app.application.bookings.get_notification_service", lambda: mock_notif
    )

    inicio = proximo_dia_habil(11, 0)
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio, telefono="11-0000-0023"),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201, r_alta.text
    turno_id = r_alta.json()["id"]

    # Primera cancelacion
    r1 = await client.post(
        f"/turnos/{turno_id}/cancelacion",
        headers=headers_recepcion,
    )
    assert r1.status_code == 200, r1.text
    t1 = r1.json()["cancelled_at"]
    assert t1 is not None

    updated_events_1 = [
        ev for ev in mock_notif.events if ev["action"] == "updated"
    ]
    assert len(updated_events_1) == 1

    # Segunda cancelacion (idempotente): 200 OK, mismo cancelled_at y no duplica notificacion
    r2 = await client.post(
        f"/turnos/{turno_id}/cancelacion",
        headers=headers_recepcion,
    )
    assert r2.status_code == 200, r2.text
    assert r2.json()["estado"] == "cancelado"
    assert r2.json()["cancelled_at"] == t1

    updated_events_2 = [
        ev for ev in mock_notif.events if ev["action"] == "updated"
    ]
    assert len(updated_events_2) == 1


async def test_cancelar_turno_presente_en_openapi(client):
    r = await client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json().get("paths", {})
    assert "/turnos/{turno_id}/cancelacion" in paths
    assert "post" in paths["/turnos/{turno_id}/cancelacion"]
