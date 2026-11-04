"""Tests para C-29: reservas públicas guest (autoasignación, token_cancelacion, concurrencia, rate limit, Ley 25.326)."""
import asyncio
import uuid
from datetime import timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.rate_limit import reset_rate_limit
from app.notifications.mock import MockNotificationService
from tests.conftest import proximo_dia_habil


def _dia_habil_desplazado(dias: int, hora: int = 10, minuto: int = 0):
    dt = proximo_dia_habil(hora, minuto)
    dt += timedelta(days=dias)
    while dt.weekday() > 4:  # asegurar lun-vie
        dt += timedelta(days=1)
    return dt


def _reserva_payload(ids, inicio, telefono="11-0000-0029", email="paciente.c29@example.com", sillon_id=None):
    iso = inicio.isoformat() if hasattr(inicio, "isoformat") else inicio
    payload = {
        "profesional_id": str(ids["p1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": iso,
        "paciente": {
            "nombre": "Mariana Guest Demo",
            "telefono": telefono,
            "email": email,
        },
    }
    if sillon_id:
        payload["sillon_id"] = str(sillon_id)
    return payload


async def test_reserva_exitosa_autoasigna_sillon_y_emite_token(
    client, seed_catalog, monkeypatch
):
    reset_rate_limit()
    mock_notif = MockNotificationService()
    monkeypatch.setattr(
        "app.application.reservas.get_notification_service", lambda: mock_notif, raising=False
    )

    inicio = proximo_dia_habil(10, 0)
    # Sin enviar sillon_id -> debe autoasignar uno disponible (s1 o s2)
    payload = _reserva_payload(seed_catalog, inicio)
    r = await client.post("/reservas", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()

    assert "id" in data
    assert "token_cancelacion" in data
    assert data["token_cancelacion"] is not None
    assert len(data["token_cancelacion"]) > 10
    assert data["sillon_id"] in [str(seed_catalog["s1"]), str(seed_catalog["s2"])]
    assert data["estado"] == "activo"
    assert data["cancelled_at"] is None


async def test_cancelacion_por_token_libera_slot_e_idempotente(
    client, seed_catalog
):
    reset_rate_limit()
    inicio = _dia_habil_desplazado(1, 10, 0)
    payload = _reserva_payload(seed_catalog, inicio, email="guest.cancel@example.com")
    r_create = await client.post("/reservas", json=payload)
    assert r_create.status_code == 201
    token = r_create.json()["token_cancelacion"]

    # Cancelación por token
    r_cancel = await client.post(f"/reservas/{token}/cancelacion")
    assert r_cancel.status_code == 200, r_cancel.text
    data_cancel = r_cancel.json()
    assert data_cancel["estado"] == "cancelado"
    assert data_cancel["cancelled_at"] is not None
    ts_primera_cancel = data_cancel["cancelled_at"]

    # Idempotencia: segunda cancelación devuelve 200 y conserva timestamp
    r_cancel_2 = await client.post(f"/reservas/{token}/cancelacion")
    assert r_cancel_2.status_code == 200
    assert r_cancel_2.json()["cancelled_at"] == ts_primera_cancel

    # Slot liberado: otro paciente puede reservar el mismo horario
    payload_nuevo = _reserva_payload(seed_catalog, inicio, email="guest.nuevo@example.com")
    r_nuevo = await client.post("/reservas", json=payload_nuevo)
    assert r_nuevo.status_code == 201


async def test_concurrencia_reservas_guest_ultimo_slot(
    client, seed_catalog
):
    reset_rate_limit()
    """Dos requests concurrentes al mismo profesional compitiendo por el único sillón disponible."""
    # Ocupar el sillón s2 de antemano para que solo quede s1
    inicio = _dia_habil_desplazado(2, 10, 0)
    headers_recepcion = {"X-API-Key": "test-recepcion-key"}
    r_bloqueo = await client.post(
        "/turnos",
        headers=headers_recepcion,
        json={
            "profesional_id": str(seed_catalog["p2"]), # otro profesional
            "sillon_id": str(seed_catalog["s2"]),       # ocupa sillon 2
            "prestacion_id": str(seed_catalog["c30"]),
            "inicio": inicio.isoformat(),
            "paciente": {"nombre": "Bloqueo Sillon", "email": "bloqueo@example.com"},
        },
    )
    assert r_bloqueo.status_code == 201

    # Ahora para el profesional p1 solo queda libre sillon 1.
    payload_a = _reserva_payload(seed_catalog, inicio, email="guest.a@example.com")
    payload_b = _reserva_payload(seed_catalog, inicio, email="guest.b@example.com")

    # Disparar ambos POST concurrentemente
    resp_a, resp_b = await asyncio.gather(
        client.post("/reservas", json=payload_a),
        client.post("/reservas", json=payload_b),
    )

    statuses = sorted([resp_a.status_code, resp_b.status_code])
    assert statuses == [201, 409], f"Se esperaba exactamente un 201 y un 409, obtenido: {statuses}"


async def test_reserva_guest_errores_y_ley_25326(
    client, seed_catalog
):
    reset_rate_limit()

    # 1. Token inexistente -> 404
    token_invalido = str(uuid.uuid4())
    r_404 = await client.post(f"/reservas/{token_invalido}/cancelacion")
    assert r_404.status_code == 404
    assert r_404.json()["code"] == "NO_ENCONTRADO"

    # 2. Ley 25.326: Rechazo con 422 ante campos clínicos no permitidos (extra="forbid")
    inicio = _dia_habil_desplazado(3, 11, 0)
    payload_extra = _reserva_payload(seed_catalog, inicio)
    payload_extra["diagnostico"] = "Carie profunda"
    payload_extra["obra_social"] = "OSDE 310"

    r_422 = await client.post("/reservas", json=payload_extra)
    assert r_422.status_code == 422

    # 3. Rate limiting: 10 reservas consecutivas permitidas, la 11ava devuelve 429
    reset_rate_limit()
    for i in range(10):
        dt = _dia_habil_desplazado(4 + i, 10, 0)
        p = _reserva_payload(seed_catalog, dt, email=f"ratelimit{i}@example.com")
        res = await client.post("/reservas", json=p)
        assert res.status_code in [201, 409], f"Req {i} falló inesperadamente: {res.status_code}"

    # La petición 11 debe superar el rate limit (10/min)
    dt_exceso = _dia_habil_desplazado(15, 10, 0)
    p_exceso = _reserva_payload(seed_catalog, dt_exceso, email="exceso@example.com")
    r_429 = await client.post("/reservas", json=p_exceso)
    assert r_429.status_code == 429
    assert r_429.json()["code"] == "RATE_LIMIT_EXCEEDED"
