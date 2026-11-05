# Proposal

## Why

El paciente necesita reservar online 24/7 sin autenticación: catálogos → disponibilidad → `POST /reservas` → mostrar/guardar token de cancelación → cancelar con token. Solo contacto ficticio; sin datos clínicos (Ley 25.326).

## What Changes

- Flujo público sin auth: selección de profesional/prestación/fecha, slots, datos de contacto, reserva.
- Muestra y guarda el `token_cancelacion` (en memoria/localStorage solo para el guest, aceptado por DD-06).
- Cancelación con token vía `POST /reservas/{token}/cancelacion`.
- Validación de campos clínicos (rechazo 422) no aplica en UI (no se piden).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `frontend-base`: se agrega el flujo de reserva pública guest (US-003, US-004).

## Impact

- `frontend/js/screens/reserva.js` (nuevo).
- `frontend/js/app.js` (ruta `#/reserva`).
- Sin cambios de backend.