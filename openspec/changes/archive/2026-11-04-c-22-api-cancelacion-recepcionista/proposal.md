# Proposal

## Why

La recepcionista necesita un endpoint autenticado (`POST /turnos/{id}/cancelacion`) para cancelar turnos existentes de forma inmediata e idempotente, registrando `cancelled_at = now()` y cambiando `estado = 'cancelado'` sin borrado físico (RN04). Con el esquema ya preparado en `C-20` (columna `cancelled_at`) y el servicio de notificaciones *best-effort* de `C-28`, implementar `C-22` permite que los predicados parciales `WHERE (estado = 'activo')` de PostgreSQL liberen automáticamente el slot en las agendas del profesional y del sillón (US-004 / CU03).

## What Changes

- Agregar el endpoint `POST /turnos/{id}/cancelacion` protegido por `require_recepcion` (`X-API-Key` con `API_KEY_RECEPCION`) en `backend/app/api/v1/turnos.py`.
- Extender el schema de salida `TurnoOut` en `backend/app/schemas/turno.py` incluyendo `cancelled_at: datetime | None = None` para reflejar el instante de cancelación.
- Implementar la función de aplicación `cancelar_turno(session, turno_id)` en `backend/app/application/bookings.py`:
  - Si el turno no existe, lanzar `NotFound("NO_ENCONTRADO", ...)` → `404`.
  - Si el turno está `activo`, actualizar `estado = "cancelado"` y `cancelled_at = _ahora()`, hacer `commit()` y disparar notificación *best-effort* (`get_notification_service().notify_turn_updated(turno.id)`).
  - Si el turno ya estaba `cancelado` (**idempotencia**), retornar el turno con `200 OK` **conservando intacto el `cancelled_at` original** sin sobrescribirlo.
- Agregar suite de pruebas de integración contra PostgreSQL 16 real (`backend/tests/test_cancelacion_api.py`) cubriendo cancelación exitosa + liberación de slot en RN02/RN05/disponibilidad, idempotencia de `cancelled_at`, `404 NO_ENCONTRADO`, `401` sin credencial y resiliencia de notificación *best-effort*.

## Capabilities

### New Capabilities
<!-- Ninguna capacidad nueva; extiende la capacidad existente `turnos`. -->

### Modified Capabilities
- `turnos`: Agrega el requerimiento de cancelación idempotente de turno por recepcionista (`POST /turnos/{id}/cancelacion`) con liberación inmediata del slot (RN04) y notificación post-commit *best-effort*.

## Impact

- **API (`backend/app/api/v1/turnos.py`)**: Nuevo endpoint `POST /turnos/{turno_id}/cancelacion` (`status_code=200`, `response_model=TurnoOut`).
- **Schemas (`backend/app/schemas/turno.py`)**: Campo `cancelled_at: datetime | None = None` expuesto en `TurnoOut`.
- **Aplicación (`backend/app/application/bookings.py`)**: Nueva operación transaccional `cancelar_turno` usando `AsyncSession` de SQLAlchemy 2.0 (`expire_on_commit=False`).
- **Tests (`backend/tests/test_cancelacion_api.py`)**: Nuevos tests de integración contra PostgreSQL 16 real verificando los escenarios de funcionamiento esperado, error de negocio y caso de borde (idempotencia).
