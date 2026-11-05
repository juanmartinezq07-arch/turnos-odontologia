# Proposal

## Why

El MVP ya permite alta y cancelación de turnos, pero la reprogramación (US-005) requiere una operación **atómica**: cancelar el turno original e insertar el nuevo en una única transacción, con rollback total si el destino viola RN02/RN03/RN05. Sin esto, la UI y los flujos de recepción no pueden reprogramar sin riesgo de dejar el slot inconsistente. El código y los tests ya existen; este change formaliza la especificación y cierra el gap de RN05 same-day.

## What Changes

- Formalizar el endpoint `POST /turnos/{id}/reprogramacion` (recepcionista autenticada) que cancela el original y crea el nuevo turno en una sola transacción.
- Asegurar atomicidad: ante conflicto en el destino (RN02/RN03/RN05) se hace rollback total y el original permanece `activo`.
- Corregir el precheck RN05 para excluir el turno original, habilitando reprogramación al mismo día del mismo paciente.
- Validaciones: turno inexistente → 404 `NO_ENCONTRADO`; ya cancelado → 409 `TURNO_NO_ACTIVO`; sin credencial → 401; campos extra → 422.
- Notificación best-effort post-commit (`notify_turn_updated` + `notify_turn_created`).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

(none — los requisitos de reprogramación atómica ya figuran en `openspec/specs/turnos/spec.md`; este change formaliza la implementación y corrige el precheck RN05 same-day, sin cambios de spec.)

## Impact

- `backend/app/application/bookings.py::reprogramar_turno`
- `backend/app/api/v1/turnos.py` (endpoint ya existente)
- `backend/app/schemas/turno.py` (`TurnoReprogramar`, `ReprogramacionOut`)
- `backend/tests/test_reprogramacion_api.py`
- `CHANGES.md` (marcar C-23 como completado al archivar)