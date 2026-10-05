"""Interfaz de notificaciones (D-07)."""
from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    async def notificar(self, evento: str, turno_id: str, destino: str) -> None:
        raise NotImplementedError
