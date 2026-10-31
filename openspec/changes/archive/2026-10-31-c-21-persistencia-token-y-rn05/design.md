# Design

## Context

`C-01` implementó la invariante RN02 con doble `EXCLUDE USING gist` parcial. `C-20` agregó `cancelled_at` y `idx_turno_paciente_fecha`. Falta ahora `token_cancelacion` (para reserva guest, CU02) y la invariante RN05 como índice único parcial en la base, cerrando la pregunta de prioridad Alta de `KB-10` (IN-01).

## Goals / Non-Goals

**Goals:**

- Agregar columna `token_cancelacion TEXT UNIQUE` nullable a `turno`.
- Agregar índice único parcial `rn05_un_activo_por_dia` para RN05 (máx. 1 activo por paciente/día).
- Que `downgrade` sea reversible al estado de la 004.
- Tests que verifiquen migración y comportamiento del índice RN05 contra Postgres real.

**Non-Goals:**

- Lógica de aplicación para generar/validar `token_cancelacion` (es `C-29`).
- Validación de RN05 en la capa de aplicación (es `C-26`).
- Endpoints públicos o guest booking.

## Decisions

### D-01 — Índice único parcial para RN05

`CREATE UNIQUE INDEX rn05_un_activo_por_dia ON turno (paciente_id, ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)) WHERE estado = 'activo'`. Así la base impone la invariante sin lógica procedural. Alternativa descartada: solo validación en Python (deja ventana de carrera).

### D-02 — Columna `token_cancelacion` nullable y única

Se agrega como `TEXT UNIQUE` nullable. Solo se llena en reserva guest (`C-29`); en alta por recepcionista (`POST /turnos`) queda NULL.

### D-03 — No editar migraciones aplicadas

La 005 tiene `down_revision = "004_cancelled_at_paciente_fecha"`. Nunca se editan 001–004.

## Risks / Trade-offs

- [Risk] **Regresión en fixtures de C-01**: los fixtures existentes usan un único paciente (`11-0000-0001`) para dos turnos activos del mismo día. Con el índice único parcial de RN05, esos tests fallan. Mitigación: parametrizar fixtures con pacientes distintos en `C-26`, no aquí. En `C-21` solo se crea el índice; los tests de migración usan pacientes distintos.
- [Risk] El índice usa `AT TIME ZONE` con zona hardcodeada `America/Argentina/Buenos_Aires`. Debe coincidir con `TZ_CONSULTORIO`.

## Migration Plan

1. `docker compose up -d db` (base ya levantada).
2. `alembic upgrade head`: aplica 005 sobre 004.
3. Verificar que `rn02_profesional`, `rn02_sillon`, `ck_turno_fin_mayor_inicio` sigan presentes.
4. Rollback: `alembic downgrade -1` (005) y luego base; nunca editar migración aplicada.

## Open Questions

- Ninguna que cambie specs, enfoque o tasks.
