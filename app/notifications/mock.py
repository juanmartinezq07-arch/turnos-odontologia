"""Mock best-effort: registra sin enviar. Un fallo nunca revierte el turno."""
import logging

from app.notifications.interface import NotificationService

log = logging.getLogger(__name__)


class MockNotificationService(NotificationService):
    def __init__(self) -> None:
        self.enviados: list[dict[str, str]] = []
        self.fallar: bool = False

    async def notificar(self, evento: str, turno_id: str, destino: str) -> None:
        if self.fallar:
            raise RuntimeError("mock de notificaciones caido (simulado)")
        self.enviados.append(
            {"evento": evento, "turno_id": turno_id, "destino": destino}
        )
        log.info("notificacion mock %s turno=%s destino=%s", evento, turno_id, destino)


_notifier = MockNotificationService()


def get_notifier() -> MockNotificationService:
    return _notifier
