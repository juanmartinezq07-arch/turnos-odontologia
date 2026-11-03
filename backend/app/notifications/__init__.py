import os
from .interface import NotificationService
from .mock import MockNotificationService


def get_notification_service() -> NotificationService:
    """Factory that returns a NotificationService implementation.

    The backend is selected via the ``NOTIF_BACKEND`` environment variable.
    Currently only ``mock`` is supported, which returns an in‑memory mock
    implementation. Extending this function with real back‑ends is straightforward.
    """
    backend = os.getenv("NOTIF_BACKEND", "mock").lower()
    if backend == "mock":
        return MockNotificationService()
    raise NotImplementedError(f"Notification backend '{backend}' is not implemented")

