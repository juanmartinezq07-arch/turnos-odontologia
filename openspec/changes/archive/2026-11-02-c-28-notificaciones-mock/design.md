# Design

## Overview
Implement a mock notification service that integrates with the turn creation flow. The service implements the `NotificationService` interface and records events in memory. It is invoked after a turn is persisted, using the `NOTIF_BACKEND` environment variable to select the mock implementation. Errors from the mock are logged but do not affect the transaction.

## Modules
- `backend/app/notifications/interface.py`: Defines the abstract `NotificationService` with methods `notify_turn_created(turn_id: int)` and `notify_turn_updated(turn_id: int)`.
- `backend/app/notifications/mock.py`: Implements `MockNotificationService` storing events in a thread‑safe list and logging exceptions.
- `backend/app/application/bookings.py`: After persisting a `Turn`, obtains the notification service via a factory (`get_notification_service()`) and calls the appropriate method.
- `backend/app/core/config.py`: Reads `NOTIF_BACKEND` (default `mock`).
- `.env.example`: Adds `NOTIF_BACKEND=mock` placeholder.

## Error Handling
Exceptions in the mock are caught; the service logs the error and the turn transaction proceeds.

## Tests
- Unit tests for `MockNotificationService` verifying event storage and error handling.
- Integration test ensuring a turn creation results in a notification entry.

