# Design

## Context

Ver `proposal.md`. Endpoints de cancelación/reprogramación (C-22, C-23) archivados.

## Goals / Non-Goals

**Goals:** pantallas de cancelación y reprogramación con estados y manejo de rollback.

**Non-Goals:** no modificar backend.

## Decisions

### 1. Cancelación
Formulario con ID de turno + botón cancelar; mostrar resultado y estado.

### 2. Reprogramación
Formulario con ID de turno, nuevo inicio, sillón opcional; mostrar original+nuevo o error con mensaje de rollback.

### 3. Errores
Mapear `TURNO_NO_ACTIVO`→"Turno ya cancelado", `RN02_*`/`RN05`→conflicto, `RN03_*`→validación.

## Risks / Trade-offs

- [Rollback visible] El mensaje deja claro que el original sigue activo.

## Migration Plan

Solo archivos frontend.

## Open Questions

(none)