from abc import ABC, abstractmethod


class NotificationService(ABC):
    """Interface for notification services used after turn operations.

    Implementations must be *best‑effort*: failures should be logged but must not
    raise exceptions that abort the surrounding transaction.
    """

    @abstractmethod
    def notify_turn_created(self, turn_id: int) -> None:
        """Called after a turn is successfully created."""

    @abstractmethod
    def notify_turn_updated(self, turn_id: int) -> None:
        """Called after a turn is updated (e.g., reprogrammed or cancelled)."""

