# Proposal

## Why

La recepcionista necesita cancelar y reprogramar turnos desde la UI, mostrando el resultado de la transacción y dejando explícito que, si la reprogramación falla, el original sigue activo (rollback total).

## What Changes

- Pantalla de gestión de turnos: listar/cancelar/reprogramar.
- Cancelación vía `POST /turnos/{id}/cancelacion` con confirmación y estado `cancelado`/`cancelled_at`.
- Reprogramación vía `POST /turnos/{id}/reprogramacion` mostrando original (cancelado) + nuevo (activo); ante fallo, mensaje de rollback y original intacto.
- Estados visibles `activo`/`cancelado`.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `frontend-base`: se agrega la pantalla de cancelación/reprogramación (US-004, US-005).

## Impact

- `frontend/js/screens/reprogramar.js` (nuevo).
- `frontend/js/app.js` (ruta `#/reprogramar`).
- Sin cambios de backend.