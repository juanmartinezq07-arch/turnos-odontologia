# notifications/mock Specification

## Purpose
Define a mock notification service that records turn creation and update events in a best‑effort manner without affecting the core transaction.

## Requirements

### Requirement: Mock Notification Service
The system SHALL provide a `MockNotificationService` implementing the `NotificationService` interface. It records notification events in memory and logs any failures, but MUST NOT prevent the turn transaction from committing.

#### Scenario: Successful notification
- **WHEN** a turn is created or updated
- **THEN** the `MockNotificationService` records an event with the turn ID, type of operation, and timestamp.

#### Scenario: Notification error handling
- **WHEN** the mock service raises an exception while recording
- **THEN** the exception is logged and the turn transaction commits successfully.
