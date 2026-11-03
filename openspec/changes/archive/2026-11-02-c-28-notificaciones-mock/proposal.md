# Proposal

## Why
Se necesita un sistema de notificaciones que registre de forma *best‑effort* los eventos de creación y actualización de turnos. Actualmente, la lógica de negocio persiste el turno pero no informa a otros sistemas. Añadir una capa de notificación mock permite validar la integración sin depender de servicios externos, cumpliendo con la regla de no exponer datos reales de pacientes.

## What Changes
- Añadir la interfaz `NotificationService` en `backend/app/notifications/interface.py`.
- Implementar un mock en memoria `MockNotificationService` en `backend/app/notifications/mock.py`.
- Inyectar el backend mediante la variable de entorno `NOTIF_BACKEND=mock`.
- Registrar cualquier excepción del mock pero **no** revertir la transacción del turno.
- Actualizar la configuración y `.env.example` con la nueva variable.

## Capabilities
### New Capabilities
- `notifications/mock`: Capacidad que define la contractura de notificación *best‑effort* y su comportamiento mock.

## Impact
- Código nuevo en `backend/app/notifications/`.
- Cambios en `backend/app/application/bookings.py` para llamar al servicio tras crear un turno.
- Documentación actualizada en `knowledge-base/05_reglas_de_negocio.md`.

