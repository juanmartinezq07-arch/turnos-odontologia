"""Tests para C-23: POST /turnos/{id}/reprogramacion (RN04 + atomicidad + notificaciones)."""
import uuid
from datetime import timedelta

from app.notifications.mock import MockNotificationService
from tests.conftest import proximo_dia_habil


def _dia_habil_desplazado(dias: int, hora: int = 10, minuto: int = 0):
    dt = proximo_dia_habil(hora, minuto)
    dt += timedelta(days=dias)
    while dt.weekday() > 4:  # asegurar lun-vie
        dt += timedelta(days=1)
    return dt


def _alta_payload(ids, inicio, telefono="11-0000-0023", email="paciente.c23@example.com"):
    iso = inicio.isoformat() if hasattr(inicio, "isoformat") else inicio
    return {
        "profesional_id": str(ids["p1"]),
        "sillon_id": str(ids["s1"]),
        "prestacion_id": str(ids["c30"]),
        "inicio": iso,
        "paciente": {
            "nombre": "Esteban Reprogramacion Demo",
            "telefono": telefono,
            "email": email,
        },
    }


async def test_reprogramacion_exitosa(
    client, seed_catalog, headers_recepcion, monkeypatch
):
    mock_notif = MockNotificationService()
    monkeypatch.setattr(
        "app.application.bookings.get_notification_service", lambda: mock_notif
    )

    inicio_original = proximo_dia_habil(10, 0)
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio_original),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201, r_alta.text
    turno_orig_id = r_alta.json()["id"]

    nuevo_inicio = _dia_habil_desplazado(1, 11, 0)

    r_reprog = await client.post(
        f"/turnos/{turno_orig_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": nuevo_inicio.isoformat()},
    )
    assert r_reprog.status_code == 200, r_reprog.text
    datos = r_reprog.json()
    assert "original" in datos
    assert "nuevo" in datos
    assert datos["original"]["id"] == turno_orig_id
    assert datos["original"]["estado"] == "cancelado"
    assert datos["original"]["cancelled_at"] is not None
    assert datos["nuevo"]["id"] != turno_orig_id
    assert datos["nuevo"]["estado"] == "activo"
    assert datos["nuevo"]["cancelled_at"] is None

    # Verificar notificaciones: debe haber 1 "updated" para el original y 1 "created" para el nuevo
    turnos_notif = {ev["action"]: str(ev["turn_id"]) for ev in mock_notif.events}
    assert turnos_notif.get("updated") == turno_orig_id
    assert turnos_notif.get("created") == datos["nuevo"]["id"]


async def test_reprogramacion_cambio_sillon(
    client, seed_catalog, headers_recepcion
):
    """Triangulación: reprogramar a un sillón alternativo explícito."""
    inicio_original = proximo_dia_habil(10, 0)
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio_original),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201
    turno_orig_id = r_alta.json()["id"]

    nuevo_inicio = _dia_habil_desplazado(1, 12, 0)
    sillon_2 = str(seed_catalog["s2"])

    r_reprog = await client.post(
        f"/turnos/{turno_orig_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": nuevo_inicio.isoformat(), "sillon_id": sillon_2},
    )
    assert r_reprog.status_code == 200, r_reprog.text
    datos = r_reprog.json()
    assert datos["nuevo"]["sillon_id"] == sillon_2
    assert datos["nuevo"]["estado"] == "activo"
    assert datos["original"]["estado"] == "cancelado"


async def test_reprogramacion_extra_fields_forbidden(
    client, seed_catalog, headers_recepcion
):
    """Triangulación: extra='forbid' rechaza campos no permitidos con 422."""
    inicio_original = proximo_dia_habil(10, 0)
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio_original),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201
    turno_orig_id = r_alta.json()["id"]

    nuevo_inicio = _dia_habil_desplazado(1, 14, 0)
    r_reprog = await client.post(
        f"/turnos/{turno_orig_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": nuevo_inicio.isoformat(), "campo_extra": "prohibido"},
    )
    assert r_reprog.status_code == 422


async def test_reprogramacion_conflicto_destino_rollback_total(
    client, seed_catalog, headers_recepcion
):
    inicio_1 = proximo_dia_habil(10, 0)
    # Crear Turno 1 (que se intentará reprogramar)
    r1 = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio_1, email="p1@example.com"),
        headers=headers_recepcion,
    )
    assert r1.status_code == 201
    turno_1_id = r1.json()["id"]

    # Crear Turno 2 en otro día hábil
    inicio_2 = _dia_habil_desplazado(2, 10, 0)
    r2 = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio_2, email="p2@example.com"),
        headers=headers_recepcion,
    )
    assert r2.status_code == 201

    # Intentar reprogramar Turno 1 al horario ocupado por Turno 2 (mismo profesional/sillón)
    r_reprog = await client.post(
        f"/turnos/{turno_1_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": inicio_2.isoformat()},
    )
    assert r_reprog.status_code == 409, r_reprog.text
    assert r_reprog.json()["code"] == "RN02_PROFESIONAL"

    # Verificar que Turno 1 NO fue cancelado (rollback total atómico): puede ser cancelado exitosamente
    r_canc = await client.post(
        f"/turnos/{turno_1_id}/cancelacion",
        headers=headers_recepcion,
    )
    assert r_canc.status_code == 200, "Turno original debió permanecer activo tras rollback"
    assert r_canc.json()["estado"] == "cancelado"


async def test_reprogramacion_mismo_dia_mismo_paciente(
    client, seed_catalog, headers_recepcion
):
    """RN05 no debe rechazar la reprogramación al mismo día del mismo paciente:
    el turno original queda cancelado y el nuevo queda activo."""
    inicio_original = proximo_dia_habil(10, 0)
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, inicio_original),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201
    turno_orig_id = r_alta.json()["id"]

    # Reprogramar a la misma fecha, otra hora (sin solapar con el original)
    nuevo_inicio = inicio_original.replace(hour=14, minute=0)

    r_reprog = await client.post(
        f"/turnos/{turno_orig_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": nuevo_inicio.isoformat()},
    )
    assert r_reprog.status_code == 200, r_reprog.text
    datos = r_reprog.json()
    assert datos["original"]["id"] == turno_orig_id
    assert datos["original"]["estado"] == "cancelado"
    assert datos["nuevo"]["estado"] == "activo"
    assert datos["nuevo"]["id"] != turno_orig_id


async def test_reprogramacion_errores_validacion(
    client, seed_catalog, headers_recepcion
):
    # 1. Turno inexistente -> 404
    random_id = str(uuid.uuid4())
    futuro = _dia_habil_desplazado(3, 10, 0).isoformat()
    r_404 = await client.post(
        f"/turnos/{random_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": futuro},
    )
    assert r_404.status_code == 404
    assert r_404.json()["code"] == "NO_ENCONTRADO"

    # 2. Sin auth recepcionista -> 401
    r_401 = await client.post(
        f"/turnos/{random_id}/reprogramacion",
        headers={"X-API-Key": "invalida"},
        json={"inicio": futuro},
    )
    assert r_401.status_code == 401

    # 3. Fecha en el pasado -> 422
    r_alta = await client.post(
        "/turnos",
        json=_alta_payload(seed_catalog, proximo_dia_habil(11, 0)),
        headers=headers_recepcion,
    )
    assert r_alta.status_code == 201
    turno_id = r_alta.json()["id"]

    pasado = "2020-01-01T10:00:00Z"
    r_past = await client.post(
        f"/turnos/{turno_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": pasado},
    )
    assert r_past.status_code == 422
    assert r_past.json()["code"] == "RN03_PASADO"

    # 4. Turno ya cancelado -> 409
    r_canc = await client.post(
        f"/turnos/{turno_id}/cancelacion",
        headers=headers_recepcion,
    )
    assert r_canc.status_code == 200

    r_ya_canc = await client.post(
        f"/turnos/{turno_id}/reprogramacion",
        headers=headers_recepcion,
        json={"inicio": futuro},
    )
    assert r_ya_canc.status_code == 409
    assert r_ya_canc.json()["code"] == "TURNO_NO_ACTIVO"
