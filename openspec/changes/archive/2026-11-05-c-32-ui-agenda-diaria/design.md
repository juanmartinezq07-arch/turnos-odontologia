# Design

## Context

Ver `proposal.md`. Base frontend vanilla (C-31) disponible; endpoints de agenda (C-27) archivados.

## Goals / Non-Goals

**Goals:** pantalla de agenda consumiendo `GET /agenda`, orden por inicio, filtro cancelados, manejo 403/401.

**Non-Goals:** no modificar backend; no otras pantallas (C-33…C-35).

## Decisions

### 1. Formulario de credencial
Ingreso de API key + (opcional) profesional_id en un modal/panel lateral; se guarda en memoria via `auth.js`.

### 2. Consulta
`apiFetch(`/agenda?profesional_id=...&fecha=...&incluir_cancelados=...`)` con headers de auth.

### 3. Render
Tabla con columnas: inicio, prestación (duración), sillón, paciente, estado. Cancelados con estilo atenuado.

### 4. Errores
Mapear `AGENDA_AJENA` → "Solo podés ver tu propia agenda"; 401 → pedir credencial.

## Risks / Trade-offs

- [Sin backend de usuarios] La credencial se ingresa manualmente; aceptado por DD-08.

## Migration Plan

Solo archivos frontend. Sin migraciones.

## Open Questions

(none)