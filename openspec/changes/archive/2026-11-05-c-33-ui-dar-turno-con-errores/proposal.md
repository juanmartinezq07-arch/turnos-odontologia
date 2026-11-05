# Proposal

## Why

La recepcionista necesita agendar turnos desde la UI sobre catálogos + disponibilidad, enviando solo `inicio` (RN01 calcula `fin` en servidor) y diferenciando 409 por regla (RN02_*, RN05) y 422 de validación en la interfaz.

## What Changes

- Pantalla "Dar turno": selección de profesional, prestación, sillón, fecha/hora; consulta de disponibilidad; alta vía `POST /turnos`.
- Manejo diferenciado de 409 (choque profesional/sillón/RN05) y 422 (pasado/fuera de horario/validación).
- Ingreso de datos mínimos del paciente (nombre + teléfono/email) sin campos clínicos.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `frontend-base`: se agrega la pantalla de alta de turno con manejo de errores por código (US-001, US-002).

## Impact

- `frontend/js/screens/dar-turno.js` (nuevo).
- `frontend/js/app.js` (ruta `#/dar-turno`).
- Sin cambios de backend.