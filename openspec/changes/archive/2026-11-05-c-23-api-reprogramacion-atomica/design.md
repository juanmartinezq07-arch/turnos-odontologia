# Design

## Context

Ver `proposal.md` — Why. La reprogramación ya existe en `bookings.py::reprogramar_turno` y el endpoint `POST /turnos/{id}/reprogramacion`. Este change formaliza la implementación y corrige el orden del precheck RN05.

## Goals / Non-Goals

**Goals:**
- Garantizar atomicidad cancelar+crear en una única transacción.
- Rollback total ante violación de RN02/RN03/RN05.
- Permitir reprogramación al mismo día del mismo paciente (fix RN05).

**Non-Goals:**
- No cambiar el contrato del endpoint ni los schemas.
- No introducir locks pesimistas; se confía en el precheck + constraint de DB.

## Decisions

### 1. Orden de validaciones
1. Cargar turno origen (404 si no existe; 409 `TURNO_NO_ACTIVO` si cancelado).
2. Validar recursos destino (profesional/sillón/prestación).
3. Calcular `fin` (RN01).
4. RN03 temporal + horario.
5. Precheck RN02 (profesional/sillón).
6. Cancelar original en memoria (`estado='cancelado'`, `cancelled_at=now()`).
7. Precheck RN05 **excluyendo el turno original** (`Turno.id != turno_orig.id`), para no rechazar falsamente al reprogramar al mismo día.
8. Insertar nuevo turno; `flush()` captura `IntegrityError` → rollback + `DomainConflict`.
9. `commit()` y notificaciones best-effort.

### 2. Manejo del rollback
Ante `IntegrityError` en `flush()`, se llama `session.rollback()` (revierte también el cancel en memoria) y se re-lanza como `DomainConflict` con código por nombre de constraint. El original permanece `activo` en DB.

### 3. Notificaciones
Post-commit, best-effort: `notify_turn_updated(original)` + `notify_turn_created(nuevo)`. Si fallan, se loguea y no se revierte.

## Risks / Trade-offs

- [RN05 same-day] Mitigado excluyendo el turno original del precheck.
- [Carrera entre precheck e insert] Mitigado por el constraint `rn05_un_activo_por_dia` y el mapeo de `IntegrityError`.
- [Sesión sucia tras excepción de precheck] Mitigado por el rollback del dependency `get_session` en FastAPI.

## Migration Plan

Sin migraciones: solo cambio de código. Tests existentes en `test_reprogramacion_api.py`.

## Open Questions

(none)