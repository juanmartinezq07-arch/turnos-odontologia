# Design

## Context

El esquema actual viene de las migraciones 001 (tablas), 002 (doble `EXCLUDE` RN02 + `CHECK`) y 003 (recorte de alcance que eliminó `cancelled_at`, `token_cancelacion` y el índice RN05). La 003 ya define en su `downgrade` cómo recrear `cancelled_at`, pero ese `downgrade` no se ejecuta y la 004 no debe editar migraciones aplicadas. El modelo `Turno` en `backend/app/domain/models.py` refleja el esquema de la 003. Los tests corren contra Postgres 16 real y crean el esquema con `Base.metadata.create_all`, no con Alembic.

Ver `proposal.md` para la motivación.

## Goals / Non-Goals

**Goals:**

- Restituir `cancelled_at` como columna nullable y agregar `idx_turno_paciente_fecha` mediante una migración 004 nueva, reversible.
- Mantener el modelo SQLAlchemy alineado con el esquema migrado.
- Demostrar con un test que la 004 no altera `estado`, `fin`, `CHECK (fin > inicio)` ni los dos `EXCLUDE` de RN02.

**Non-Goals:**

- No implementar el endpoint de cancelación (eso es `C-22`).
- No agregar `token_cancelacion` ni el índice RN05 (eso es `C-21`).
- No modificar la lógica de `POST /turnos` ni los schemas de la API.

## Decisions

- **Migración 004 nueva con `op.execute` de SQL explícito.** Sigue el estilo de 001–003 (SQL crudo), evita depender de autogenerate y deja explícito el `ALTER TABLE`/`CREATE INDEX`. Alternativa descartada: `op.add_column`/`op.create_index` con tipos SQLAlchemy, que sería más idiomático pero rompe la consistencia del repo.
- **Índice no único sobre `(paciente_id, inicio)`.** La KB lo define como índice de consulta, no como invariante; RN05 es otra cosa y la resuelve `C-21`. Alternativa descartada: índice único, que adelantaría RN05 y rompería la suite de `C-01` (un paciente con dos turnos el mismo día).
- **`cancelled_at` nullable sin default.** Un turno activo no tiene instante de cancelación; el default lo fija `C-22` al cancelar (`now()`).
- **Test de migración por introspección de catálogo.** Consulta `information_schema.columns`, `pg_indexes` y `pg_constraint` para verificar la columna, el índice y la persistencia de los EXCLUDE y el CHECK. Alternativa descartada: ejecutar `alembic upgrade`/`downgrade` dentro del test, que acopla el test a una base limpia y complica el aislamiento de la suite existente.

## Risks / Trade-offs

- **El test de la suite no usa Alembic** (usa `create_all`) → el test de migración debe inspeccionar el catálogo tras aplicar la 004 en una conexión dedicada, sin interferir con las fixtures que recrean el esquema. Mitigación: ejecutar la 004 con `alembic` sobre la base de test o verificar el estado del catálogo de forma idempotente.
- **Divergencia modelo ↔ migración** → si se olvida actualizar `models.py`, `create_all` y la migración difieren. Mitigación: actualizar `models.py` en la misma tarea y cubrirlo con el test.
- **`downgrade` deja el esquema de la 003** → no debe intentar recrear `token_cancelacion` ni RN05. Mitigación: `downgrade` solo dropea lo que la 004 creó.

## Migration Plan

1. `alembic upgrade head` aplica la 004 (columna + índice).
2. `alembic downgrade -1` revierte a la 003.
3. Rollback: el `downgrade` es la estrategia; no hay datos que transformar.
