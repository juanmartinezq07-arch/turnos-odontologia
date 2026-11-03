"""Tests para notificaciones mock (C-28).

Verifica:
1. Pruebas unitarias de MockNotificationService (registro de eventos y resiliencia).
2. Fábrica get_notification_service según NOTIF_BACKEND.
3. Llamada e integración best-effort en crear_turno (mockeando db_session).
4. Resiliencia: si el servicio de notificaciones falla/lanza excepción, la función no rompe.
"""
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.notifications.interface import NotificationService
from app.notifications.mock import MockNotificationService
from app.notifications import get_notification_service
from app.application import bookings
from datetime import datetime, timezone


def test_mock_notification_service_unit():
    service = MockNotificationService()
    assert isinstance(service, NotificationService)
    assert len(service.events) == 0

    service.notify_turn_created(101)
    service.notify_turn_updated(101)

    assert len(service.events) == 2
    assert service.events[0] == {"turn_id": 101, "action": "created"}
    assert service.events[1] == {"turn_id": 101, "action": "updated"}


def test_get_notification_service_factory(monkeypatch):
    monkeypatch.setenv("NOTIF_BACKEND", "mock")
    service = get_notification_service()
    assert isinstance(service, MockNotificationService)

    monkeypatch.setenv("NOTIF_BACKEND", "desconocido")
    with pytest.raises(NotImplementedError):
        get_notification_service()


@pytest.mark.asyncio
async def test_crear_turno_notifica_best_effort():
    mock_service = MockNotificationService()
    inicio = datetime(2026, 11, 10, 10, 0, tzinfo=timezone.utc)

    dummy_prest = MagicMock(id=1, duracion_min=30)
    dummy_paciente = MagicMock(id=1)

    session = AsyncMock()

    with patch("app.application.bookings._cargar_recursos", return_value=dummy_prest), \
         patch("app.application.bookings.get_or_create_paciente", return_value=dummy_paciente), \
         patch("app.application.bookings._validar_temporalidad", new_callable=AsyncMock), \
         patch("app.application.bookings._precheck_rn02", new_callable=AsyncMock), \
         patch("app.application.bookings._precheck_rn05", new_callable=AsyncMock), \
         patch("app.application.bookings.get_notification_service", return_value=mock_service):

        turno = await bookings.crear_turno(
            session=session,
            profesional_id=1,
            sillon_id=1,
            prestacion_id=1,
            inicio=inicio,
            nombre="Juan Mock",
            telefono="11-9999-0001",
            email="juan.mock@example.com",
        )

    assert session.commit.awaited
    assert len(mock_service.events) == 1
    assert mock_service.events[0] == {"turn_id": turno.id, "action": "created"}


@pytest.mark.asyncio
async def test_crear_turno_persiste_aunque_notificacion_falle():
    class ExplodingNotificationService(NotificationService):
        def notify_turn_created(self, turn_id: int) -> None:
            raise RuntimeError("Fallo simulado en servicio de notificacion")

        def notify_turn_updated(self, turn_id: int) -> None:
            raise RuntimeError("Fallo simulado")

    exploding_service = ExplodingNotificationService()
    inicio = datetime(2026, 11, 10, 11, 0, tzinfo=timezone.utc)

    dummy_prest = MagicMock(id=1, duracion_min=30)
    dummy_paciente = MagicMock(id=1)

    session = AsyncMock()

    with patch("app.application.bookings._cargar_recursos", return_value=dummy_prest), \
         patch("app.application.bookings.get_or_create_paciente", return_value=dummy_paciente), \
         patch("app.application.bookings._validar_temporalidad", new_callable=AsyncMock), \
         patch("app.application.bookings._precheck_rn02", new_callable=AsyncMock), \
         patch("app.application.bookings._precheck_rn05", new_callable=AsyncMock), \
         patch("app.application.bookings.get_notification_service", return_value=exploding_service):

        # No debe lanzar excepción
        turno = await bookings.crear_turno(
            session=session,
            profesional_id=1,
            sillon_id=1,
            prestacion_id=1,
            inicio=inicio,
            nombre="Maria Resiliente",
            telefono="11-9999-0002",
            email="maria.resiliente@example.com",
        )

    assert session.commit.awaited
    assert turno.estado == "activo"
