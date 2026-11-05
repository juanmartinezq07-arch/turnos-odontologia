# Design

## Context

Ver `proposal.md`. Endpoints públicos (C-24, C-25, C-29) archivados.

## Goals / Non-Goals

**Goals:** flujo guest completo sin auth, token de cancelación, cancelación con token.

**Non-Goals:** no modificar backend; no auth de paciente.

## Decisions

### 1. Flujo por pasos
1. Seleccionar profesional + prestación + fecha.
2. Consultar disponibilidad → mostrar slots.
3. Seleccionar slot → datos de contacto (nombre + teléfono/email).
4. POST /reservas → mostrar token (guardar en memoria + localStorage para el guest).
5. Cancelación con token.

### 2. Token
Guardar en `localStorage` bajo clave `turnos_guest_token` para permitir cancelar después. Aceptado por DD-06 (guest sin auth).

### 3. Errores
Mapear 409/422 a mensajes; 429 (rate limit) → "Demasiados intentos".

## Risks / Trade-offs

- [Token en localStorage] Aceptado para guest (DD-06); no es credencial de rol.

## Migration Plan

Solo archivos frontend.

## Open Questions

(none)