# Design

## Context

`C-21` creó el índice parcial `rn05_un_activo_por_dia` en la base. Ahora falta traducir esa violación al código de error `RN05` y agregar la validación de aplicación para devolver 409 con mensaje claro. También se agrega `require_odontologo` para completar el auth mínimo de personal (necesario para C-27).

## Goals / Non-Goals

**Goals:**

- Mapear la violación del índice `rn05_un_activo_por_dia` al código `RN05` en `conflict_code_from_integrity_error`.
- Agregar precheck de RN05 en la capa de aplicación (antes del insert) para dar 409 con código `RN05` sin depender solo de la base.
- Agregar `require_odontologo` con `API_KEY_ODONTOLOGO` en `security.py`.
- Tests de punta a punta para RN05 (mismo paciente/mismo día → 409 `RN05`).
- Arreglar regresión en fixtures de C-01 (separar pacientes para turnos activos mismo día).

**Non-Goals:**

- Endpoint público de reserva guest (`C-29`).
- Notificaciones mock (`C-28`).
- Agenda del odontólogo (`C-27`, aunque se agrega el auth requerido aquí).

## Decisions

### D-01 — Mapeo de índice parcial a código RN05

En `conflict_code_from_integrity_error`, agregar detección de `rn05_un_activo_por_dia` → `"RN05"`. Se inspecciona el nombre del constraint vía `diag.constraint_name`, nunca parseo del mensaje de Postgres (consistente con D-05 de C-01).

### D-02 — Precheck de RN05 en aplicación

Antes del `INSERT`, consultar si ya existe un turno activo del mismo paciente (identidad por teléfono normalizado, fallback email — SU-03) en el mismo día calendario (zona `America/Argentina/Buenos_Aires`). Si existe, lanzar `DomainConflict("RN05", ...)` con status 409. La base sigue siendo el árbitro final (índice único parcial).

### D-03 — Identidad del paciente para RN05

Teléfono normalizado primero, email como fallback (SU-03). Normalización: solo dígitos para teléfono; minúsculas + trim para email. Si no hay teléfono ni email, no se puede aplicar RN05 (se deja solo a la base).

### D-04 — `require_odontologo`

Nueva dependency en `security.py` que valida `API_KEY_ODONTOLOGO` por env. Paralelo a `require_recepcion`.

## Risks / Trade-offs

- [Risk] **Regresión en fixtures de C-01**: `test_borde_que_se_toca_no_choca` y `test_borde_201` crean dos turnos activos del mismo paciente el mismo día. Con el índice de C-21 fallan. Mitigación: crear pacientes distintos en esos fixtures.
- [Risk] **Flaky en concurrencia**: `test_doble_post_concurrente_un_ganador` puede caer en RN05 en lugar de RN02 si usan el mismo paciente. Mitigación: usar pacientes distintos en el payload concurrente.

## Migration Plan

Ninguna migración nueva (C-21 ya creó el índice). Solo cambios de código de aplicación y tests.

## Open Questions

- Ninguna.
