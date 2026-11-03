import logging
from typing import List, Dict
from .interface import NotificationService

log = logging.getLogger(__name__)

class MockNotificationService(NotificationService):
    """In‑memory mock notification service.

    Records events in a list ``events`` where each entry is a dict with
    ``turn_id`` and ``action``. Errors are caught and logged; they never
    propagate to the caller.
    """

    def __init__(self) -> None:
        self.events: List[Dict[str, int | str]] = []

    def _record(self, turn_id: int, action: str) -> None:
        try:
            self.events.append({"turn_id": turn_id, "action": action})
        except Exception as exc:  # pragma: no cover – defensive
            log.error("MockNotificationService failed to record event: %s", exc)

    def notify_turn_created(self, turn_id: int) -> None:
        self._record(turn_id, "created")

    def notify_turn_updated(self, turn_id: int) -> None:
        self._record(turn_id, "updated")

