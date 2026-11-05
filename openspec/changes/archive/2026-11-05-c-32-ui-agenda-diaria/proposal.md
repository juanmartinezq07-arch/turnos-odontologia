# Proposal

## Why

Con la base frontend vanilla (C-31) disponible, la recepcionista/odontólogo necesita ver la agenda del día (US-006) sobre `GET /agenda`: turnos ordenados por inicio con prestación, sillón y paciente, con filtro de cancelados y manejo de 403 para agenda ajena.

## What Changes

- Pantalla de agenda diaria: selector de profesional y fecha, tabla de turnos ordenada por `inicio`.
- Muestra prestación (con duración), sillón y paciente por turno.
- Filtro "incluir cancelados" toggle.
- Manejo visible de 403 (agenda ajena) y 401 (sin credencial).
- Ingreso de credencial de recepcionista/odontólogo en runtime.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `frontend-base`: se agrega la pantalla de agenda diaria (US-006) consumiendo `GET /agenda`.

## Impact

- `frontend/js/screens/agenda.js` (nuevo).
- `frontend/js/app.js` (registro de ruta `#/agenda`).
- Sin cambios de backend.