# Design

## Context

Ver `proposal.md`. Base frontend vanilla (C-31) y endpoints (C-24, C-25) disponibles.

## Goals / Non-Goals

**Goals:** pantalla de alta con catálogos + disponibilidad + POST /turnos, manejo diferenciado de 409/422/401.

**Non-Goals:** no modificar backend; no reprogramación (C-34).

## Decisions

### 1. Flujo
1. Cargar catálogos (profesionales, sillones, prestaciones) al montar.
2. Seleccionar profesional + prestación + fecha → consultar disponibilidad → mostrar slots.
3. Seleccionar slot → completar datos paciente → POST /turnos con credencial.

### 2. Errores
Mapear códigos: `RN02_PROFESIONAL`→"Profesional ocupado", `RN02_SILLON`→"Sillón ocupado", `RN05`→"Paciente ya tiene turno ese día", `VALIDACION`/422→"Datos inválidos".

### 3. No enviar `fin`
El formulario solo envía `inicio`; RN01 calcula `fin` en servidor.

## Risks / Trade-offs

- [Disponibilidad puede quedar stale] Aceptado; el backend decide con RN02.

## Migration Plan

Solo archivos frontend. Sin migraciones.

## Open Questions

(none)